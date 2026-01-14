from abaqus import mdb
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup
from math import pi


def encastrement_GBS(model):
    # 1. On récupère l'instance du GBS
    inst_gbs = model.rootAssembly.instances['GBS-1']

    # 2. On sélectionne les faces qui sont au sol (Y = 0)
    # On utilise une "Bounding Box" très fine autour de 0.0
    # yMin=-0.1 et yMax=0.1 capturent toutes les faces planes du bas
    bottom_faces = inst_gbs.faces.getByBoundingBox(
        xMin=-100.0, yMin=-0.1, zMin=-100.0,
        xMax=100.0,  yMax=0.1,  zMax=100.0
    )

    # 3. On crée un Set (groupe) pour ces faces
    region_base = model.rootAssembly.Set(name='Base_GBS_Set', faces=bottom_faces)

    # 4. On applique l'encastrement (Tout bloqué : U1=U2=U3=UR1=UR2=UR3=0)
    # Important : createStepName='Initial' pour que ce soit bloqué dès le début
    model.EncastreBC(
        name='BC_Encastrement_Base',
        createStepName='Initial', 
        region=region_base
    )


def create_interaction_tower_GBS(model, inst_tower, h_interface, dof, step_name='Step_BC'):
    """
    Gère la "colle" entre les pièces : Reference Point, Coupling et Conditions Limites.
    """
    a = model.rootAssembly
    
    # 1. Création du Reference Point (RP) à l'interface
    a.ReferencePoint(point=(0.0, h_interface, 0.0))
    # On le retrouve par sa position pour créer un Set
    rp_obj = a.referencePoints.findAt((0.0, h_interface, 0.0), )
    rp_set = a.Set(name='RP_Interface', referencePoints=(rp_obj,))

    # 2. Définition de la surface esclave (bas de la tour)
    # Note : On utilise l'objet instance passé en argument
    pipe_surf = a.Surface(side1Faces=inst_tower.faces[:], name='Tower_Contact_Surf')

    # 3. Création du Coupling (Liaison rigide cinématique)
    model.Coupling(
        name='Coupling_Pipe_GBS', 
        controlPoint=rp_set, 
        surface=pipe_surf,
        influenceRadius=WHOLE_SURFACE, 
        couplingType=KINEMATIC,
        u1=ON, u2=ON, u3=ON, ur1=ON, ur2=ON, ur3=ON
    )

    # 4. Gestion du Step et des BCs (Conditions limites sur le RP)
    if dof is not None:
        # Création du Step si nécessaire
        if step_name not in model.steps:
            model.StaticStep(name=step_name, previous='Initial')

        # Mapping des noms utilisateur vers Abaqus (ux -> u1)
        bc_args = {'name': 'BC_Interface', 'createStepName': step_name, 'region': rp_set}
        dof_map = {
            'ux': 'u1', 'uy': 'u2', 'uz': 'u3',
            'urx': 'ur1', 'ury': 'ur2', 'urz': 'ur3'
        }
        
        # Conversion Degrés -> Radians pour les rotations
        deg_to_rad = pi / 180.0
        
        for user_key, abq_key in dof_map.items():
            val = dof.get(user_key)
            if val is not None:
                # Si c'est une rotation (commence par 'ur'), on convertit
                if user_key.startswith('ur'):
                    bc_args[abq_key] = val * deg_to_rad
                else:
                    bc_args[abq_key] = val

        # Application de la BC seulement si on a des valeurs
        if len(bc_args) > 3: # >3 car il y a name, step, region
            model.DisplacementBC(**bc_args)
            
    print("Interactions et BC appliquées.")