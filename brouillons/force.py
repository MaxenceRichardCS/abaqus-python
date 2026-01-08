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


tower_part = create_tower(mymodel, param_geom)

tower = mymodel.parts['Tower']

# Type d’éléments
elem_type = mesh.ElemType(elemCode=C3D8R, elemLibrary=STANDARD)

# Affecter les éléments
tower.setElementType(regions=(tower.cells,), elemTypes=(elem_type,))

# Définir la taille du maillage
tower.seedPart(size=1.5, deviationFactor=0.1, minSizeFactor=0.1)

# Générer le maillage
tower.generateMesh()

#définir le matériau
steel = mymodel.Material(name='Steel')
steel.Elastic(table=((210e3, 0.3),))


# l'attriber au mât

mymodel.HomogeneousSolidSection(
    name='SecTower',
    material='Steel'
)
tower = mymodel.parts['Tower']
cells = tower.cells
region = tower.Set(name='SetTower', cells=cells)

tower.SectionAssignment(
    region=region,
    sectionName='SecTower'
)

mymodel.StaticStep(name='LoadStep', previous='Initial')


mymodel.TabularAmplitude(
    name='AmpForce',
    timeSpan=STEP,
    smooth=SOLVER_DEFAULT,
    data=((0.0, 0.0),
          (10.0, 1.0))
)

