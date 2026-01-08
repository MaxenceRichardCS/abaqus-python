# =============================================================================
# 1. Initialisation du modèle Abaqus
# =============================================================================
from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup
from math import pi

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
    'base_tower': True,

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
# 4. Fonction utilitaire
# =============================================================================
def deg2rad(angle_deg):
    """Convertit des degrés en radians."""
    return angle_deg * pi / 180.0

# =============================================================================
# 5. Fonction de création d'un cône coque 3D
# =============================================================================

def create_tower(model, params):
    """
    Crée une tour conique coque 3D avec épaisseur.

    Args:
        model: Modèle Abaqus
        params: Dictionnaire avec clés:
            - r_up_tower
            - r_down_tower
            - h_tower
            - thickness_tower
            - base_tower

    Returns:
        Part: Pièce "Tower"
    """
    r_up = params['r_up_tower']
    r_down = params['r_down_tower']
    h = params['h_tower']
    thickness = params['thickness_tower']
    base = params['base_tower']
    sheetSize = max(r_up, r_down, h) * 2.5

    model.ConstrainedSketch(name='__sketch_tower__', sheetSize=sheetSize)
    s = model.sketches['__sketch_tower__']
    s.ConstructionLine(point1=(0.0, -sheetSize), point2=(0.0, sheetSize))
    if base:
        s.Line(point1=(0, 0), point2=(r_down, 0))
    s.Line(point1=(r_down, 0), point2=(r_up, h))
    model.Part(dimensionality=THREE_D, name='Tower', type=DEFORMABLE_BODY)
    p = model.parts['Tower']
    p.BaseShellRevolve(angle=360.0, flipRevolveDirection=OFF, sketch=s)
    del model.sketches['__sketch_tower__']
    p.Set(faces=p.faces[:], name='Set_Tower')
    return p


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
# 7. Fonction d'assemblage avec debug
# =============================================================================
# ----------------------------
# Assembly et interface Pipe <-> GBS
# ----------------------------


# ----------------------------
# Assembly et interface Pipe <-> GBS
# ----------------------------
from abaqusConstants import *
import numpy as np
import regionToolset

# ----------------------------
# Assembly et interface Pipe <-> GBS
# ----------------------------
from abaqusConstants import *
import numpy as np
import regionToolset

def assemble_pipe_gbs(
        model,
        pipe_part='pipe',
        gbs_part='GBS_Fused',
        h_pipe_bottom=0.0,
        h_gbs_top=0.0,
        dof=None,
        step_name='Step_BC'):
    """
    Assemble Pipe + GBS sans bounding box.
    Positionne Pipe directement centré sur GBS le long de l'axe Y.
    Crée RP + couplings + appl. DOF dans un step dédié.

    Paramètres
    ----------
    h_pipe_bottom : float
        Position locale du bas du Pipe (souvent 0)
    h_gbs_top : float
        Hauteur du haut du GBS (tu la connais depuis la création)
    dof : dict
        Exemple :
        dof = {
            'ux': 0,
            'uy': None,
            'uz': 0,
            'urx': None,
            'ury': None,
            'urz': 10   # degrés
        }
    step_name : str
        Nom du step dans lequel appliquer les BC non nulles
    """

    a = model.rootAssembly

    # ---------- 0) Vérification des pièces ----------
    for part_name in [pipe_part, gbs_part]:
        if part_name not in model.parts:
            raise KeyError(f"La pièce '{part_name}' n'existe pas dans model.parts. Vérifie la création des parts.")

    # ---------- 1) Nettoyage assembly ----------
    for inst in list(a.instances.keys()):
        del a.instances[inst]

    # ---------- 2) Création instances ----------
    inst_gbs = a.Instance(name='GBS-1', part=model.parts[gbs_part], dependent=ON)
    inst_pipe = a.Instance(name='Pipe-1', part=model.parts[pipe_part], dependent=ON)

    # ---------- 3) Positionnement le long de Y ----------
    dy = h_gbs_top - h_pipe_bottom
    a.translate(instanceList=('Pipe-1',), vector=(0.0, dy, 0.0))

    # ---------- 4) Création du Reference Point ----------
    rp = a.ReferencePoint(point=(0.0, h_gbs_top, 0.0))
    rp_id = rp.id
    rp_region = regionToolset.Region(referencePoints=(a.referencePoints[rp_id],))

    # ---------- 5) Coupling ----------
    pipe_surf = a.Surface(
        side1Faces=inst_pipe.faces[:],
        name='Pipe_Contact_Surf'
    )

    model.Coupling(
        name='Pipe_GBS_Coupling',
        controlPoint=rp_region,
        surface=pipe_surf,
        influenceRadius=WHOLE_SURFACE,
        couplingType=KINEMATIC
    )

    # ---------- 6) Création du Step pour BC non nulles ----------
    if dof is not None:
        if step_name not in model.steps:
            model.StaticStep(name=step_name, previous='Initial')

        # Conversion rotations en radians
        def deg(x):
            return x * np.pi / 180.0 if x is not None else None

        bc_kwargs = {
            'u1': dof.get('ux', None) if dof.get('ux', None) is not None else UNSET,
            'u2': dof.get('uy', None) if dof.get('uy', None) is not None else UNSET,
            'u3': dof.get('uz', None) if dof.get('uz', None) is not None else UNSET,
            'ur1': deg(dof.get('urx', None)) if dof.get('urx', None) is not None else UNSET,
            'ur2': deg(dof.get('ury', None)) if dof.get('ury', None) is not None else UNSET,
            'ur3': deg(dof.get('urz', None)) if dof.get('urz', None) is not None else UNSET,
        }

        model.DisplacementBC(
            name='BC_Interface',
            createStepName=step_name,
            region=rp_region,
            **bc_kwargs
        )

    print(f"✔ Assembly complet. Pipe posé à Y={h_gbs_top}, RP créé, coupling et BC appliqués dans '{step_name}'.")

    return rp_region


# =============================================================================
# 8. Création des pièces
# =============================================================================
print("="*80)
print("CREATION DES PIECES")
print("="*80 + "\n")

pipe_part = model_geom_conical_shell_3D(
    model=mymodel,
    r_up=param_geom['r_up_cone'],
    r_down=param_geom['r_down_cone'],
    h=param_geom['h_cone'],
    thickness=param_geom['thickness_cone'],
    base=param_geom['base_cone'],
    size=200,
    name_part=param_calc['name_system']
)

GBS_part = create_fused_gbs(mymodel, param_geom)


# =============================================================================
# 9. Paramètres de contraintes
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
    pipe_part='pipe',
    gbs_part='GBS_Fused',
    h_pipe_bottom=0.0,
    h_gbs_top=h_gbs_top,
    dof=dof,
    step_name='Step_BC'  # step dédié pour BC non nulles
)
# =============================================================================
# 11. Affichage dans le viewport
# =============================================================================
print("CONFIGURATION DU VIEWPORT...")

myview.assemblyDisplay.setValues(

    adaptiveMeshConstraints=OFF,
    geometricConstraints=OFF
)
myview.assemblyDisplay.setValues(partInstances='all')
myview.view.fitView()

print("OK Viewport configure avec affichage ombre")
print("OK Vue ajustee a l'assemblage\n")

print("="*80)
print("SCRIPT TERMINE AVEC SUCCES!")
print("="*80)
print("Modele cree: {}".format(mymodel.name))
print("Pieces: {} (Pipe, GBS_Fused)".format(len(mymodel.parts)))
print("Instances: {}".format(len(mymodel.rootAssembly.instances)))
print("Contraintes: {}".format(len(mymodel.rootAssembly.constraints)))
print("="*80)