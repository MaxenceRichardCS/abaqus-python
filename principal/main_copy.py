import def_geometrie as geom
import def_mesh  as meshpart
import def_mat as mat

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
# Vérifier le dictionnaire des surfaces
gbs_part = geom.create_fused_gbs(mymodel,param_geom)

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

geom.assemble_tower_gbs(
    mymodel,
    tower_part,
    gbs_part,
    h_pipe_bottom=0.0,
    h_gbs_top=h_gbs_top,
    dof=dof,
    step_name='Step_BC'  # step dédié pour BC non nulles
)



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
# Création du Mesh
# =============================================================================

meshpart.MeshTower(tower_part)

meshpart.MeshGBS(gbs_part)


#=============================================================================
#=============================================================================

def apply_tabular_surface_traction(
        model,
        surfaceName,
        stepName,
        data,
        directionVector,
        magnitude,
        ampName='Amp_Tabular'
    ):

    a = model.rootAssembly

    # -------------------------------
    # Création de l'amplitude tabulée
    # -------------------------------
    if ampName not in model.amplitudes.keys():
        model.TabularAmplitude(
            name=ampName,
            timeSpan=STEP,
            smooth=SOLVER_DEFAULT,
            data=data
        )

    # -------------------------------
    # Création de la charge
    # -------------------------------
    model.SurfaceTraction(
        name='Load_' + ampName + '_' + surfaceName + '_' + str(directionVector[1]),
        createStepName=stepName,
        region=a.surfaces[surfaceName],
        magnitude=magnitude,
        directionVector=directionVector,
        traction=GENERAL,
        distributionType=UNIFORM,
        amplitude=ampName
    )


data = (
    (0.0, 0.0),
    (1, 0.5),
    (2, 1.0),
    (3, 0.5),
    (4, 0.0)
)

vectez = ((0.0, 0.0, 0.0), (0.0, 0.0, 0.1))

# 1. Récupération de l'assemblage
a = mdb.models['Model-1'].rootAssembly

# 2. Récupération des deux objets surfaces (depuis les instances)
surf_gbs = a.instances['GBS-1'].surfaces['GBS_Outer_Surface']
surf_tower = a.instances['Tower-1'].surfaces['Tower_Lateral_Surface']

# 3. Création de la surface fusionnée par Union
# Cette nouvelle surface existera au niveau de l'assemblage
a.SurfaceByBoolean(
    name='Global_Outer_Surface',
    surfaces=(surf_gbs, surf_tower),
    operation=UNION
)

apply_tabular_surface_traction(
    mymodel,
    surfaceName='Global_Outer_Surface',
    stepName='Step_BC',
    data=data,
    directionVector=vectez,   # ez
    magnitude=10.0,
    ampName='Amp_Tabular_Z'
)


""""

# 1. Création du Job
# On lie le job au modèle nommé 'Model-1' (ou votre variable mymodel)
mdb.Job(name='Job-GBS-Tower', model='Model-1', description='Calcul GBS et Tour')

# 2. Soumission du Job (Lancement du calcul)
mdb.jobs['Job-GBS-Tower'].submit()

# 3. Attente de la fin du calcul (Optionnel mais recommandé dans un script)
# Cela bloque le script tant que le calcul n'est pas fini.
# Utile pour ne pas essayer d'ouvrir les résultats avant qu'ils n'existent.
mdb.jobs['Job-GBS-Tower'].waitForCompletion()

print("Calcul terminé. Le fichier .odb est généré.")


# Exemple de création propre dans votre script
a = mdb.models['Model-1'].rootAssembly
p_gbs = mdb.models['Model-1'].parts['GBS_Fused']
p_tower = mdb.models['Model-1'].parts['Tower']

# Création explicite en mode DEPENDENT
a.Instance(name='GBS-1', part=p_gbs, dependent=ON)
a.Instance(name='Tower-1', part=p_tower, dependent=ON)
"""