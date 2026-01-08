from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup
from math import pi, sin

# 1. Initialisation
executeOnCaeStartup()
Mdb()  # Remet à zéro le modèle
mymodel = mdb.models['Model-1']

# Configuration de la vue
myview = session.Viewport(name='TecnoDigital School', origin=(0.0, 0.0), width=110, height=190)
myview.makeCurrent()
myview.maximize()
myview.partDisplay.geometryOptions.setValues(referenceRepresentation=ON)

# 2. Fonction pour créer un solide conique 3D
def model_geom_cylindre_3D(model, radius=2.0, height=10.0, size=20, name_part='cylindre'):
    """
    Crée un cylindre plein 3D dans le modèle Abaqus.
    
    Args:
        model: le modèle Abaqus (mdb.models['Model-1'])
        radius: rayon du cylindre
        height: hauteur du cylindre
        size: taille de l'esquisse (sheetSize)
        name_part: nom de la pièce
    Returns:
        La pièce créée (Part object)
    """
    # 1. Création de l'esquisse
    model.ConstrainedSketch(name='__profile__', sheetSize=size)
    s = model.sketches['__profile__']
    
    # Cercle de base
    s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(radius, 0.0))
    
    # 2. Création de la pièce solide
    model.Part(dimensionality=THREE_D, name=name_part, type=DEFORMABLE_BODY)
    p = model.parts[name_part]
    p.BaseSolidExtrude(sketch=s, depth=height)
    
    # 3. Suppression de l'esquisse
    del model.sketches['__profile__']
    
    return p


# 3. Paramètres
params = {
    'base': False,
    'r_up': 1.0,
    'r_down': 2.0,
    'h': 50.0,
    'size_mesh': 1.0,
    'incSize': 0.005,
    'timePeriod': 10.0,
    'name_system': 'pipe',
    'A_wind': 1000.0,
    'E': 2e5,
    'nu': 0.3,
    'density': 7.85e-9
}

# 4. Création de la géométrie solide
pipe_part = model_geom_cylindre_3D(
    mymodel,
    name_part=params['name_system']
)
p = mymodel.parts['pipe']

# 5. Matériau et section solide
mymodel.Material(name='Acier')
mymodel.materials['Acier'].Elastic(table=((params['E'], params['nu']), ))
mymodel.materials['Acier'].Density(table=((params['density'], ), ))

mymodel.HomogeneousSolidSection(name='Pipe_Section', material='Acier', thickness=None)

# Assigner la section à tout le solide
cells_solid = p.cells[:]
region_solid = p.Set(cells=cells_solid, name='Set_Pipe')
p.SectionAssignment(region=region_solid, sectionName='Pipe_Section')

# 6. Maillage
p.seedPart(size=params['size_mesh'], deviationFactor=0.1, minSizeFactor=0.1)
p.generateMesh()

# 7. Step dynamique implicite
nom_etape = 'Vent_Etape'
try:
    mymodel.ImplicitDynamicsStep(
        name=nom_etape, previous='Initial',
        timePeriod=params['timePeriod'],
        maxNumInc=10000,
        initialInc=params['incSize']
    )
except ValueError:
    pass

# 8. Création de la surface pour appliquer la pression
seq_faces = p.faces[0:1]
p.Surface(side1Faces=seq_faces, name='Surf_Vent')

# 9. Création de l’instance
a = mymodel.rootAssembly
if 'Pipe-1' in a.instances:
    del a.instances['Pipe-1']
a.Instance(name='Pipe-1', part=p, dependent=ON)

region_instance = a.instances['Pipe-1'].surfaces['Surf_Vent']

# 10. Amplitude temporelle sin²(t)
nb_points = 100
delta_t = params['timePeriod'] / (nb_points - 1)
data_amplitude = [(i*delta_t, sin(i*delta_t)**2) for i in range(nb_points)]
nom_amplitude = 'Vent_Dynamique_Amplitude'
mymodel.TabularAmplitude(name=nom_amplitude, data=tuple(data_amplitude), timeSpan=STEP)

# 11. Application de la pression variable
mymodel.Pressure(
    name='PressionVent',
    createStepName=nom_etape,
    region=region_instance,
    magnitude=params['A_wind'],
    amplitude=nom_amplitude
)

# 12. Création et lancement du job
job = mdb.Job(name='Job_Pipe', model='Model-1', type=ANALYSIS)
job.submit()
job.waitForCompletion()

# 13. Lecture des déplacements
from odbAccess import openOdb
odb = openOdb('Job_Pipe.odb')
step = odb.steps[nom_etape]
frame = step.frames[-1]
disp_field = frame.fieldOutputs['U']

for value in disp_field.values:
    print(f'Nœud {value.nodeLabel} : déplacement {value.data}')
