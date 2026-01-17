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
def create_tower_1d(model, param, names):
    """
    Crée la géométrie de la tour sous forme de fil (WIRE) pour éléments poutres (B31).
    """
    print(f"   -> Mode 1D : Création d'une poutre (Wire).")
    part_name = names['part_tower']
    h = param['h_tower']
    
    # 1. Création de la Part (Espace 3D, Deformable)
    p = model.Part(name=part_name, dimensionality=THREE_D, type=DEFORMABLE_BODY)
    
    # 2. Dessin de la ligne (Wire)
    # De (0,0,0) à (0, h, 0)
    p.WirePolyLine(points=[((0.0, 0.0, 0.0), (0.0, h, 0.0))], mergeType=IMPRINT, meshable=ON)
    
    # 3. Création du Set pour l'assignation de section
    # On sélectionne l'unique arête créée
    edge = p.edges.findAt(((0.0, h/2.0, 0.0),))
    p.Set(name='Set_Beam_All', edges=edge)
    
    return p

def create_tower_3d(model, params, names):
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

def create_tower(model, param, names):
    """
    Fonction principale (Aiguilleur).
    Appelle la version 1D ou 3D selon le paramètre.
    """
    part_name = names['part_tower']
    
    # Nettoyage préventif
    if part_name in model.parts:
        del model.parts[part_name]

    print(f"\n--- Création Part Tour (Type: {param['dim_tour']}) ---")

    # L'AIGUILLAGE EST ICI
    if param['dim_tour'] == '1D':
        return create_tower_1d(model, param, names)
    else:
        return create_tower_3d(model, param, names)


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

def create_monitor_point_top(model, names, inst_tower, h_total, dim_type):
    """
    Crée un POINT unique pour le monitoring.
    - En 1D : Utilise le sommet de la poutre (Vertex).
    - En 3D : Crée un Point de Référence (RP) au centre + Couplage avec le bord.
    
    Retourne True si succès, False si échec (permet de continuer sans planter).
    """
    print(f"\n--- Création du Point de Monitoring (Cible : Y={h_total:.2f}m) ---")
    a = model.rootAssembly
    set_name = names['set_monitor']
    
    # Nettoyage préventif (Set, RP, Coupling précédents)
    if set_name in a.sets: del a.sets[set_name]
    if 'RP_Monitor_Top' in a.features: del a.features['RP_Monitor_Top']
    if 'Cpl_Monitor_Top' in model.constraints: del model.constraints['Cpl_Monitor_Top']

    try:
        # --- CAS 1 : MODE 1D (La tour est déjà une ligne) ---
        if dim_type == '1D':
            # On cherche le sommet (Vertex)
            verts = inst_tower.vertices.getByBoundingBox(
                yMin=h_total - 0.05, yMax=h_total + 0.05,
                xMin=-0.5, xMax=0.5, zMin=-0.5, zMax=0.5
            )
            
            if len(verts) > 0:
                a.Set(name=set_name, vertices=verts)
                print(f"   -> [SUCCÈS 1D] Point de suivi créé sur le sommet de la poutre.")
                return True
            else:
                print(f"   -> [ATTENTION] Sommet de poutre introuvable à Y={h_total}.")
                return False

        # --- CAS 2 : MODE 3D (La tour est un tube) ---
        else:
            # A. On cherche le bord supérieur (Cercle d'arêtes)
            edges = inst_tower.edges.getByBoundingBox(
                yMin=h_total - 0.05, yMax=h_total + 0.05
            )
            
            if len(edges) == 0:
                print(f"   -> [ATTENTION] Bord supérieur introuvable à Y={h_total}.")
                return False

            # B. Création d'un Point de Référence (RP) au centre du cercle
            rp_feat = a.ReferencePoint(point=(0.0, h_total, 0.0))
            a.features.changeKey(fromName=rp_feat.name, toName='RP_Monitor_Top')
            
            # Récupération de l'objet géométrique RP pour le Set
            # (L'ID du RP est accessible via l'attribut .id de la feature créée)
            rp_id = a.features['RP_Monitor_Top'].id
            rp_geo = a.referencePoints[rp_id]
            
            # C. Création du Set sur ce RP
            region_rp = a.Set(name=set_name, referencePoints=(rp_geo,))
            
            # D. Création du Couplage (Le RP suit le mouvement moyen du tube)
            # Surface esclave = le bord du tube
            surf_name = 'Surf_Monitor_Edges'
            a.Surface(name=surf_name, side1Edges=edges)
            
            model.Coupling(name='Cpl_Monitor_Top', 
                           controlPoint=region_rp, 
                           surface=a.surfaces[surf_name], 
                           couplingType=KINEMATIC, # Ou CONTINUUM si on veut moins rigidifier
                           influenceRadius=WHOLE_SURFACE,
                           u1=ON, u2=ON, u3=ON)
            
            print(f"   -> [SUCCÈS 3D] Point de Référence (RP) créé et couplé au sommet.")
            return True

    except Exception as e:
        print(f"   -> [ERREUR NON BLOQUANTE] Echec création point monitoring : {e}")
        return False    


def create_monitor_point_GBS(model, names, params, h_monitor):
    """
    Crée un point de monitoring sur la face INTERNE du GBS à une hauteur h_monitor.
    Méthode : Partitionne la Part GBS pour créer un sommet (Vertex) exact à cette hauteur.
    """
    print(f"\n--- Création Point Monitoring GBS (Interne, Y={h_monitor:.2f}m) ---")
    
    # 1. Récupération des objets
    part_name = names['part_gbs']
    inst_name = names['inst_gbs']
    set_name = names['set_monitor']
    
    p = model.parts[part_name]
    a = model.rootAssembly
    
    # 2. Partitionnement de la Pièce (Part)
    # On crée un plan de coupe horizontal à Y = h_monitor
    # Cela garantit qu'il y aura des noeuds à cette hauteur exacte.
    
    # On vérifie si la partition existe déjà pour ne pas la refaire 50 fois
    feature_name = f'Partition_Monitor_{int(h_monitor)}m'
    if feature_name not in p.features:
        try:
            datum_id = p.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=h_monitor).id
            p.PartitionCellByDatumPlane(datumPlane=p.datums[datum_id], cells=p.cells)
            # On renomme la feature pour la retrouver
            p.features.changeKey(fromName=p.features.keys()[-1], toName=feature_name)
            print("   -> Partition créée sur le GBS (Part).")
            
            # Il faut régénérer l'assemblage pour que la partition apparaisse sur l'instance
            a.regenerate()
        except Exception as e:
            print(f"   -> Info: Partition non créée (déjà existante ou erreur): {e}")

    # 3. Calcul du Rayon Interne Cible (Géométrie Analytique)
    # On doit savoir où cliquer (quel rayon ?) pour trouver la face interne.
    
    h_plat = params['plateau_height']
    h_cone = params['cone_height']
    
    # Rayons du cone
    r_ext_bot = params['cone_bottom_outer_radius']
    r_ext_top = params['cone_top_outer_radius']
    t_cone = params['cone_thickness']
    r_int_bot = r_ext_bot - t_cone
    r_int_top = r_ext_top - t_cone
    
    r_target = 0.0
    
    if h_monitor < h_plat:
        print("   ERREUR : h_monitor est dans le plateau (pas de face interne).")
        return False
        
    elif h_monitor <= (h_plat + h_cone):
        # On est dans le cône : Interpolation linéaire
        h_local = h_monitor - h_plat
        ratio = h_local / h_cone
        r_target = r_int_bot + (r_int_top - r_int_bot) * ratio
        print(f"   -> Zone Cône : Rayon interne calculé = {r_target:.3f} m")
        
    else:
        # On est dans le cylindre supérieur (Rayon constant)
        r_target = r_int_top
        print(f"   -> Zone Cylindre : Rayon interne constant = {r_target:.3f} m")

    # 4. Sélection du Vertex sur l'Instance
    # On cherche le point à (r_target, h_monitor, 0.0)
    # On utilise une petite boîte de tolérance
    
    inst = a.instances[inst_name]
    
    verts = inst.vertices.getByBoundingBox(
        xMin=r_target - 0.1, xMax=r_target + 0.1,
        yMin=h_monitor - 0.01, yMax=h_monitor + 0.01,
        zMin=-0.1, zMax=0.1 # On cherche sur l'axe X (Z~0)
    )
    
    # Nettoyage ancien set
    if set_name in a.sets: del a.sets[set_name]

    if len(verts) > 0:
        a.Set(name=set_name, vertices=verts)
        print(f"   -> [SUCCÈS] Point de monitoring GBS créé à R={r_target:.2f}, Y={h_monitor}.")
        return True
    else:
        print(f"   -> [ECHEC] Aucun vertex trouvé à R={r_target:.2f}, Y={h_monitor}.")
        print("      Vérifiez que h_monitor ne tombe pas dans le vide.")
        return False