# =============================================================================
# 1. Initialisation du modèle Abaqus
# =============================================================================
from abaqus import mdb
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup

from math import pi
import numpy as np
import regionToolset

import os
import sys

import def_geometrie as geom
from def_mesh import MeshGBS, MeshTower


# Initialise CAE (utile si on lance le script depuis l'extérieur)
executeOnCaeStartup()

# Crée un modèle dans la base de données
mymodel = mdb.Model(name='Model-1')

# Vérification
print("Nom du modèle créé :", mymodel.name)



# current_dir = os.getcwd()
# if current_dir not in sys.path:
#     sys.path.append(current_dir)


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
# Vérification des paramètres et création des deux Parts 
# =============================================================================
geom.check_parameters(param_geom)

tower_part = geom.create_tower(mymodel, param_geom)
GBS_part = geom.create_fused_gbs(mymodel, param_geom) 

# =============================================================================
# Création de l'Assembly 
# =============================================================================

#ici encastrement 
dof = {
    'ux': 0,
    'uy': None,
    'uz': 0,
    'urx': 0,
    'ury': 0,
    'urz': 0
}

h_gbs_top = param_geom['plateau_height'] + param_geom['cone_height'] + param_geom['cyl_height']

geom.assemble_pipe_gbs(
    mymodel,
    tower_part='Tower',
    gbs_part='GBS_Fused',
    h_pipe_bottom=0.0,
    h_gbs_top=h_gbs_top,
    dof=dof,
    step_name='Step_BC'  # step dédié pour BC non nulles
)


MeshGBS()
MeshTower()

# surf = geom.get_surfaces_for_load(
#     model=mymodel
#     )

# a = mdb.models['Model-1'].rootAssembly
# print(a.surfaces)

# assert surf in a.surfaces.keys()

def Load_Sinus_Z():

    model = mymodel
    a = model.rootAssembly

    # -------------------------------
    # Amplitude sinusoïdale analytique
    # -------------------------------
    # syntaxe correcte : 5 arguments minimum
    model.PeriodicAmplitude(
        name='Amp_Sinus_Z',
        createStepName='Step_BC',
        timeSpan=STEP,
        frequency=1.0,  # 1 cycle sur la durée du step
        start=0.0
    )

    # -------------------------------
    # Surface chargée
    # -------------------------------
    region = a.surfaces['Pipe_Contact_Surf']

    # -------------------------------
    # Traction surfacique sinusoïdale
    # direction = axe global ez
    # -------------------------------
    model.SurfaceTraction(
        name='Load_Sinus_Z',
        createStepName='Step_BC',
        region=region,
        magnitude=10.0,
        directionVector=((0.0, 0.0, 0.0),
                         (0.0, 0.0, 1.0)),
        distributionType=UNIFORM,
        traction=GENERAL,
        amplitude='Amp_Sinus_Z'
    )



Load_Sinus_Z()
