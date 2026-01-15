from abaqus import *
from abaqusConstants import *
from caeModules import *

# =============================================================================
# FONCTION : TRACTION SURFACIQUE VARIABLE (TABULAIRE)
# =============================================================================

def apply_tabular_surface_traction(
        model, names, stepName, data, directionVector, 
        magnitude, h_cut, ampName='Amp_Tabular', 
        mask_side='above', surf_key='surf_global'
    ):
    """
    Applique une force répartie sur une surface, mais masquée par une hauteur (h_cut).
    Utilise une transition douce (tanh) pour éviter les erreurs numériques.
    
    Args:
        model : Le modèle Abaqus.
        names (dict) : Le dictionnaire contenant les noms des surfaces.
        stepName (str) : L'étape où la force est appliquée.
        data (tuple) : Les données (temps, amplitude) pour l'évolution temporelle.
        directionVector (tuple) : Vecteur direction de la force ((0,0,0), (1,0,0)).
        magnitude (float) : Valeur de base de la force.
        h_cut (float) : Altitude de la coupure (ex: niveau de la mer).
        ampName (str) : Nom à donner à l'amplitude temporelle.
        mask_side (str) : 'above' pour force au-dessus de h_cut (Vent), 
                          'below' pour force en dessous (Courant).
        surf_key (str) : La clé dans le dictionnaire 'names' pour trouver la surface.
                         Par défaut 'surf_global'.
    """
    print(f"\n--- Application Force Masquée ({mask_side} {h_cut}m) ---")
    a = model.rootAssembly
    
    # 1. Récupération du vrai nom de la surface depuis le dictionnaire
    if surf_key not in names:
        raise KeyError(f"La clé '{surf_key}' n'existe pas dans le dictionnaire 'names'.")
    
    real_surface_name = names[surf_key]
    
    # Vérification que la surface existe bien dans l'assemblage
    if real_surface_name not in a.surfaces:
        raise ValueError(f"La surface '{real_surface_name}' est introuvable dans l'assemblage.")

    # 2. Création du Masque Spatial (ExpressionField)
    # On gère le sens : Au-dessus (Vent) ou En-dessous (Eau)
    
    field_name = f'Mask_{mask_side}_{int(h_cut)}m'
    
    # Formule Sigmoïde (tanh)
    # k = 10.0 contrôle la raideur de la transition (plus c'est grand, plus c'est net)
    if mask_side == 'above':
        # Vaut 0 en bas, 1 en haut
        formula = f'0.5 * (1.0 + tanh((Y - {h_cut}) * 10.0))'
    elif mask_side == 'below':
        # Vaut 1 en bas, 0 en haut (notez le signe moins devant tanh)
        formula = f'0.5 * (1.0 - tanh((Y - {h_cut}) * 10.0))'
    else:
        raise ValueError("mask_side doit être 'above' ou 'below'")

    # Nettoyage préventif
    if field_name in model.analyticalFields:
        del model.analyticalFields[field_name]

    model.ExpressionField(
        name=field_name,
        expression=formula, 
        localCsys=None,
        description=f'Masque progressif {mask_side} Y={h_cut}m'
    )
    print(f"-> Champ analytique '{field_name}' créé.")

    # 3. Création de l'Amplitude Temporelle (Chronologie)
    if ampName not in model.amplitudes:
        model.TabularAmplitude(
            name=ampName, timeSpan=STEP, smooth=SOLVER_DEFAULT, data=data
        )

    # 4. Application de la Charge (SurfaceTraction)
    
    # Génération d'un nom unique pour la charge pour éviter les doublons
    # On utilise un bout du vecteur direction pour différencier X et Z
    suffix_vec = str(directionVector).replace(' ', '').replace('(', '').replace(')', '')[:6]
    load_name = f'Load_{ampName}_{suffix_vec}'
    
    if load_name in model.loads: del model.loads[load_name]

    model.SurfaceTraction(
        name=load_name,
        createStepName=stepName,
        region=a.surfaces[real_surface_name], # Utilisation du nom dynamique
        magnitude=magnitude,
        directionVector=directionVector,
        traction=GENERAL,
        
        # C'est ici qu'on lie tout : Espace (Field) et Temps (Amplitude)
        distributionType=FIELD,
        field=field_name,
        amplitude=ampName
    )
    
    print(f"-> Force appliquée avec succès : '{load_name}' sur '{real_surface_name}'.")