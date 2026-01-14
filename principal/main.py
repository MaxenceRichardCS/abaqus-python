import def_geometrie as geom
import def_mesh  as meshpart
import def_mat as mat
import def_boundaryconditions as BC
import def_force as force
import def_job as job

# =============================================================================
# Initialisation du modèle Abaqus
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
# Paramètres
# =============================================================================
param_geom = {
    # Tower
    'r_up_tower': 1.0,
    'r_down_tower': 3.5,
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

param_mesh = {
    'Tower':6.0 , #compromis pour rester en dessous de 1 000 noeuds 
    'GBS' :5.0  #compromis pour rester en dessous de 1 000 noeuds 
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

BC.create_tie_tower_gbs(mymodel, inst_tower, inst_gbs, h_gbs_top)

# =============================================================================
# Application de l'encastrement au sol
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
meshpart.MeshTower(tower_part,param_mesh['Tower'])

# 2. Application sur le GBS
meshpart.MeshGBS(gbs_part, param_mesh['GBS'])

# =============================================================================
# GESTION DES SURFACES (FUSION)
# =============================================================================

geom.fus_outer_surfaces(mymodel, inst_gbs, inst_tower)

# =============================================================================
# CONFIGURATION TEMPORELLE AUTOMATIQUE (STEP)
# =============================================================================

# Données d'amplitude
force_z_temp = (
    (0.0, 0.0),
    (1.0, 0.5),
    (2.0, 1.0),
    (3.0, 0.5),
    (4.0, 0.0)
)

# Calcul automatique de la durée et du pas de temps
total_duration = force_z_temp[-1][0]    # Prend le dernier temps (4.0)
target_frames = 50              # On veut environ 50 images pour l'animation
calculated_inc = total_duration / target_frames

# Application des réglages au Step 'Step_BC'
# Cela force Abaqus à découper le temps pour voir l'évolution progressive

if 'Step_BC' not in mymodel.steps:
    mymodel.StaticStep(name='Step_BC', previous='Initial')

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
# Application de la force de traction
# =============================================================================

# Définition du vecteur directeur (Point A -> Point B) pour l'axe Z
vectez = ((0.0, 0.0, 0.0), (0.0, 0.0, 0.1))

force.apply_tabular_surface_traction(
    model=mymodel,
    surfaceName='Global_Outer_Surface', # On appelle la surface fusionnée
    stepName='Step_BC',
    data=force_z_temp,
    directionVector=vectez,
    magnitude=1,
    ampName='Amp_Tabular_Z'
)

# =============================================================================
# CRÉATION ET LANCEMENT DU JOB
# =============================================================================

job.lancement_job(mymodel)