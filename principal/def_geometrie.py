# -*- coding: utf-8 -*-
# =============================================================================
# FICHIER : def_geometrie.py
# DESCRIPTION : Ce module contient la logique de construction géométrique.
#               Il ne contient pas de valeurs "en dur" (dimensions ou noms),
#               celles-ci sont passées via les dictionnaires 'params' et 'names'.
# =============================================================================

from abaqus import *
from abaqusConstants import *
from caeModules import *
import regionToolset
import math

# =============================================================================
# 1. OUTILS UTILITAIRES (Fonctions d'aide)
# =============================================================================

def clean_features(model, object_names, object_type='Part'):
    """
    Supprime proprement des objets (Parts, Sketches, Instances) s'ils existent déjà.
    
    Pourquoi cette fonction ?
    Abaqus plante si on essaie de créer un objet qui porte le même nom qu'un objet existant.
    Il faut donc "faire le ménage" avant de créer quoi que ce soit.
    
    Args:
        model : L'objet modèle Abaqus dans lequel on travaille.
        object_names (list) : Liste des noms (str) à supprimer (ex: ['MaTour']).
        object_type (str) : Ce qu'on veut supprimer ('Part', 'Sketch' ou 'Instance').
    """
    for name in object_names:
        # On vérifie si le nom existe dans le dictionnaire correspondant du modèle
        if object_type == 'Part' and name in model.parts:
            del model.parts[name]
        elif object_type == 'Sketch' and name in model.sketches:
            del model.sketches[name]
        elif object_type == 'Instance' and name in model.rootAssembly.instances:
            del model.rootAssembly.instances[name]


# =============================================================================
# 2. VÉRIFICATION DES PARAMÈTRES (Sécurité Physique)
# =============================================================================

def check_parameters(params):
    """
    Vérifie que les dimensions fournies sont physiquement possibles.
    Cela évite de lancer un calcul voué à l'échec (géométrie impossible).
    
    Args:
        params (dict): Dictionnaire contenant les dimensions (rayons, hauteurs...).
    """
    print("--- Vérification des paramètres géométriques ---")
    
    # Liste des clés qui doivent impérativement être positives
    required_positive = [
        'cone_thickness', 'cone_top_outer_radius', 'plateau_radius', 
        'plateau_height', 'cyl_height', 'thickness_tower', 'h_tower'
    ]
    
    # 1. Test de positivité
    for key in required_positive:
        if params[key] <= 0:
            # 'raise ValueError' arrête le script immédiatement avec un message d'erreur
            raise ValueError(f"Erreur paramètre : '{key}' doit être strictement positif.")

    # 2. Test de cohérence géométrique du cône
    # Le rayon extérieur bas doit être plus grand que l'épaisseur, sinon le rayon intérieur est négatif !
    if params['cone_bottom_outer_radius'] <= params['cone_thickness']:
        raise ValueError("Le rayon bas du cône est trop petit par rapport à son épaisseur.")

    # 3. Test de l'assemblage (Interface Tour / GBS)
    # On vérifie que la tour ne tombe pas dans le trou du GBS ou ne flotte pas à l'extérieur.
    
    r_gbs_ext = params['cone_top_outer_radius']           # Rayon extérieur sommet GBS
    r_gbs_hole = r_gbs_ext - params['cone_thickness']     # Rayon du trou du GBS
    r_tower_bot = params['r_down_tower']                  # Rayon de la base de la tour

    # Si la tour est plus petite que le trou
    if r_tower_bot <= r_gbs_hole:
        raise ValueError(
            f"ERREUR : La base de la tour (R={r_tower_bot}) est plus petite que le trou du GBS (R={r_gbs_hole})."
        )

    # Si la tour est plus large que le sommet du GBS
    if r_tower_bot > r_gbs_ext:
        raise ValueError(
            f"ERREUR : La tour (R={r_tower_bot}) dépasse du sommet du GBS (R={r_gbs_ext})."
        )

    print("✅ Paramètres géométriques valides.")


# =============================================================================
# 3. CRÉATION DE LA TOUR (Partie Acier)
# =============================================================================

def create_tower(model, params, names):
    """
    Crée la géométrie de la Tour.
    La tour est définie par un profil trapézoïdal tourné à 360° (Révolution).
    
    Args:
        model : Le modèle Abaqus.
        params (dict) : Dimensions géométriques.
        names (dict) : Dictionnaire contenant les noms (ex: names['part_tower']).
        
    Returns:
        final_part : L'objet 'Part' créé dans Abaqus.
    """
    # On récupère le nom que l'utilisateur veut donner à la pièce et à la surface
    part_name = names['part_tower']
    surf_name = names['surf_tower']
    
    # Dimensions
    r_up = params['r_up_tower']
    r_down = params['r_down_tower']
    h = params['h_tower']
    t = params['thickness_tower']
    
    # Taille de la feuille de dessin (Sketch) : doit être assez grande pour contenir la pièce
    sheetSize = max(r_down, h) * 3.0

    # --- Fonction Locale (Interne) ---
    # Sert à dessiner un tronc de cône PLEIN par révolution.
    # On l'utilise deux fois : une fois pour l'extérieur, une fois pour l'intérieur (le trou).
    def create_revolve_part(temp_part_name, r_bot, r_top, height):
        # 1. Nettoyage et création du Sketch (Plan 2D)
        sketch_name = f'__profile_{temp_part_name}__'
        clean_features(model, [sketch_name], 'Sketch')
        
        model.ConstrainedSketch(name=sketch_name, sheetSize=sheetSize)
        s = model.sketches[sketch_name]
        
        # Axe de révolution (Ligne verticale au centre)
        s.ConstructionLine(point1=(0, -sheetSize), point2=(0, sheetSize))
        
        # Dessin du demi-profil (Trapèze rectangle)
        # On part du centre bas (0,0) -> droite -> haut -> gauche -> retour centre
        s.Line(point1=(0, 0), point2=(r_bot, 0))       
        s.Line(point1=(r_bot, 0), point2=(r_top, height)) 
        s.Line(point1=(r_top, height), point2=(0, height)) 
        s.Line(point1=(0, height), point2=(0, 0))       

        # 2. Création de la Part 3D par Révolution
        clean_features(model, [temp_part_name], 'Part')
        p = model.Part(name=temp_part_name, dimensionality=THREE_D, type=DEFORMABLE_BODY)
        p.BaseSolidRevolve(angle=360.0, sketch=s)
        
        # On supprime le sketch pour ne pas polluer le fichier
        del model.sketches[sketch_name]
        return p

    # --- Logique Principale : Création du Tube ---
    
    # Calcul des rayons intérieurs (Rayon ext - épaisseur)
    r_up_in = r_up - t
    r_down_in = r_down - t
    
    # Est-ce un tube creux ? (Oui si rayons intérieurs > 0)
    is_hollow = (r_up_in > 0 and r_down_in > 0)

    if not is_hollow:
        # Cas simple : Barre pleine
        final_part = create_revolve_part(part_name, r_down, r_up, h)
    else:
        # Cas complexe : Tube creux
        # On utilise la méthode booléenne : Volume Extérieur MOINS Volume Intérieur
        
        # 1. Créer les deux formes temporaires
        part_outer = create_revolve_part('__Temp_Outer__', r_down, r_up, h)
        part_inner = create_revolve_part('__Temp_Inner__', r_down_in, r_up_in, h)

        # 2. Les mettre dans l'assemblage (Abaqus a besoin d'instances pour faire une coupe)
        a = model.rootAssembly
        clean_features(model, ['__Inst_Out__', '__Inst_In__'], 'Instance')
        inst_outer = a.Instance(name='__Inst_Out__', part=part_outer, dependent=ON)
        inst_inner = a.Instance(name='__Inst_In__', part=part_inner, dependent=ON)

        # 3. Opération de Coupe (Cut)
        clean_features(model, [part_name], 'Part')
        a.InstanceFromBooleanCut(
            name=part_name, 
            instanceToBeCut=inst_outer, 
            cuttingInstances=(inst_inner, ),
            originalInstances=SUPPRESS # Masque les originaux
        )
        final_part = model.parts[part_name]

        # 4. Nettoyage des objets temporaires
        if f'{part_name}-1' in a.instances: del a.instances[f'{part_name}-1']
        clean_features(model, ['__Inst_Out__', '__Inst_In__'], 'Instance')
        clean_features(model, ['__Temp_Outer__', '__Temp_Inner__'], 'Part')

    # --- Création de la Surface Latérale (Nommée) ---
    # Utile pour appliquer la pression du vent/eau plus tard.
    # On cherche la face en visant un point au milieu de la hauteur et sur le rayon extérieur.
    target_point = ((r_down + r_up) / 2.0, h / 2.0, 0.0)
    faces_ext = final_part.faces.findAt((target_point, ))
    
    if not faces_ext:
        print(f"ATTENTION: Surface introuvable sur {part_name} au point {target_point}")
    else:
        # On crée la surface avec le nom défini dans 'names'
        final_part.Surface(name=surf_name, side1Faces=faces_ext)
    
    print(f"-> Pièce '{part_name}' créée avec sa surface '{surf_name}'.")
    return final_part


# =============================================================================
# 4. CRÉATION DU GBS (Partie Béton)
# =============================================================================

def create_fused_gbs(model, params, names):
    """
    Construit le GBS (Gravity Based Structure).
    C'est une pièce complexe faite de 3 parties : Plateau, Cône, Cylindre.
    On les crée séparément puis on les fusionne (Merge) en une seule pièce.
    """
    # Noms depuis le dictionnaire
    part_name = names['part_gbs']
    surf_name = names['surf_gbs']
    
    # Dimensions
    h_plat = params['plateau_height']
    r_plat = params['plateau_radius']
    h_cone = params['cone_height']
    t_cone = params['cone_thickness']
    r_ext_bot = params['cone_bottom_outer_radius']
    r_ext_top = params['cone_top_outer_radius']
    # Rayons intérieurs du cône (pour le creux)
    r_int_bot = r_ext_bot - t_cone
    r_int_top = r_ext_top - t_cone
    h_cyl = params['cyl_height']
    
    a = model.rootAssembly
    # Taille de la zone de dessin
    sheetSize = max(r_plat, h_cone + h_cyl) * 2.5

    # --- Étape A : Création des 3 formes primitives (Temporaires) ---
    
    # 1. Le Plateau (Cylindre plat plein)
    clean_features(model, ['__Plateau__'], 'Part')
    model.ConstrainedSketch(name='__s_plat__', sheetSize=sheetSize)
    s = model.sketches['__s_plat__']
    s.ConstructionLine(point1=(0, -100), point2=(0, 100)) # Axe
    # Profil rectangulaire à droite de l'axe
    s.Line(point1=(0, 0), point2=(r_plat, 0))
    s.Line(point1=(r_plat, 0), point2=(r_plat, h_plat))
    s.Line(point1=(r_plat, h_plat), point2=(0, h_plat))
    s.Line(point1=(0, h_plat), point2=(0, 0))
    p_plat = model.Part(name='__Plateau__', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    p_plat.BaseSolidRevolve(angle=360.0, sketch=s)

    # 2. Le Cône (Tronc de cône creux)
    clean_features(model, ['__Cone__'], 'Part')
    model.ConstrainedSketch(name='__s_cone__', sheetSize=sheetSize)
    s = model.sketches['__s_cone__']
    s.ConstructionLine(point1=(0, -100), point2=(0, 100))
    # Profil trapézoïdal creux (parois seulement)
    s.Line(point1=(r_ext_bot, 0), point2=(r_ext_top, h_cone)) # Extérieur
    s.Line(point1=(r_ext_top, h_cone), point2=(r_int_top, h_cone)) # Epaisseur haut
    s.Line(point1=(r_int_top, h_cone), point2=(r_int_bot, 0)) # Intérieur
    s.Line(point1=(r_int_bot, 0), point2=(r_ext_bot, 0)) # Epaisseur bas
    p_cone = model.Part(name='__Cone__', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    p_cone.BaseSolidRevolve(angle=360.0, sketch=s)

    # 3. Le Cylindre Supérieur (Tube)
    clean_features(model, ['__Cyl__'], 'Part')
    model.ConstrainedSketch(name='__s_cyl__', sheetSize=sheetSize)
    s = model.sketches['__s_cyl__']
    s.ConstructionLine(point1=(0, -100), point2=(0, 100))
    s.Line(point1=(r_ext_top, 0), point2=(r_ext_top, h_cyl))
    s.Line(point1=(r_int_top, h_cyl), point2=(r_ext_top, h_cyl)) # Fermeture haut (Bouchon ?)
    # Note: Dans le code original, il y avait une fermeture. Je garde la logique.
    s.Line(point1=(r_int_top, 0), point2=(r_int_top, h_cyl))
    s.Line(point1=(r_int_top, 0), point2=(r_ext_top, 0))
    p_cyl = model.Part(name='__Cyl__', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    p_cyl.BaseSolidRevolve(angle=360.0, sketch=s)
    
    # Nettoyage des sketches
    for k in ['__s_plat__', '__s_cone__', '__s_cyl__']:
        if k in model.sketches: del model.sketches[k]

    # --- Étape B : Positionnement pour assemblage ---
    clean_features(model, ['__I_Plat__', '__I_Cone__', '__I_Cyl__'], 'Instance')
    
    # On crée des instances temporaires
    i_plat = a.Instance(name='__I_Plat__', part=p_plat, dependent=ON)
    
    # Le cône est posé sur le plateau
    i_cone = a.Instance(name='__I_Cone__', part=p_cone, dependent=ON)
    a.translate(instanceList=(i_cone.name,), vector=(0.0, h_plat, 0.0))
    
    # Le cylindre est posé sur le cône
    i_cyl = a.Instance(name='__I_Cyl__', part=p_cyl, dependent=ON)
    a.translate(instanceList=(i_cyl.name,), vector=(0.0, h_plat + h_cone, 0.0))

    # --- Étape C : Fusion Finale (Merge) ---
    clean_features(model, [part_name], 'Part')
    
    # Cette commande fusionne les instances en une seule Part maillable
    a.InstanceFromBooleanMerge(
        name=part_name,
        instances=(i_plat, i_cone, i_cyl),
        keepIntersections=True,   # Garde les frontières internes (aide le maillage)
        originalInstances=SUPPRESS,
        domain=GEOMETRY
    )
    
    gbs_part = model.parts[part_name]

    # --- Étape D : Création de la Surface Extérieure "Propre" ---
    # Comme la pièce est fusionnée, la surface extérieure est composée de plusieurs faces.
    # On va sélectionner un point sur chaque face composant l'extérieur.
    
    pts_to_find = [
        (r_plat, h_plat/2.0, 0.0),                        # Flanc du plateau
        ((r_ext_bot+r_ext_top)/2.0, h_plat + h_cone/2.0, 0.0), # Flanc du cône
        (r_ext_top, h_plat + h_cone + h_cyl/2.0, 0.0)        # Flanc du cylindre haut
    ]
    
    # findAt peut prendre plusieurs points d'un coup
    # L'astuce *[(p,) for p in pts] transforme la liste en arguments séparés pour findAt
    try:
        faces_found = gbs_part.faces.findAt(*[(p,) for p in pts_to_find])
        gbs_part.Surface(name=surf_name, side1Faces=faces_found)
    except Exception as e:
        print(f"Erreur lors de la création de la surface GBS : {e}")

    # --- Étape E : Nettoyage des pièces temporaires ---
    clean_features(model, ['__Plateau__', '__Cone__', '__Cyl__'], 'Part')
    
    print(f"-> Pièce '{part_name}' créée avec sa surface '{surf_name}'.")
    return gbs_part


# =============================================================================
# 5. ASSEMBLAGE FINAL (Positionnement)
# =============================================================================

def create_assembly_geometry(model, names, h_pipe_bottom, h_gbs_top):
    """
    Met en place l'assemblage final (Assembly).
    Récupère les pièces créées et crée les Instances définitives.
    
    Args:
        names (dict) : Doit contenir les noms des Parts et des Instances futures.
        h_pipe_bottom : Altitude du bas de la tour (souvent 0).
        h_gbs_top : Altitude du sommet du GBS (là où on doit poser la tour).
    """
    a = model.rootAssembly
    
    # 1. Nettoyage de l'assemblage (pour éviter les doublons)
    if hasattr(a, 'instances'):
        for k in list(a.instances.keys()): del a.instances[k]

    # 2. Récupération des Parts existantes
    p_gbs_name = names['part_gbs']
    p_tower_name = names['part_tower']
    
    # Vérification que les parts existent
    if p_gbs_name not in model.parts or p_tower_name not in model.parts:
        raise ValueError("Les Parts n'ont pas été créées. Lancez create_tower/create_gbs avant.")

    p_gbs = model.parts[p_gbs_name]
    p_tower = model.parts[p_tower_name]
    
    # 3. Création des Instances (Objets réels dans la simulation)
    # On utilise les noms définis dans le dictionnaire 'names'
    inst_gbs_name = names['inst_gbs']
    inst_tower_name = names['inst_tower']
    
    print("--- Création des Instances ---")
    inst_gbs = a.Instance(name=inst_gbs_name, part=p_gbs, dependent=ON)
    inst_tower = a.Instance(name=inst_tower_name, part=p_tower, dependent=ON)

    # 4. Positionnement de la Tour
    # Par défaut, la tour est créée à Y=0. On doit la monter sur le GBS.
    dy = h_gbs_top - h_pipe_bottom
    if abs(dy) > 1e-6: # Si le déplacement n'est pas nul
        a.translate(instanceList=(inst_tower_name, ), vector=(0.0, dy, 0.0))
        print(f"-> Tour '{inst_tower_name}' translatée de DY = {dy:.2f} m")

    return inst_gbs, inst_tower


# =============================================================================
# 6. GESTION DES SURFACES GLOBALES (Pour chargement)
# =============================================================================

def fus_outer_surfaces(model, inst_gbs, inst_tower, names):
    """
    Crée une surface unique qui combine l'extérieur du GBS et de la Tour.
    Cela permet d'appliquer une force globale (ex: Vent ou Courant) sur l'ensemble.
    
    Args:
        inst_gbs, inst_tower : Les OBJETS instances réels.
        names (dict) : Contient les noms des surfaces à chercher et le nom final à créer.
    """
    a = model.rootAssembly
    
    # Récupération des noms depuis le dictionnaire
    surf_gbs_key = names['surf_gbs']       # ex: 'Surf_Ext_GBS'
    surf_tower_key = names['surf_tower']   # ex: 'Surf_Lat_Tower'
    surf_global_key = names['surf_global'] # ex: 'Surf_Totale_Ext'
    
    print(f"--- Fusion des surfaces : {surf_gbs_key} + {surf_tower_key} -> {surf_global_key} ---")

    # 1. Vérification d'existence (Sécurité)
    if surf_gbs_key not in inst_gbs.surfaces:
        raise KeyError(f"La surface '{surf_gbs_key}' n'existe pas sur l'instance GBS.")
    if surf_tower_key not in inst_tower.surfaces:
        raise KeyError(f"La surface '{surf_tower_key}' n'existe pas sur l'instance Tour.")

    # 2. Récupération des objets surfaces
    s_gbs = inst_gbs.surfaces[surf_gbs_key]
    s_tower = inst_tower.surfaces[surf_tower_key]

    # 3. Nettoyage si la surface globale existe déjà
    if surf_global_key in a.surfaces:
        del a.surfaces[surf_global_key]

    # 4. Fusion (Union)
    a.SurfaceByBoolean(
        name=surf_global_key,
        surfaces=(s_gbs, s_tower),
        operation=UNION
    )
    print(f"-> Surface globale '{surf_global_key}' créée avec succès.")

# =============================================================================
# Création des points de contrôle
# =============================================================================

def create_monitor_set(model, names, inst_tower, h_total):
    """
    Crée un Set (point de repère) au sommet de la tour pour suivre son déplacement.
    Utilise le nom défini dans le dictionnaire 'names'.
    
    Args:
        model : Le modèle Abaqus.
        names (dict) : Le dictionnaire de configuration (doit contenir 'set_monitor').
        inst_tower : L'objet Instance de la tour (pour chercher les arêtes).
        h_total : La hauteur totale (Y) où se trouve le sommet.
    """
    print(f"\n--- Création du Set de Monitoring (Cible : Sommet à Y={h_total:.2f}m) ---")
    a = model.rootAssembly
    
    # 1. Récupération du nom du Set
    if 'set_monitor' not in names:
        raise KeyError("Le dictionnaire 'names' ne contient pas la clé 'set_monitor'.")
    
    set_name = names['set_monitor']
    
    # 2. Nettoyage préventif
    # Si le set existe déjà (ex: relance du script), on le supprime pour le recréer propre.
    if set_name in a.sets:
        del a.sets[set_name]

    # 3. Sélection Géométrique Robuste (Bounding Box)
    # Au lieu de chercher un point précis (risqué), on capture tout ce qui est
    # dans une tranche très fine au sommet (+/- 1 cm).
    try:
        # On cherche les arêtes (Edges) du cercle supérieur
        top_edges = inst_tower.edges.getByBoundingBox(
            yMin=h_total - 0.01,  # 1 cm en dessous
            yMax=h_total + 0.01,  # 1 cm au dessus
            xMin=-500.0, xMax=500.0, # Large en X
            zMin=-500.0, zMax=500.0  # Large en Z
        )
        
        # Vérification qu'on a bien attrapé quelque chose
        if len(top_edges) == 0:
            print(f"ERREUR CRITIQUE : Aucune arête trouvée à l'altitude Y={h_total}m !")
            print("Vérifiez la hauteur totale calculée dans main.py.")
            return

        # 4. Création du Set
        a.Set(name=set_name, edges=top_edges)
        print(f"-> Set '{set_name}' créé avec succès ({len(top_edges)} arêtes sélectionnées).")
        
    except Exception as e:
        print(f"ERREUR lors de la création du Set de monitoring : {e}")