
from abaqus import mdb
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup

from math import pi
import numpy as np
import regionToolset

# =============================================================================
# 2. Paramètres
# =============================================================================
param_geom = {
    # Tower
    'r_up_tower': 1.0,
    'r_down_tower': 3.0,
    'h_tower': 50.0,
    'thickness_tower': 0.5,

    # Plateau (solid)
    'plateau_radius': 15.5,
    'plateau_height': 1.7,

    # Cône GBS (hollow)
    'cone_height': 25.34,
    'cone_top_outer_radius': 3.5,
    'cone_bottom_outer_radius': 10.0,
    'cone_thickness': 0.5,

    # Cylindre au-dessus du cône
    'cyl_height': 18.0,
}

# =============================================================================
# 3. Vérification des paramètres
# =============================================================================

def check_parameters(params):
    if params['cone_thickness'] <= 0:
        raise ValueError("Cone thickness must be positive.")
    if params['cone_top_outer_radius'] <= 0:
        raise ValueError("Cone top outer radius must be positive.")
    if params['cone_bottom_outer_radius'] <= params['cone_thickness']:
        raise ValueError("Cone bottom radius must be larger than thickness.")
    if params['plateau_radius'] <= 0 or params['plateau_height'] <= 0:
        raise ValueError("Plateau dimensions must be positive.")
    if params['cyl_height'] <= 0:
        raise ValueError("Cylinder height must be positive.")
    if params['r_up_tower'] >= params['cone_top_outer_radius']:
        raise ValueError("Tower upper radius must be smaller than GBS top outer radius.")
    if params['r_down_tower'] > params['cone_top_outer_radius']:
        raise ValueError("Tower lower radius must be smaller or equal to GBS top outer radius.")
    if params['thickness_tower'] <= 0:
        raise ValueError("Pipe thickness must be positive.")

# =============================================================================
# 5. Fonction de création du mât
# =============================================================================

def create_tower(model, params):
    """
    Crée une tour (Part) et sa surface extérieure.
    Gère les versions pleines ou creuses.
    
    Returns:
        final_part (Part object) : L'objet Part final (unique).
    """
    # 1. Paramètres
    r_up = params['r_up_tower']
    r_down = params['r_down_tower']
    h = params['h_tower']
    t = params['thickness_tower']

    if r_up <= 0 or r_down <= 0 or h <= 0:
        raise ValueError("Dimensions invalides (doivent être > 0).")

    a = model.rootAssembly
    sheetSize = max(r_down, h) * 3.0

    # ---------------------------------------------------------
    # Fonction interne : Sketch + Revolve
    # ---------------------------------------------------------
    def create_revolve_part(part_name, r_bot, r_top, height):
        # Nettoyage préventif si le sketch existe
        sketch_name = '__profile_' + part_name + '__'
        if sketch_name in model.sketches:
            del model.sketches[sketch_name]

        model.ConstrainedSketch(name=sketch_name, sheetSize=sheetSize)
        s = model.sketches[sketch_name]
        s.ConstructionLine(point1=(0, -sheetSize), point2=(0, sheetSize))
        
        s.Line(point1=(0, 0), point2=(r_bot, 0))       
        s.Line(point1=(r_bot, 0), point2=(r_top, height)) 
        s.Line(point1=(r_top, height), point2=(0, height)) 
        s.Line(point1=(0, height), point2=(0, 0))       

        # Si la part existe déjà, on la supprime pour éviter les erreurs
        if part_name in model.parts:
            del model.parts[part_name]

        p = model.Part(name=part_name, dimensionality=THREE_D, type=DEFORMABLE_BODY)
        p.BaseSolidRevolve(angle=360.0, sketch=s)
        del model.sketches[sketch_name]
        return p

    # ---------------------------------------------------------
    # Logique de création
    # ---------------------------------------------------------
    
    # 1. Création de l'enveloppe extérieure
    # On lui donne déjà le nom final 'Tower' si c'est plein, sinon un nom temp
    r_up_in = r_up - t
    r_down_in = r_down - t
    is_hollow = (r_up_in > 0 and r_down_in > 0)

    if not is_hollow:
        # CAS PLEIN : C'est simple
        final_part = create_revolve_part('Tower', r_down, r_up, h)
    
    else:
        # CAS CREUX : On passe par l'assemblage pour couper
        part_outer = create_revolve_part('Tower_Outer_Temp', r_down, r_up, h)
        part_inner = create_revolve_part('Tower_Inner_Temp', r_down_in, r_up_in, h)

        # Instanciation temporaire
        inst_outer = a.Instance(name='inst_out', part=part_outer, dependent=ON)
        inst_inner = a.Instance(name='inst_in', part=part_inner, dependent=ON)

        # CORRECTION DE L'ERREUR ICI :
        # On utilise InstanceFromBooleanCut (méthode de l'Assembly).
        # Cela crée une NOUVELLE Part dans model.parts nommée 'Tower'
        a.InstanceFromBooleanCut(
            name='Tower', 
            instanceToBeCut=inst_outer, 
            cuttingInstances=(inst_inner, ),
            originalInstances=SUPPRESS
        )
        
        # On récupère l'objet Part qui vient d'être créé
        final_part = model.parts['Tower']

        # Nettoyage propre (suppression des instances temp et parts temp)
        del a.features['Tower-1'] # InstanceFromBooleanCut crée une instance, on la vire
        del a.instances['inst_out']
        del a.instances['inst_in']
        del model.parts['Tower_Outer_Temp']
        del model.parts['Tower_Inner_Temp']

    # ---------------------------------------------------------
    # Création de la Surface (Sur la pièce finale propre)
    # ---------------------------------------------------------
    mid_h = h / 2.0
    mid_r = (r_down + r_up) / 2.0
    # Coordonnée cible sur la face externe (X=Rayon, Y=Hauteur, Z=0)
    target_point = (mid_r, mid_h, 0.0)
    
    faces_ext = final_part.faces.findAt((target_point, ))
    
    # Création de la surface directement dans la Part
    final_part.Surface(name='Tower_Lateral_Surface', side1Faces=faces_ext)

    return final_part
# =============================================================================
# 6. Fonction de création du GBS fusionné
# =============================================================================
def create_fused_gbs(model, params):
    """
    Crée une structure GBS fusionnée avec:
        1. Plateau solide
        2. Cône creux
        3. Cylindre creux au-dessus du cône
    Puis fusionne toutes les parties en un seul solide et crée la surface extérieure.

    Args:
        model: Modèle Abaqus
        params: Dictionnaire de paramètres géométriques

    Returns:
        Part: Pièce GBS fusionnée
    """
    # -------------------------------
    # 1. Récupération et Calcul des Paramètres
    # -------------------------------
    h_plateau = params['plateau_height']
    r_plateau = params['plateau_radius']

    h_cone = params['cone_height']
    r_ext_top_cone = params['cone_top_outer_radius']
    r_ext_bottom_cone = params['cone_bottom_outer_radius']
    t_cone = params['cone_thickness']
    r_int_top_cone = r_ext_top_cone - t_cone
    r_int_bottom_cone = r_ext_bottom_cone - t_cone

    h_cyl = params['cyl_height']
    r_ext_cyl_top = r_ext_top_cone # Le cylindre suit le haut du cône
    r_int_cyl_top = r_ext_cyl_top - t_cone

    # Altitudes (Coordonnées Y)
    y0 = 0.0
    y1 = y0 + h_plateau
    y2 = y1 + h_cone
    y3 = y2 + h_cyl

    # Taille de la feuille de dessin
    max_radius = max(r_plateau, r_ext_bottom_cone, r_ext_cyl_top)
    max_height = y3
    sheetSize = max(max_radius, max_height) * 2.5

    a = model.rootAssembly
    a.DatumCsysByDefault(CARTESIAN)

    # -------------------------------
    # 2. Création des Parts Temporaires
    # -------------------------------

    # --- A. Plateau solide ---
    model.ConstrainedSketch(name='__sketch_plateau__', sheetSize=sheetSize)
    s = model.sketches['__sketch_plateau__']
    s.ConstructionLine(point1=(0, -sheetSize), point2=(0, sheetSize))
    # Profil rectangle plein
    s.Line(point1=(0, y0), point2=(r_plateau, y0))
    s.Line(point1=(r_plateau, y0), point2=(r_plateau, y1))
    s.Line(point1=(r_plateau, y1), point2=(0, y1))
    s.Line(point1=(0, y1), point2=(0, y0))
    plateau = model.Part(name='Plateau', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    plateau.BaseSolidRevolve(angle=360.0, sketch=s)
    del model.sketches['__sketch_plateau__']

    # --- B. Cône creux ---
    model.ConstrainedSketch(name='__sketch_cone__', sheetSize=sheetSize)
    s = model.sketches['__sketch_cone__']
    s.ConstructionLine(point1=(0, -sheetSize), point2=(0, sheetSize))
    # Profil trapézoïdal creux
    s.Line(point1=(r_ext_bottom_cone, 0), point2=(r_ext_top_cone, h_cone))
    s.Line(point1=(r_int_top_cone, h_cone), point2=(r_int_bottom_cone, 0))
    s.Line(point1=(r_ext_top_cone, h_cone), point2=(r_int_top_cone, h_cone))
    s.Line(point1=(r_ext_bottom_cone, 0), point2=(r_int_bottom_cone, 0))
    cone = model.Part(name='Cone_Creux', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    cone.BaseSolidRevolve(angle=360.0, sketch=s)
    del model.sketches['__sketch_cone__']

    # --- C. Cylindre supérieur creux ---
    model.ConstrainedSketch(name='__sketch_cyl__', sheetSize=sheetSize)
    s = model.sketches['__sketch_cyl__']
    s.ConstructionLine(point1=(0, -sheetSize), point2=(0, sheetSize))
    # Profil rectangle creux
    s.Line(point1=(r_ext_cyl_top, 0), point2=(r_ext_cyl_top, h_cyl))
    s.Line(point1=(r_int_cyl_top, 0), point2=(r_int_cyl_top, h_cyl))
    s.Line(point1=(r_int_cyl_top, h_cyl), point2=(r_ext_cyl_top, h_cyl))
    s.Line(point1=(r_int_cyl_top, 0), point2=(r_ext_cyl_top, 0))
    cyl_top = model.Part(name='Cyl_Haut', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    cyl_top.BaseSolidRevolve(angle=360.0, sketch=s)
    del model.sketches['__sketch_cyl__']

    # -------------------------------
    # 3. Assemblage et Positionnement
    # -------------------------------
    # On positionne les instances pour qu'elles s'empilent correctement
    a.Instance(name='Plateau-1', part=plateau, dependent=ON)
    
    a.Instance(name='Cone-1', part=cone, dependent=ON)
    a.translate(instanceList=('Cone-1',), vector=(0.0, h_plateau, 0.0))
    
    a.Instance(name='Cyl_Haut-1', part=cyl_top, dependent=ON)
    a.translate(instanceList=('Cyl_Haut-1',), vector=(0.0, y2, 0.0))

    # -------------------------------
    # 4. Fusion (Boolean Merge)
    # -------------------------------
    # Cette opération crée une nouvelle Part 'GBS_Fused' indépendante
    merged_part = a.InstanceFromBooleanMerge(
        name='GBS_Fused',
        instances=(a.instances['Plateau-1'], a.instances['Cone-1'], a.instances['Cyl_Haut-1']),
        keepIntersections=True,
        originalInstances=SUPPRESS,
        domain=GEOMETRY
    )
    
    # Récupération de l'objet Part réel depuis le modèle (plus sûr pour la suite)
    gbs_part = model.parts['GBS_Fused']

    # -------------------------------
    # 5. Création de la Surface Extérieure (Méthode findAt)
    # -------------------------------
    
    # Calcul des coordonnées cibles sur la peau extérieure (Z=0 par défaut dans le plan X-Y de révolution)
    # Point milieu sur le flanc du plateau
    pt_plateau = (r_plateau, y0 + h_plateau/2.0, 0.0)
    
    # Point milieu sur le flanc du cône
    # Rayon moyen entre bas et haut du cône
    r_mid_cone = (r_ext_bottom_cone + r_ext_top_cone) / 2.0
    # Hauteur moyenne du cône (absolue)
    y_mid_cone = y1 + h_cone/2.0
    pt_cone = (r_mid_cone, y_mid_cone, 0.0)
    
    # Point milieu sur le flanc du cylindre haut
    pt_cyl = (r_ext_cyl_top, y2 + h_cyl/2.0, 0.0)

    # Recherche des faces correspondantes
    # findAt prend une séquence de coordonnées et retourne les faces à ces endroits
    faces_to_select = gbs_part.faces.findAt(
        (pt_plateau, ),
        (pt_cone, ),
        (pt_cyl, )
    )

    # Création de la surface
    if len(faces_to_select) > 0:
        gbs_part.Surface(name='GBS_Outer_Surface', side1Faces=faces_to_select)
    else:
        print("Attention: Aucune face trouvée pour la surface extérieure GBS.")

    # -------------------------------
    # 6. Nettoyage
    # -------------------------------
    # Suppression des parts temporaires inutiles pour garder le fichier propre
    for part_name in ['Plateau', 'Cone_Creux', 'Cyl_Haut']:
        if part_name in model.parts:
            del model.parts[part_name]

    return gbs_part
# =============================================================================
# 7. Définition de l'Assembly 
# =============================================================================

# =============================================================================
# FONCTION 1 : GESTION DE LA GÉOMÉTRIE (INSTANCES + POSITION)
# =============================================================================
def create_assembly_geometry(model, tower_part_name, gbs_part_name, h_pipe_bottom, h_gbs_top):
    """
    Gère uniquement la mise en place des instances dans l'espace.
    Garantit le mode dependent=ON.
    """
    a = model.rootAssembly
    
    # 1. Nettoyage complet (pour éviter les conflits si on relance)
    # On supprime les features (RP, Couplings...) et les instances
    if hasattr(a, 'features'):
        a.deleteFeatures(a.features.keys())
    if hasattr(a, 'instances'):
        for i in list(a.instances.keys()): del a.instances[i]

    # 2. Création des instances (Le "Contrat de dépendance" est signé ici)
    # On utilise les noms de parts (str) pour récupérer les objets parts
    p_gbs = model.parts[gbs_part_name]
    p_tower = model.parts[tower_part_name]
    
    inst_gbs = a.Instance(name='GBS-1', part=p_gbs, dependent=ON)
    inst_tower = a.Instance(name='Tower-1', part=p_tower, dependent=ON)

    # 3. Positionnement (Translation)
    dy = h_gbs_top - h_pipe_bottom
    a.translate(instanceList=(inst_tower.name, ), vector=(0.0, dy, 0.0))
    
    print("Assemblage géométrique terminé.")
    return inst_gbs, inst_tower

# =============================================================================
# 7. Fusion des surfaces extérieures
# =============================================================================

def fus_outer_surfaces(model) :
    a = model.rootAssembly
    # Récupération des surfaces depuis les instances créées juste au-dessus
    surf_gbs = a.instances['GBS-1'].surfaces['GBS_Outer_Surface']
    surf_tower = a.instances['Tower-1'].surfaces['Tower_Lateral_Surface'] # Nom corrigé selon votre snippet

    # Création de la surface fusionnée "Global_Outer_Surface" par Union
    # Cette surface est stockée au niveau de l'assemblage (a.surfaces)
    a.SurfaceByBoolean(
        name='Global_Outer_Surface',
        surfaces=(surf_gbs, surf_tower),
        operation=UNION
    )