import def_geometrie as geom
import def_mesh  as meshpart
import def_mat as mat
import def_boundaryconditions as BC
import def_force as force
import def_job as jobb

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
Mdb()
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

h_mer = 40


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

names_dict = {
    # Noms des Parts (Bibliothèque)
    'part_tower': 'Tower_Steel',
    'part_gbs':   'GBS_Concrete',
    
    # Noms des Instances (Assemblage)
    'inst_tower': 'Inst_Tower_1',
    'inst_gbs':   'Inst_GBS_1',
    
    # Noms des Surfaces
    'surf_tower': 'Surf_Steel_Outer',
    'surf_gbs':   'Surf_Concrete_Outer',
    'surf_global':'Surf_Global_Environment'
}

# =============================================================================
# Vérification des paramètres et création des deux Parts 
# =============================================================================
geom.check_parameters(param_geom)
print("Check parameters ok")

tower_part = geom.create_tower(mymodel, param_geom,names_dict)
gbs_part = geom.create_fused_gbs(mymodel,param_geom,names_dict)

# =============================================================================
# Création de l'Assembly 
# =============================================================================

h_gbs_top = param_geom['plateau_height'] + param_geom['cone_height'] + param_geom['cyl_height']

# ---------------------------------------------------------
# ÉTAPE 1 : GÉOMÉTRIE (On pose les pièces)
# ---------------------------------------------------------
inst_gbs, inst_tower = geom.create_assembly_geometry(
    mymodel,
    names_dict,
    h_pipe_bottom=0.0,
    h_gbs_top=h_gbs_top
)

# ---------------------------------------------------------
# ÉTAPE 2 : MÉCANIQUE (On crée les liens et les blocages)
# ---------------------------------------------------------

BC.create_tie_tower_gbs(mymodel, inst_tower, inst_gbs, h_gbs_top)

# =============================================================================
# Application de l'encastrement au sol
# =============================================================================

BC.encastrement_GBS(mymodel,names_dict)

# =============================================================================
# Application des matériaux
# =============================================================================

# 1. Application sur la Tour
mat.create_and_assign_solid_material(model=mymodel,part=tower_part,mat_name='Steel_S355',props=props_steel)

# 2. Application sur le GBS
mat.create_and_assign_solid_material(model=mymodel,part=gbs_part,mat_name='Concrete_C50',props=props_concrete)

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

geom.fus_outer_surfaces(mymodel, inst_gbs, inst_tower,names_dict)

# =============================================================================
# CONFIGURATION TEMPORELLE AUTOMATIQUE (STEP)
# =============================================================================

# =============================================================================
# A. DÉFINITION DES SCÉNARIOS DE CHARGEMENT (DATA)
# =============================================================================
# Ici, on rentre directement les valeurs réelles (Temps, Force en Newtons).
# On mettra la Magnitude à 1 plus bas pour que ces valeurs soient respectées telles quelles.

# Scénario 1 : Force selon X (ex: Vent principal)
# Format : (Temps s, Force N)
data_force_x = (
    (0.0, 0.0),
    (1.0, 2.0),  # Montée rapide à 2000 N
    (2.0, 5.0),  # Pic à 5000 N
    (3.0, 2.0),
    (4.0, 0.0)      # Fin à 4s
)

# Scénario 2 : Force selon Z (ex: Courant latéral)
# Profil différent : plus lent, moins fort, dure plus longtemps
data_force_z = (
    (0.0, 0.0),
    (2.5, 8.0),   # Pic décalé à 2.5s
    (5.0, 0.0)      # Fin à 5s
)

# =============================================================================
# B. CONFIGURATION TEMPORELLE AUTOMATIQUE (STEP)
# =============================================================================

# 1. Calcul de la durée totale requise
# On regarde quel scénario finit le plus tard pour ne pas couper la simulation avant.
max_time_x = data_force_x[-1][0]
max_time_z = data_force_z[-1][0]
total_duration = max(max_time_x, max_time_z)

# 2. Réglage de la finesse du calcul (Incréments)
target_frames = 50  # On veut ~50 points pour faire une belle courbe
calc_inc = total_duration / target_frames

print(f"Configuration Temps : Durée totale = {total_duration}s (Pilotée par le scénario le plus long)")

# 3. Création / Mise à jour du Step
if 'Step_BC' not in mymodel.steps:
    mymodel.StaticStep(name='Step_BC', previous='Initial')

mymodel.steps['Step_BC'].setValues(
    timePeriod=total_duration,
    initialInc=calc_inc,
    maxInc=calc_inc,
    minInc=1e-5
)

# Force la sauvegarde à chaque point calculé (pour l'animation)
if 'F-Output-1' in mymodel.fieldOutputRequests:
    mymodel.fieldOutputRequests['F-Output-1'].setValues(frequency=1)

# =============================================================================
# C. APPLICATION DES FORCES (X et Z)
# =============================================================================

# 1. Application Force X
# Vecteur X : ((0,0,0), (1,0,0)) -> Pointe vers X positif
# Dans main.py

# ...

# 1. Force du VENT (Au-dessus de l'eau)
force.apply_tabular_surface_traction(
    model=mymodel,
    names=names_dict,                # Le dictionnaire contenant les noms
    stepName='Step_BC',
    data=data_force_x,
    directionVector=((0,0,0), (1,0,0)), 
    magnitude=1.0, 
    h_cut=h_mer,
    ampName='Amp_Vent_X',
    mask_side='above',               # Spécifique au vent
    surf_key='surf_global'           # On vise la surface fusionnée
)

# 2. Force du COURANT (En-dessous de l'eau)
force.apply_tabular_surface_traction(
    model=mymodel,
    names=names_dict,
    stepName='Step_BC',
    data=data_force_z,
    directionVector=((0,0,0), (0,0,1)),
    magnitude=1.0, 
    h_cut=h_mer,
    ampName='Amp_Courant_Z',
    mask_side='above',               # Spécifique au courant
    surf_key='surf_global'
)

# =============================================================================
# CRÉATION ET LANCEMENT DU JOB
# =============================================================================

jobb.lancement_job(mymodel)
