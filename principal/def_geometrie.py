# -*- coding: utf-8 -*-
# =============================================================================
# FICHIER : def_geometrie.py
# DESCRIPTION : Contient toutes les fonctions nécessaires pour générer la 
#               géométrie, l'assemblage et les surfaces du modèle (GBS + Tour).
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
    Fonction de nettoyage robuste.
    Elle supprime des objets (Parts, Sketches, Instances) seulement s'ils existent,
    pour éviter de faire planter le script avec une 'KeyError'.
    
    Args:
        model : L'objet modèle Abaqus (mdb.models['Model-1'])
        object_names (list) : Liste des noms à supprimer (ex: ['Tower', 'GBS'])
        object_type (str) : Type d'objet ('Part', 'Sketch', 'Instance')
    """
    for name in object_names:
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
    Analyse les dimensions fournies par l'utilisateur avant de lancer la modélisation.
    Le but est d'empêcher la création de géométries impossibles (ex: épaisseurs négatives)
    ou incohérentes pour l'assemblage (ex: la Tour qui tombe dans le trou du GBS).
    """
    print("--- Vérification des paramètres géométriques ---")
    
    # --- A. Vérifications de base (Valeurs positives) ---
    required_positive = [
        'cone_thickness', 'cone_top_outer_radius', 'plateau_radius', 
        'plateau_height', 'cyl_height', 'thickness_tower', 'h_tower'
    ]
    
    for key in required_positive:
        if params[key] <= 0:
            raise ValueError(f"Erreur paramètre : '{key}' doit être strictement positif.")

    if params['cone_bottom_outer_radius'] <= params['cone_thickness']:
        raise ValueError("Le rayon bas du cône est trop petit par rapport à son épaisseur.")

    # --- B. Vérification de l'Interface Tour / GBS (CRITIQUE) ---
    # Pour que le 'Tie' (collage) fonctionne, la tour doit reposer sur du béton, pas dans le vide.
    
    r_gbs_ext = params['cone_top_outer_radius']           # Bord extérieur du sommet GBS
    r_gbs_hole = r_gbs_ext - params['cone_thickness']     # Bord du trou intérieur
    r_tower_bot = params['r_down_tower']                  # Rayon de la base de la tour

    # Cas 1 : La tour est plus petite que le trou -> Elle tombe dedans
    if r_tower_bot <= r_gbs_hole:
        raise ValueError(
            f"\nERREUR GÉOMÉTRIQUE CRITIQUE :\n"
            f"La base de la tour (R={r_tower_bot}) est plus petite que le trou du GBS (R={r_gbs_hole}).\n"
            f"Cela rend l'assemblage impossible (pas de contact).\n"
            f"-> SOLUTION : Augmentez 'r_down_tower' (ex: {r_gbs_hole + 0.25})."
        )

    # Cas 2 : La tour est plus large que le GBS -> Elle flotte dans le vide extérieur
    if r_tower_bot > r_gbs_ext:
        raise ValueError(
            f"\nERREUR GÉOMÉTRIQUE :\n"
            f"La base de la tour (R={r_tower_bot}) dépasse la largeur du sommet GBS (R={r_gbs_ext}).\n"
            f"-> SOLUTION : Réduisez 'r_down_tower'."
        )

    print("✅ Paramètres valides : Géométrie cohérente.")


# =============================================================================
# 3. CRÉATION DE LA TOUR (Partie Acier)
# =============================================================================

def create_tower(model, params):
    """
    Génère la pièce 'Tower' par révolution.
    Gère automatiquement la création d'un tube creux via une opération booléenne (Cut).
    
    Returns:
        final_part (Part object) : La pièce finale créée.
    """
    # Récupération des données
    r_up = params['r_up_tower']
    r_down = params['r_down_tower']
    h = params['h_tower']
    t = params['thickness_tower']
    
    a = model.rootAssembly
    sheetSize = max(r_down, h) * 3.0

    # --- Fonction interne pour dessiner un cône plein ---
    def create_revolve_part(part_name, r_bot, r_top, height):
        # 1. Préparation Sketch
        sketch_name = f'__profile_{part_name}__'
        clean_features(model, [sketch_name], 'Sketch')
        
        model.ConstrainedSketch(name=sketch_name, sheetSize=sheetSize)
        s = model.sketches[sketch_name]
        s.ConstructionLine(point1=(0, -sheetSize), point2=(0, sheetSize)) # Axe de révolution
        
        # 2. Dessin du trapèze (profil)
        s.Line(point1=(0, 0), point2=(r_bot, 0))       
        s.Line(point1=(r_bot, 0), point2=(r_top, height)) 
        s.Line(point1=(r_top, height), point2=(0, height)) 
        s.Line(point1=(0, height), point2=(0, 0))       

        # 3. Révolution 360°
        clean_features(model, [part_name], 'Part')
        p = model.Part(name=part_name, dimensionality=THREE_D, type=DEFORMABLE_BODY)
        p.BaseSolidRevolve(angle=360.0, sketch=s)
        del model.sketches[sketch_name]
        return p

    # --- Logique Principale : Creux ou Plein ? ---
    r_up_in = r_up - t
    r_down_in = r_down - t
    is_hollow = (r_up_in > 0 and r_down_in > 0)

    if not is_hollow:
        # Si c'est plein, on crée directement la pièce finale
        final_part = create_revolve_part('Tower', r_down, r_up, h)
    else:
        # Si c'est creux, on doit soustraire un cône intérieur à un cône extérieur
        
        # 1. Création des formes temporaires
        part_outer = create_revolve_part('Tower_Outer_Temp', r_down, r_up, h)
        part_inner = create_revolve_part('Tower_Inner_Temp', r_down_in, r_up_in, h)

        # 2. Instanciation temporaire (nécessaire pour l'opération booléenne)
        clean_features(model, ['inst_out', 'inst_in'], 'Instance')
        inst_outer = a.Instance(name='inst_out', part=part_outer, dependent=ON)
        inst_inner = a.Instance(name='inst_in', part=part_inner, dependent=ON)

        # 3. Coupe Booléenne (Outer - Inner)
        # Cela crée une nouvelle Part nommée 'Tower' dans la bibliothèque
        clean_features(model, ['Tower'], 'Part')
        a.InstanceFromBooleanCut(
            name='Tower', 
            instanceToBeCut=inst_outer, 
            cuttingInstances=(inst_inner, ),
            originalInstances=SUPPRESS
        )
        final_part = model.parts['Tower']

        # 4. Nettoyage des objets temporaires
        # InstanceFromBooleanCut crée une instance 'Tower-1', on la supprime pour garder l'assemblage propre
        if 'Tower-1' in a.instances: del a.instances['Tower-1']
        clean_features(model, ['inst_out', 'inst_in'], 'Instance')
        clean_features(model, ['Tower_Outer_Temp', 'Tower_Inner_Temp'], 'Part')

    # --- Création de la Surface Latérale (Pour le chargement vent/houle) ---
    # On cherche une face située au milieu de la hauteur et du rayon moyen
    mid_h = h / 2.0
    mid_r = (r_down + r_up) / 2.0
    target_point = (mid_r, mid_h, 0.0)
    
    faces_ext = final_part.faces.findAt((target_point, ))
    
    if len(faces_ext) == 0:
        raise Exception(f"Erreur critique : Impossible de trouver la surface externe de la tour au point {target_point}")

    final_part.Surface(name='Tower_Lateral_Surface', side1Faces=faces_ext)
    
    print("-> Pièce 'Tower' créée avec succès.")
    return final_part


# =============================================================================
# 4. CRÉATION DU GBS (Partie Béton)
# =============================================================================

def create_fused_gbs(model, params):
    """
    Construit le GBS en assemblant 3 formes primitives (Plateau, Cône, Cylindre)
    puis les fusionne en une seule pièce monolithique pour faciliter le maillage.
    """
    # Récupération dimensions
    h_plateau = params['plateau_height']
    r_plateau = params['plateau_radius']
    h_cone = params['cone_height']
    t_cone = params['cone_thickness']
    # Rayons extérieurs
    r_ext_bot = params['cone_bottom_outer_radius']
    r_ext_top = params['cone_top_outer_radius']
    # Rayons intérieurs (pour le creux)
    r_int_bot = r_ext_bot - t_cone
    r_int_top = r_ext_top - t_cone
    
    h_cyl = params['cyl_height']
    
    a = model.rootAssembly
    sheetSize = max(r_plateau, h_cone + h_cyl) * 2.5

    # --- Étape A : Création des 3 parties temporaires ---
    
    # 1. Plateau (Disque plein)
    clean_features(model, ['Plateau'], 'Part')
    model.ConstrainedSketch(name='__sketch_plat__', sheetSize=sheetSize)
    s = model.sketches['__sketch_plat__']
    s.ConstructionLine(point1=(0, -100), point2=(0, 100))
    s.Line(point1=(0, 0), point2=(r_plateau, 0))
    s.Line(point1=(r_plateau, 0), point2=(r_plateau, h_plateau))
    s.Line(point1=(r_plateau, h_plateau), point2=(0, h_plateau))
    s.Line(point1=(0, h_plateau), point2=(0, 0))
    p_plat = model.Part(name='Plateau', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    p_plat.BaseSolidRevolve(angle=360.0, sketch=s)

    # 2. Cône (Trapèze creux)
    clean_features(model, ['Cone'], 'Part')
    model.ConstrainedSketch(name='__sketch_cone__', sheetSize=sheetSize)
    s = model.sketches['__sketch_cone__']
    s.ConstructionLine(point1=(0, -100), point2=(0, 100))
    s.Line(point1=(r_ext_bot, 0), point2=(r_ext_top, h_cone))
    s.Line(point1=(r_ext_top, h_cone), point2=(r_int_top, h_cone))
    s.Line(point1=(r_int_top, h_cone), point2=(r_int_bot, 0))
    s.Line(point1=(r_int_bot, 0), point2=(r_ext_bot, 0))
    p_cone = model.Part(name='Cone', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    p_cone.BaseSolidRevolve(angle=360.0, sketch=s)

    # 3. Cylindre Supérieur (Tube creux)
    clean_features(model, ['Cyl_Haut'], 'Part')
    model.ConstrainedSketch(name='__sketch_cyl__', sheetSize=sheetSize)
    s = model.sketches['__sketch_cyl__']
    s.ConstructionLine(point1=(0, -100), point2=(0, 100))
    s.Line(point1=(r_ext_top, 0), point2=(r_ext_top, h_cyl))
    s.Line(point1=(r_int_top, h_cyl), point2=(r_ext_top, h_cyl)) # Fermeture haut
    s.Line(point1=(r_int_top, 0), point2=(r_int_top, h_cyl))
    s.Line(point1=(r_int_top, 0), point2=(r_ext_top, 0))
    p_cyl = model.Part(name='Cyl_Haut', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    p_cyl.BaseSolidRevolve(angle=360.0, sketch=s)
    
    # Nettoyage sketches
    for k in ['__sketch_plat__', '__sketch_cone__', '__sketch_cyl__']:
        if k in model.sketches: del model.sketches[k]

    # --- Étape B : Assemblage Temporaire ---
    clean_features(model, ['Plateau-1', 'Cone-1', 'Cyl_Haut-1'], 'Instance')
    
    inst_plat = a.Instance(name='Plateau-1', part=p_plat, dependent=ON)
    
    inst_cone = a.Instance(name='Cone-1', part=p_cone, dependent=ON)
    a.translate(instanceList=('Cone-1',), vector=(0.0, h_plateau, 0.0))
    
    inst_cyl = a.Instance(name='Cyl_Haut-1', part=p_cyl, dependent=ON)
    a.translate(instanceList=('Cyl_Haut-1',), vector=(0.0, h_plateau + h_cone, 0.0))

    # --- Étape C : Fusion (Merge) ---
    clean_features(model, ['GBS_Fused'], 'Part')
    
    a.InstanceFromBooleanMerge(
        name='GBS_Fused',
        instances=(inst_plat, inst_cone, inst_cyl),
        keepIntersections=True,   # Garde les frontières internes (utile pour le maillage)
        originalInstances=SUPPRESS,
        domain=GEOMETRY
    )
    
    gbs_part = model.parts['GBS_Fused']

    # --- Étape D : Surface Extérieure (Complexe car multi-faces) ---
    # On définit un point cible sur chaque composant pour capturer toutes les faces
    pts = [
        (r_plateau, h_plateau/2.0, 0.0),                        # Flanc plateau
        ((r_ext_bot+r_ext_top)/2.0, h_plateau + h_cone/2.0, 0.0), # Flanc cône
        (r_ext_top, h_plateau + h_cone + h_cyl/2.0, 0.0)        # Flanc cylindre
    ]
    
    faces_list = []
    for pt in pts:
        found = gbs_part.faces.findAt((pt, ))
        if len(found) > 0:
            faces_list.append(found[0]) # On ajoute la face trouvée
            
    if not faces_list:
        print("ATTENTION : Aucune face extérieure trouvée pour le GBS.")
    else:
        # On crée une séquence de faces unique pour créer la surface
        # Note : findAt retourne des objets, on peut les concaténer mais c'est délicat.
        # L'approche robuste est de refaire un findAt global
        all_found = gbs_part.faces.findAt(*[(p,) for p in pts])
        gbs_part.Surface(name='GBS_Outer_Surface', side1Faces=all_found)

    # --- Étape E : Nettoyage Final ---
    clean_features(model, ['Plateau', 'Cone', 'Cyl_Haut'], 'Part')
    
    print("-> Pièce 'GBS_Fused' créée avec succès.")
    return gbs_part


# =============================================================================
# 5. ASSEMBLAGE FINAL (Positionnement)
# =============================================================================

def create_assembly_geometry(model, tower_part_name, gbs_part_name, h_pipe_bottom, h_gbs_top):
    """
    Crée les instances finales dans l'assemblage et les positionne.
    Utilise le mode 'Dependent=ON' pour hériter du maillage fait sur les Parts.
    """
    a = model.rootAssembly
    
    # 1. Nettoyage de l'assemblage (pour repartir de zéro)
    # On supprime toutes les instances existantes et les features (Couplings, RPs...)
    if hasattr(a, 'instances'):
        for k in list(a.instances.keys()): del a.instances[k]
    if hasattr(a, 'features'):
        # On garde les systèmes de coordonnées par défaut (3 premiers features généralement)
        # Mais pour être sûr, on supprime tout sauf les Datums de base
        pass 
        # Note : deleteFeatures est radical, à utiliser avec précaution. 
        # Ici on se contente souvent de supprimer les instances.

    # 2. Création des Instances Dépendantes
    print("--- Création des Instances (Mode Dépendant) ---")
    p_gbs = model.parts[gbs_part_name]
    p_tower = model.parts[tower_part_name]
    
    inst_gbs = a.Instance(name='GBS-1', part=p_gbs, dependent=ON)
    inst_tower = a.Instance(name='Tower-1', part=p_tower, dependent=ON)

    # 3. Positionnement (Translation verticale de la tour)
    # La tour est créée à Y=0, on la monte au sommet du GBS
    dy = h_gbs_top - h_pipe_bottom
    if dy != 0:
        a.translate(instanceList=(inst_tower.name, ), vector=(0.0, dy, 0.0))
        print(f"-> Tour translatée de DY = {dy}")

    return inst_gbs, inst_tower


# =============================================================================
# 6. SURFACES GLOBALES (Pour le chargement)
# =============================================================================

def fus_outer_surfaces(model, inst_gbs, inst_tower):
    """
    Crée une surface unique 'Global_Outer_Surface' qui combine l'extérieur du GBS
    et l'extérieur de la Tour. Utile pour appliquer une pression hydrodynamique globale.
    
    Args:
        inst_gbs, inst_tower : Les OBJETS instances (et non pas leurs noms string).
                               Cela rend la fonction indépendante du nom 'GBS-1' ou 'GBS-2'.
    """
    a = model.rootAssembly
    
    # Noms des surfaces définis dans les fonctions de création de part
    name_surf_gbs = 'GBS_Outer_Surface'
    name_surf_tower = 'Tower_Lateral_Surface'
    
    # Vérification d'existence
    if name_surf_gbs not in inst_gbs.surfaces:
        raise KeyError(f"Surface '{name_surf_gbs}' introuvable sur l'instance GBS.")
    if name_surf_tower not in inst_tower.surfaces:
        raise KeyError(f"Surface '{name_surf_tower}' introuvable sur l'instance Tour.")

    # Récupération des objets surfaces
    s1 = inst_gbs.surfaces[name_surf_gbs]
    s2 = inst_tower.surfaces[name_surf_tower]

    # Opération Booléenne (Union)
    # Cette surface est stockée au niveau de l'Assembly
    a.SurfaceByBoolean(
        name='Global_Outer_Surface',
        surfaces=(s1, s2),
        operation=UNION
    )
    print("-> Surface fusionnée 'Global_Outer_Surface' créée.")

def create_hydro_surface_robust(model, inst_gbs, inst_tower, h_mer):
    """
    Crée la surface d'application des forces hydrodynamiques de manière ROBUSTE.
    Méthode : Intersection entre la surface extérieure connue (Part) et une boîte de sélection en hauteur.
    
    Garantie : Aucune face intérieure ne peut être sélectionnée.
    """
    print(f"--- Création Surface Hydro (Intersection Booléenne > {h_mer}m) ---")
    a = model.rootAssembly
    
    # ---------------------------------------------------------
    # 1. Récupération des Surfaces Extérieures PROPRES (Définies dans les Parts)
    # ---------------------------------------------------------
    # Ces surfaces existent déjà et sont saines (ne contiennent que la peau ext.)
    try:
        s_clean_gbs = inst_gbs.surfaces['GBS_Outer_Surface']
        s_clean_tower = inst_tower.surfaces['Tower_Lateral_Surface']
    except KeyError:
        raise KeyError("Les surfaces 'GBS_Outer_Surface' ou 'Tower_Lateral_Surface' n'existent pas sur les instances. Vérifiez create_tower et create_fused_gbs.")

    # On crée une surface temporaire qui contient TOUT l'extérieur (Haut + Bas)
    surf_total_clean_name = '__Temp_Outer_All__'
    if surf_total_clean_name in a.surfaces: del a.surfaces[surf_total_clean_name]
    
    s_total_clean = a.SurfaceByBoolean(
        name=surf_total_clean_name,
        surfaces=(s_clean_gbs, s_clean_tower),
        operation=UNION
    )

    # ---------------------------------------------------------
    # 2. Sélection de la ZONE DE HAUTEUR (Sale)
    # ---------------------------------------------------------
    # On prend TOUTES les faces au-dessus de h_mer (Intérieur + Extérieur)
    # On y va "à la louche" avec une bounding box géante
    faces_zone_gbs = inst_gbs.faces.getByBoundingBox(yMin=h_mer - 0.01, yMax=9999.0)
    faces_zone_tower = inst_tower.faces.getByBoundingBox(yMin=h_mer - 0.01, yMax=9999.0)
    
    if len(faces_zone_gbs) == 0 and len(faces_zone_tower) == 0:
        raise ValueError(f"Aucune face trouvée au-dessus de {h_mer}m !")

    # On crée une surface temporaire "Zone" (qui contient aussi l'intérieur du tube, ce qu'on ne veut pas)
    surf_zone_name = '__Temp_Zone_Height__'
    # Astuce : Pour créer une surface à partir de listes de faces de deux instances, 
    # il faut passer par une séquence unique ou deux surfaces temp.
    # Ici on fait simple : 2 surfaces temp puis Union.
    
    surfs_to_merge = []
    if len(faces_zone_gbs) > 0:
        surfs_to_merge.append(a.Surface(name='__T1__', side1Faces=faces_zone_gbs))
    if len(faces_zone_tower) > 0:
        surfs_to_merge.append(a.Surface(name='__T2__', side1Faces=faces_zone_tower))
        
    if len(surfs_to_merge) == 1:
        s_zone_height = surfs_to_merge[0]
    else:
        s_zone_height = a.SurfaceByBoolean(name=surf_zone_name, surfaces=tuple(surfs_to_merge), operation=UNION)

    # ---------------------------------------------------------
    # 3. L'INTERSECTION MAGIQUE (Le Filtre)
    # ---------------------------------------------------------
    # On garde seulement ce qui est à la fois "Propre" ET "Dans la zone"
    
    final_name = 'Global_Outer_Surface'
    # Suppression préventive
    if final_name in a.surfaces: del a.surfaces[final_name]
    
    a.SurfaceByBoolean(
        name=final_name,
        surfaces=(s_total_clean, s_zone_height),
        operation=INTERSECTION
    )
    
    # ---------------------------------------------------------
    # 4. Nettoyage des surfaces temporaires
    # ---------------------------------------------------------
    # On supprime les surfaces intermédiaires pour ne pas polluer l'arbre
    temp_names = [surf_total_clean_name, surf_zone_name, '__T1__', '__T2__']
    for name in temp_names:
        if name in a.surfaces: del a.surfaces[name]

    print(f"-> Surface '{final_name}' créée par Intersection Booléenne (Sûre à 100%).")
