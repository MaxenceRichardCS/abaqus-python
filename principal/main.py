import def_geometrie as geom
import def_mesh  as meshpart
import def_mat as mat
import def_boundaryconditions as BC
import def_force as force

# =============================================================================
# 1. Initialisation du modèle Abaqus
# =============================================================================
from abaqus import mdb
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup

from math import pi, sqrt
import numpy as np

# Initialise CAE (utile si on lance le script depuis l'extérieur)
executeOnCaeStartup()

# Crée un modèle dans la base de données
mymodel = mdb.Model(name='Model-1')

# Vérification
print("Nom du modèle créé :", mymodel.name)


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

props_steel = {
    'young': 210e9,   # 210 GPa
    'poisson': 0.3,
    'density': 7850.0
}

# Béton pour le GBS
props_concrete = {
    'young': 30e9,    # 30 GPa
    'poisson': 0.2,
    'density': 2400.0
}

# =============================================================================
# Vérification des paramètres et création des deux Parts 
# =============================================================================
geom.check_parameters(param_geom)
print("Check parameters ok")

tower_part = geom.create_tower(mymodel, param_geom)
gbs_part = geom.create_fused_gbs(mymodel,param_geom)

# =============================================================================
# Création de l'Assembly 
# =============================================================================


h_gbs_top = param_geom['plateau_height'] + param_geom['cone_height'] + param_geom['cyl_height']

# ---------------------------------------------------------
# ÉTAPE 1 : GÉOMÉTRIE (On pose les pièces)
# ---------------------------------------------------------
inst_gbs, inst_tower = geom.create_assembly_geometry(
    mymodel,
    tower_part_name='Tower',
    gbs_part_name='GBS_Fused',
    h_pipe_bottom=0.0,
    h_gbs_top=h_gbs_top
)

# ---------------------------------------------------------
# ÉTAPE 2 : MÉCANIQUE (On crée les liens et les blocages)
# ---------------------------------------------------------
dof = {'ux': 0, 'uy': 0, 'uz': 0, 'urx': 0, 'ury': 0, 'urz': 0}

BC.create_interaction_tower_GBS(
    mymodel,
    inst_tower=inst_tower,    # On passe l'objet instance créé juste au-dessus
    h_interface=h_gbs_top,
    dof=dof,
    step_name='Step_BC'
)

# =============================================================================
# Application des BC
# =============================================================================

BC.encastrement_GBS(mymodel)

# =============================================================================
# Application des matériaux
# =============================================================================

# 1. Application sur la Tour
mat.create_and_assign_solid_material(
    model=mymodel, 
    part=tower_part, 
    mat_name='Steel_S355', 
    props=props_steel
)

# 2. Application sur le GBS
mat.create_and_assign_solid_material(
    model=mymodel, 
    part=gbs_part, 
    mat_name='Concrete_C50', 
    props=props_concrete
)

#=============================================================================
# Application  du Mesh
# =============================================================================

# 1. Application sur la Tour
meshpart.MeshTower(tower_part)

# 2. Application sur le GBS
meshpart.MeshGBS(gbs_part)

# =============================================================================
# 1. INITIALISATION ET CRÉATION DES INSTANCES
# =============================================================================

a = mymodel.rootAssembly

# Récupération des pièces
p_gbs = mymodel.parts['GBS_Fused']
p_tower = mymodel.parts['Tower']

# Création explicite des instances en mode DÉPENDANT (héritent du maillage des parts)
# Il est impératif de faire cela avant de manipuler les surfaces
if 'GBS-1' not in a.instances.keys():
    a.Instance(name='GBS-1', part=p_gbs, dependent=ON)

if 'Tower-1' not in a.instances.keys():
    a.Instance(name='Tower-1', part=p_tower, dependent=ON)

# =============================================================================
# 2. GESTION DES SURFACES (FUSION)
# =============================================================================

geom.fus_outer_surfaces(mymodel)

# =============================================================================
# 3. CONFIGURATION TEMPORELLE AUTOMATIQUE (STEP)
# =============================================================================

# Vos données d'amplitude
data = (
    (0.0, 0.0),
    (1.0, 0.5),
    (2.0, 1.0),
    (3.0, 0.5),
    (4.0, 0.0)
)

# Calcul automatique de la durée et du pas de temps
total_duration = data[-1][0]    # Prend le dernier temps (4.0)
target_frames = 50              # On veut environ 50 images pour l'animation
calculated_inc = total_duration / target_frames

# Application des réglages au Step 'Step_BC'
# Cela force Abaqus à découper le temps pour voir l'évolution progressive
mymodel.steps['Step_BC'].setValues(
    timePeriod=total_duration,
    initialInc=calculated_inc,
    maxInc=calculated_inc,       # Empêche le solveur de sauter des étapes
    minInc=total_duration * 1e-5
)

# Force l'enregistrement des résultats à chaque incrément calculé
if 'F-Output-1' in mymodel.fieldOutputRequests.keys():
    mymodel.fieldOutputRequests['F-Output-1'].setValues(frequency=1)

# =============================================================================
# 5. APPEL DE LA FONCTION
# =============================================================================

# Définition du vecteur directeur (Point A -> Point B) pour l'axe Z
vectez = ((0.0, 0.0, 0.0), (0.0, 0.0, 0.1))

force.apply_tabular_surface_traction(
    model=mymodel,
    surfaceName='Global_Outer_Surface', # On appelle la surface fusionnée
    stepName='Step_BC',
    data=data,
    directionVector=vectez,
    magnitude=10.0,
    ampName='Amp_Tabular_Z'
)

# =============================================================================
# 6. CRÉATION ET LANCEMENT DU JOB
# =============================================================================
def lancement_job(model):
    job_name = 'Job-GBS-Tower'

    # Création du Job
    mdb.Job(name=job_name, model=model, description='Calcul GBS et Tour')

    # Soumission du Job
    print("Soumission du job {}...".format(job_name))
    mdb.jobs[job_name].submit()

    # Attente de la fin du calcul
    print("Calcul en cours...")
    mdb.jobs[job_name].waitForCompletion()

    print("Calcul terminé. Le fichier .odb est généré.")

lancement_job(mymodel)