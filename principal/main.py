import def_geometrie as geom
import def_mesh  as meshpart
import def_mat as mat
import def_boundaryconditions as BC
import def_force as force
import def_job as jobb
import def_post as post

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

    'dim_tour' : '1D',  #1D ou 3D

    # Tower
    'r_up_tower': 2.0,
    'r_down_tower': 3.5,
    'h_tower': 50.0,
    'thickness_tower': 0.5,

    # Plateau (solid)
    'plateau_radius': 15.5,
    'plateau_height': 1.7,

    # Cône GBS (hollow)
    'cone_height': 27.3,
    'cone_top_outer_radius': 3.5,
    'cone_bottom_outer_radius': 10.0,
    'cone_thickness': 0.5,

    # Cylindre au-dessus du cône
    'cyl_height': 18.0,

    'h_monitor' : 42.65
}

r_moy = (param_geom['r_up_tower'] + param_geom['r_down_tower']) / 2.0
param_geom['r_moy'] = r_moy

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
    'GBS' :3.0  #compromis pour rester en dessous de 1 000 noeuds 
}

names_dict = {
    # --- Géométrie (Parts) ---
    'part_tower': 'Tower_Steel',
    'part_gbs':   'GBS_Concrete',
    
    # --- Assemblage (Instances) ---
    'inst_tower': 'Inst_Tower_1',
    'inst_gbs':   'Inst_GBS_1',
    
    # --- Surfaces ---
    'surf_tower': 'Surf_Steel_Outer',
    'surf_gbs':   'Surf_Concrete_Outer',
    'surf_global':'Surf_Global_Environment',

    # --- Simulation (Job, Step, Monitoring) ---
    'job_name':    'Job-GBS-Tower',       # Le nom du fichier calcul
    'step_name':   'Step_BC',             # Le nom de l'étape de calcul
    'set_monitor': 'Set_Monitor_Top'      # Le nom du point qu'on surveille
}

# =============================================================================
# Vérification des paramètres et création des deux Parts 
# =============================================================================
geom.check_parameters(param_geom)
print("Check parameters ok")

tower_part = geom.create_tower(mymodel, param_geom, names_dict)
gbs_part = geom.create_fused_gbs(mymodel,param_geom,names_dict)

# =============================================================================
# Application des matériaux
# =============================================================================

# 1. Application sur la Tour
# DANS L'APPLICATION DES MATERIAUX
if param_geom['dim_tour'] == '1D':
    # Nouvelle fonction pour les poutres
    mat.create_and_assign_beam_material(mymodel, tower_part, 'Steel_S355', props_steel, param_geom)
else:
    # Ancienne fonction pour les solides
    mat.create_and_assign_solid_material(mymodel, tower_part, 'Steel_S355', props_steel)
# 2. Application sur le GBS
mat.create_and_assign_solid_material(model=mymodel,part=gbs_part,mat_name='Concrete_C50',props=props_concrete)

#=============================================================================
# Application  du Mesh
# =============================================================================

# 1. Application sur la Tour
if param_geom['dim_tour'] == '1D':
    meshpart.MeshTower1D(tower_part, size=param_mesh['Tower'])
else:
    meshpart.MeshTower(tower_part, param_mesh['Tower'])

# 2. Application sur le GBS
meshpart.MeshGBS(gbs_part, param_mesh['GBS'])

# =============================================================================
# Création de l'Assemblage
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

BC.create_tie_tower_gbs(mymodel, inst_tower, inst_gbs, h_gbs_top, param_geom['dim_tour'])

# =============================================================================
# Application de l'encastrement au sol
# =============================================================================

BC.encastrement_GBS(mymodel,names_dict)

# =============================================================================
# Definition des points d'observation
# =============================================================================
h_top = h_gbs_top + param_geom['h_tower']

#monitor_created = geom.create_monitor_point_GBS(mymodel,names_dict,param_geom,param_geom['h_monitor'])
monitor_created = geom.create_monitor_point_top(mymodel,names_dict, inst_tower, h_top, '1D')


if monitor_created : 
    print("--- Mise à jour du maillage GBS (post-partition) ---")
    meshpart.MeshGBS(gbs_part, param_mesh['GBS']) # On remaille le GBS modifié
else : 
    print("   /!\\ ALERTE : Le point de monitoring n'a pas pu être créé.")
    print("                Le calcul se lancera sans courbe de suivi au sommet.")

# =============================================================================
# GESTION DES SURFACES (FUSION)
# =============================================================================

# On ne crée la surface globale "GBS + Tour" que si la tour est un volume (3D).
# En 1D, la tour est gérée à part (via son Set de poutre).

if param_geom['dim_tour'] == '3D':
    geom.fus_outer_surfaces(mymodel, inst_gbs, inst_tower, names_dict)

# =============================================================================
# CONFIGURATION TEMPORELLE AUTOMATIQUE (STEP)
# =============================================================================

# =============================================================================
# A. DÉFINITION DES SCÉNARIOS DE CHARGEMENT (DATA)
# =============================================================================
# Ici, on rentre directement les valeurs réelles (Temps, Force en Newtons).
# On mettra la Magnitude à 1 plus bas pour que ces valeurs soient respectées telles quelles.

# Scénario 1 : Force selon X (ex: Vent principal)
# =============================================================================
# A. DÉFINITION DES SCÉNARIOS DE CHARGEMENT
# =============================================================================
print("\n--- Traitement des Données de Chargement ---")

# Scénario 1 : Force Vent X (Données Brutes)
# Note : Ici, j'ai mis 5000.0 N pour tester la normalisation automatique
raw_force_x = (
    (0.0, 0.0),
    (1.0, 2000.0), 
    (2.0, 5000.0), # Pic à 5000 N
    (3.0, 2000.0),
    (4.0, 0.0)
)

# Scénario 2 : Force Vent Z (Données Brutes)
raw_force_z = (
    (0.0, 0.0),
    (2.5, 8000.0), # Pic à 8000 N
    (5.0, 0.0)
)

# --- Normalisation Automatique ---
# On récupère : le profil (0-1), la magnitude (Newton) et la durée (s)
data_x_norm, mag_x, time_x = force.process_load_data(raw_force_x)
data_z_norm, mag_z, time_z = force.process_load_data(raw_force_z)

# =============================================================================
# B. CONFIGURATION TEMPORELLE (STEP)
# =============================================================================

# Calcul de la durée totale requise (le max des deux scénarios)
total_sim_duration = max(time_x, time_z)

# Appel de la fonction de configuration robuste
force.configure_step_and_outputs(
    model=mymodel, 
    names=names_dict, 
    total_time=total_sim_duration, 
    target_frames=50
)

# =============================================================================
# C. APPLICATION DES FORCES
# =============================================================================

print("\n--- Application des Chargements ---")

# 1. Force du VENT X
force.apply_force_automatic(
    model=mymodel,
    names=names_dict,
    stepName=names_dict['step_name'],
    data=data_x_norm,             # Profil temporel normalisé
    directionVector=((0,0,0), (1,0,0)), 
    magnitude=mag_x,     # <--- On envoie la PRESSION pure (Pa)
    h_cut=h_mer,
    ampName='Amp_Vent_X',
    mask_side='above',
    surf_key='surf_global',
    param_geom=param_geom         # <--- C'est lui qui permet la conversion interne
)

# 2. Force du VENT Z
force.apply_force_automatic(
    model=mymodel,
    names=names_dict,
    stepName=names_dict['step_name'],
    data=data_z_norm,
    directionVector=((0,0,0), (0,0,1)), 
    magnitude=mag_z,     # <--- Idem, pression pure
    h_cut=h_mer,
    ampName='Amp_Vent_Z',
    mask_side='above',
    surf_key='surf_global',
    param_geom=param_geom
)

# ============================================================================
# LANCEMENT ET POST-TRAITEMENT
# =============================================================================

# 1. Lancement du Job
# On passe juste le nom stocké dans le dictionnaire
# (Assurez-vous que votre def_job.py accepte cet argument, voir note plus bas)
my_job = jobb.lancement_job(mymodel, names_dict['job_name'])

# 2. Attente de la fin du calcul (Sécurité indispensable)
# Cela évite que le script de post-traitement ne se lance avant la fin du calcul
try:
    my_job.waitForCompletion()
except Exception as e:
    print(f"Calcul interrompu : {e}")

# =============================================================================
# POST-TRAITEMENT (CSV + IMAGE)
# =============================================================================

# 1. Définition des noms de fichiers
odb_file = names_dict['job_name'] + '.odb'
csv_file = names_dict['job_name'] + '_Resultats.csv'
png_file = names_dict['job_name'] + '_Courbe.png'

# 2. Génération du CSV (Données brutes)
post.export_history_to_csv(
    odb_name=odb_file,
    step_name=names_dict['step_name'],   # 'Step_BC'
    set_name=names_dict['set_monitor'],  # 'Set_Monitor_Top'
    csv_filename=csv_file
)

# 3. Génération de l'Image (Visualisation)
post.create_plot_from_csv(
    csv_filename=csv_file,
    image_filename=png_file
)

jobb.clean_abaqus_temp_files(names_dict['job_name'])

print("\n--- FIN DU SCRIPT ---")
