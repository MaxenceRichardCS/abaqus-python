from abaqus import *
from abaqusConstants import *
from caeModules import *

# =============================================================================
# FONCTION : TRACTION SURFACIQUE VARIABLE (TABULAIRE)
# =============================================================================

def apply_tabular_surface_traction(
        model,
        surfaceName,
        stepName,
        data,
        directionVector,
        magnitude,
        ampName='Amp_Tabular'
    ):
    """
    Applique une force répartie (Surface Traction) sur une surface donnée,
    avec une intensité qui varie au cours du temps selon un tableau de données.

    Args:
        model: Le modèle Abaqus.
        surfaceName (str): Nom de la surface (déjà créée dans l'assemblage).
        stepName (str): Nom de l'étape (Step) où la force s'applique.
        data (list): Paires (Temps, Amplitude) ex: ((0,0), (1,1)).
        directionVector (tuple): Vecteur (x, y, z) donnant la direction de la force.
        magnitude (float): Valeur de base de la force.
        ampName (str): Nom à donner à la courbe d'amplitude.
    """
    
    print(f"\n--- Application d'une Traction Surfacique sur '{surfaceName}' ---")
    
    a = model.rootAssembly

    # -------------------------------
    # Vérification de sécurité
    # -------------------------------
    # On vérifie d'abord que la surface existe bien dans l'assemblage.
    if surfaceName not in a.surfaces:
        print(f"ERREUR : La surface '{surfaceName}' n'existe pas dans l'assemblage rootAssembly !")
        print("Vérifiez que vous avez bien lancé la fonction 'fus_outer_surfaces' avant.")
        return # On arrête la fonction ici pour éviter le crash

    # -------------------------------
    # Création de l'Amplitude Temporelle
    # -------------------------------
    # Une "Amplitude" définit comment la force évolue (ex: monte progressivement).
    # Si elle n'existe pas encore, on la crée à partir des données 'data'.
    
    if ampName not in model.amplitudes.keys():
        model.TabularAmplitude(
            name=ampName,
            timeSpan=STEP,          # Le temps 0 correspond au début de l'étape (Step)
            smooth=SOLVER_DEFAULT,  # Lissage standard entre les points
            data=data               # Les points (temps, valeur)
        )
        print(f"-> Amplitude '{ampName}' créée (Type: Tabular).")
    else:
        print(f"-> Amplitude '{ampName}' existe déjà, on la réutilise.")

    # -------------------------------
    # Création de la Charge (Traction)
    # -------------------------------
    # On définit maintenant la force physique qui utilise l'amplitude créée ci-dessus.
    
    # Génération d'un nom unique pour la charge pour éviter les conflits
    # On inclut le nom de la surface et un élément du vecteur
    load_name = f"Load_{ampName}_{surfaceName}"
    
    # SurfaceTraction est utilisé pour des forces générales (pas forcément normales à la surface)
    model.SurfaceTraction(
        name=load_name,
        createStepName=stepName,
        region=a.surfaces[surfaceName], # On applique sur l'objet surface récupéré
        magnitude=magnitude,            # Valeur de référence
        directionVector=directionVector,# Vecteur (X, Y, Z)
        traction=GENERAL,               # 'GENERAL' permet de définir un vecteur arbitraire
        distributionType=UNIFORM,       # La force est la même partout sur la surface
        amplitude=ampName               # On lie la force à l'évolution temporelle
    )

    print(f"-> Succès : Charge '{load_name}' appliquée (Vecteur: {directionVector}).")