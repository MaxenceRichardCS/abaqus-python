# =============================================================================
# 1. Initialisation du modèle Abaqus
# =============================================================================
from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup
from abaqusConstants import *
from math import pi
import numpy as np
import regionToolset

executeOnCaeStartup()
Mdb()
mymodel = mdb.Model(name='Model-1')

# Configuration viewport
myview = session.Viewport(
    name='TecnoDigital School',
    origin=(0.0, 0.0),
    width=110, height=190
)
myview.makeCurrent()
myview.maximize()
myview.partDisplay.geometryOptions.setValues(referenceRepresentation=ON)

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


check_parameters(param_geom)


# =============================================================================
# 5. Fonction de création du mât
# =============================================================================

def create_tower(model, params):
    """
    Crée une tour conique (pleine ou creuse) dans Abaqus avec noms de parts prédéfinis.
    """
    r_up = params['r_up_tower']
    r_down = params['r_down_tower']
    h = params['h_tower']
    t = params['thickness_tower']

    if r_up <= 0 or r_down <= 0:
        raise ValueError("Les rayons doivent être strictement positifs.")
    if h <= 0:
        raise ValueError("La hauteur doit être strictement positive.")

    a = model.rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    sheetSize = max(r_down * 2, h * 2)

    # Fonction pour créer un sketch et le revolver
    def create_sketch_part(sketch_name, part_name, r1, r2):
        model.ConstrainedSketch(name=sketch_name, sheetSize=sheetSize)
        s = model.sketches[sketch_name]
        s.ConstructionLine(point1=(0,-sheetSize), point2=(0,sheetSize))
        s.Line((r1,0), (r2,h))
        s.Line((r2,h), (0,h))
        s.Line((0,h), (0,0))
        s.Line((0,0), (r1,0))
        part = model.Part(name=part_name, dimensionality=THREE_D, type=DEFORMABLE_BODY)
        part.BaseSolidRevolve(angle=360.0, sketch=s)
        del model.sketches[sketch_name]
        return part

    # Noms fixes des parts
    name_ext = 'Tower_ext'
    name_in  = 'Tower_in'

    # Partie externe
    tower_ext = create_sketch_part('__sketch_' + name_ext + '__', name_ext, r_down, r_up)

    # Partie interne
    r_up_in = r_up - t
    r_down_in = r_down - t
    tower_in = None
    if r_up_in > 0 and r_down_in > 0:
        tower_in = create_sketch_part('__sketch_' + name_in + '__', name_in, r_down_in, r_up_in)

    # Assemblage et fusion
    inst_ext = a.Instance(name='Tower_ext-1', part=tower_ext, dependent=ON)
    if tower_in:
        inst_in = a.Instance(name='Tower_in-1', part=tower_in, dependent=ON)
        tower_fused = a.InstanceFromBooleanCut(
            name='Tower',
            instanceToBeCut=inst_ext,
            cuttingInstances=(inst_in,),
            originalInstances=SUPPRESS
        )
    else:
        tower_fused = inst_ext.part
        tower_fused.rename('Tower')

    # Suppression sécurisée des parts temporaires
    for part_name in [name_ext, name_in]:
        if part_name in model.parts.keys():
            del model.parts[part_name]

    return tower_fused

# =============================================================================
# 6. Fonction de création du GBS fusionné
# =============================================================================
def create_fused_gbs(model, params):
    """
    Crée une structure GBS fusionnée avec:
        1. Plateau solide
        2. Cône creux
        3. Cylindre creux au-dessus du cône
    Puis fusionne toutes les parties en un seul solide.

    Args:
        model: Modèle Abaqus
        params: Dictionnaire de paramètres géométriques

    Returns:
        Part: Pièce GBS fusionnée
    """
    h_plateau = params['plateau_height']
    r_plateau = params['plateau_radius']

    h_cone = params['cone_height']
    r_ext_top_cone = params['cone_top_outer_radius']
    r_ext_bottom_cone = params['cone_bottom_outer_radius']
    t_cone = params['cone_thickness']
    r_int_top_cone = r_ext_top_cone - t_cone
    r_int_bottom_cone = r_ext_bottom_cone - t_cone

    h_cyl = params['cyl_height']
    r_ext_cyl_top = r_ext_top_cone
    r_int_cyl_top = r_ext_cyl_top - t_cone

    y0 = 0.0
    y1 = y0 + h_plateau
    y2 = y1 + h_cone
    y3 = y2 + h_cyl

    max_radius = max(r_plateau, r_ext_bottom_cone, r_ext_cyl_top)
    max_height = y3
    sheetSize = max(max_radius, max_height) * 2.5

    a = model.rootAssembly
    a.DatumCsysByDefault(CARTESIAN)

    # Plateau solide
    model.ConstrainedSketch(name='__sketch_plateau__', sheetSize=sheetSize)
    s = model.sketches['__sketch_plateau__']
    s.ConstructionLine(point1=(0, -sheetSize), point2=(0, sheetSize))
    s.Line(point1=(0, y0), point2=(r_plateau, y0))
    s.Line(point1=(r_plateau, y0), point2=(r_plateau, y1))
    s.Line(point1=(r_plateau, y1), point2=(0, y1))
    s.Line(point1=(0, y1), point2=(0, y0))
    plateau = model.Part(name='Plateau', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    plateau.BaseSolidRevolve(angle=360.0, sketch=s)
    del model.sketches['__sketch_plateau__']

    # Cône creux
    model.ConstrainedSketch(name='__sketch_cone__', sheetSize=sheetSize)
    s = model.sketches['__sketch_cone__']
    s.ConstructionLine(point1=(0, -sheetSize), point2=(0, sheetSize))
    s.Line(point1=(r_ext_bottom_cone, 0), point2=(r_ext_top_cone, h_cone))
    s.Line(point1=(r_int_top_cone, h_cone), point2=(r_int_bottom_cone, 0))
    s.Line(point1=(r_ext_top_cone, h_cone), point2=(r_int_top_cone, h_cone))
    s.Line(point1=(r_ext_bottom_cone, 0), point2=(r_int_bottom_cone, 0))
    cone = model.Part(name='Cone_Creux', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    cone.BaseSolidRevolve(angle=360.0, sketch=s)
    del model.sketches['__sketch_cone__']

    # Cylindre supérieur creux
    model.ConstrainedSketch(name='__sketch_cyl__', sheetSize=sheetSize)
    s = model.sketches['__sketch_cyl__']
    s.ConstructionLine(point1=(0, -sheetSize), point2=(0, sheetSize))
    s.Line(point1=(r_ext_cyl_top, 0), point2=(r_ext_cyl_top, h_cyl))
    s.Line(point1=(r_int_cyl_top, 0), point2=(r_int_cyl_top, h_cyl))
    s.Line(point1=(r_int_cyl_top, h_cyl), point2=(r_ext_cyl_top, h_cyl))
    s.Line(point1=(r_int_cyl_top, 0), point2=(r_ext_cyl_top, 0))
    cyl_top = model.Part(name='Cyl_Haut', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    cyl_top.BaseSolidRevolve(angle=360.0, sketch=s)
    del model.sketches['__sketch_cyl__']

    # Assemblage
    a.Instance(name='Plateau-1', part=plateau, dependent=ON)
    a.Instance(name='Cone-1', part=cone, dependent=ON)
    a.translate(instanceList=('Cone-1',), vector=(0.0, h_plateau, 0.0))
    a.Instance(name='Cyl_Haut-1', part=cyl_top, dependent=ON)
    a.translate(instanceList=('Cyl_Haut-1',), vector=(0.0, y2, 0.0))

    # Fusion en un seul solide
    merged_part = a.InstanceFromBooleanMerge(
        name='GBS_Fused',
        instances=(a.instances['Plateau-1'], a.instances['Cone-1'], a.instances['Cyl_Haut-1']),
        keepIntersections=True,
        originalInstances=SUPPRESS,
        domain=GEOMETRY
    )

    # Nettoyage des parts originales
    for part_name in ['Plateau', 'Cone_Creux', 'Cyl_Haut']:
        if part_name in model.parts:
            del model.parts[part_name]

    return model.parts['GBS_Fused']


# =============================================================================
# 7. Création des deux parts
# =============================================================================

tower_part = create_tower(mymodel, param_geom)
GBS_part = create_fused_gbs(mymodel, param_geom) 

# =============================================================================
# 7. Définition de l'Assembly 
# =============================================================================

def assemble_pipe_gbs(
        model,
        tower_part='Tower',
        gbs_part='GBS_Fused',
        h_pipe_bottom=0.0,
        h_gbs_top=0.0,
        dof=None,
        step_name='Step_BC'):
    """
    Assemble Pipe + GBS avec :
        - Positionnement vertical automatisé
        - Reference Point au sommet du GBS
        - Coupling RP ↔ surface du Pipe (KINEMATIC)
        - Sets visibles dans Abaqus/CAE
        - BC appliquées sur le RP via un Step dédié
    """

    a = model.rootAssembly

    # ---------- 0) Vérification des pièces ----------
    for part_name in [tower_part, gbs_part]:
        if part_name not in model.parts:
            raise KeyError(f"La pièce '{part_name}' n'existe pas dans model.parts.")

    # ---------- 1) Nettoyage assembly ----------
    for inst in list(a.instances.keys()):
        del a.instances[inst]

    # ---------- 2) Création instances ----------
    inst_gbs = a.Instance(name='GBS-1', part=model.parts[gbs_part], dependent=ON)
    inst_pipe = a.Instance(name='Pipe-1', part=model.parts[tower_part], dependent=ON)

    # ---------- 3) Positionnement du Pipe ----------
    dy = h_gbs_top - h_pipe_bottom
    a.translate(instanceList=('Pipe-1',), vector=(0.0, dy, 0.0))

    # ---------- 4) Création du Reference Point ----------
    rp = a.ReferencePoint(point=(0.0, h_gbs_top, 0.0))
    rp_id = rp.id
    rp_region = regionToolset.Region(referencePoints=(a.referencePoints[rp_id],))

    # ---------- 4b) Set pour le RP (visible dans CAE) ----------
    a.Set(name='RP_Interface', referencePoints=(a.referencePoints[rp_id],))

    # ---------- 5) Surface du Pipe (slave surface du coupling) ----------
    pipe_surf = a.Surface(
        side1Faces=inst_pipe.faces[:],
        name='Pipe_Contact_Surf'
    )

    # ---------- 5b) Set des faces du Pipe (visible dans CAE) ----------
    a.Set(name='Pipe_Top_Surface', faces=inst_pipe.faces[:])

    # ---------- 6) Coupling cinématique RP ↔ Pipe ----------
    model.Coupling(
        name='Coupling_Pipe_GBS',
        controlPoint=a.sets['RP_Interface'],
        surface=pipe_surf,
        influenceRadius=WHOLE_SURFACE,
        couplingType=KINEMATIC
    )

    # ---------- 7) Step + BC ----------
    if dof is not None:

        # Création du step si absent
        if step_name not in model.steps:
            model.StaticStep(name=step_name, previous='Initial')

        # Conversion degrés → radians
        def deg(x):
            return x * np.pi / 180.0 if x is not None else None

        # Remplissage des DOF non définis avec UNSET
        bc_kwargs = {
            'u1': dof.get('ux', None) if dof.get('ux', None) is not None else UNSET,
            'u2': dof.get('uy', None) if dof.get('uy', None) is not None else UNSET,
            'u3': dof.get('uz', None) if dof.get('uz', None) is not None else UNSET,
            'ur1': deg(dof.get('urx', None)) if dof.get('urx', None) is not None else UNSET,
            'ur2': deg(dof.get('ury', None)) if dof.get('ury', None) is not None else UNSET,
            'ur3': deg(dof.get('urz', None)) if dof.get('urz', None) is not None else UNSET,
        }

        # BC appliquée sur le Set du RP
        model.DisplacementBC(
            name='BC_Interface',
            createStepName=step_name,
            region=a.sets['RP_Interface'],   # <-- Set visible
            **bc_kwargs
        )

    return a.sets['RP_Interface']

# =============================================================================
# 7. Création de l'Assembly 
# =============================================================================

dof = {
    'ux': 0,
    'uy': 0,
    'uz': None,
    'urx': None,
    'ury': None,
    'urz': 0
}

h_gbs_top = param_geom['plateau_height'] + param_geom['cone_height'] + param_geom['cyl_height']

assemble_pipe_gbs(
    mymodel,
    tower_part='Tower',
    gbs_part='GBS_Fused',
    h_pipe_bottom=0.0,
    h_gbs_top=h_gbs_top,
    dof=dof,
    step_name='Step_BC'  # step dédié pour BC non nulles
)


