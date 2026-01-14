

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