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
    # Le nom inclut une partie du vecteur pour l'unicité
    load_name = 'Load_' + ampName + '_' + surfaceName + '_' + str(directionVector[1])
    
    model.SurfaceTraction(
        name=load_name,
        createStepName=stepName,
        region=a.surfaces[surfaceName], # Utilise la surface d'assemblage
        magnitude=magnitude,
        directionVector=directionVector,
        traction=GENERAL,
        distributionType=UNIFORM,
        amplitude=ampName
    )
