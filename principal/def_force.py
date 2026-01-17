from abaqus import *
from abaqusConstants import *
from caeModules import *

def create_height_mask(model, mask_side, h_cut):
    """
    Crée le champ analytique (ExpressionField) pour couper la force en hauteur.
    Retourne le nom du champ créé.
    """
    field_name = f'Mask_{mask_side}_{int(h_cut)}m'
    
    # Formule Sigmoïde (tanh) pour transition douce
    if mask_side == 'above':
        # 0 en bas, 1 en haut (Vent)
        formula = f'0.5 * (1.0 + tanh((Y - {h_cut}) * 10.0))'
    elif mask_side == 'below':
        # 1 en bas, 0 en haut (Courant)
        formula = f'0.5 * (1.0 - tanh((Y - {h_cut}) * 10.0))'
    else:
        # Pas de masque (toujours 1)
        return None

    # Nettoyage si existe déjà
    if field_name in model.analyticalFields:
        del model.analyticalFields[field_name]

    model.ExpressionField(
        name=field_name,
        expression=formula, 
        localCsys=None,
        description=f'Masque progressif {mask_side} Y={h_cut}m'
    )
    return field_name


def apply_surface_traction_3d(model, step_name, load_name, region, amp_name, field_name, mag, vec):
    """
    Ouvrier 3D : Applique une Pression sur une Surface.
    """
    print(f"   -> 3D : Surface Traction sur '{region.name}' (Mag={mag:.1f})")
    
    # Arguments pour SurfaceTraction
    args = {
        'name': load_name,
        'createStepName': step_name,
        'region': region,
        'magnitude': mag,
        'directionVector': vec,
        'traction': GENERAL,
        'amplitude': amp_name
    }
    
    # Ajout du masque seulement s'il existe
    if field_name:
        args['distributionType'] = FIELD
        args['field'] = field_name
        
    model.SurfaceTraction(**args)


def apply_line_load_1d(model, step_name, load_name, region, amp_name, field_name, mag, vec):
    """
    Ouvrier 1D : Applique une Charge Linéique sur une Poutre.
    Force = N/m
    """
    print(f"   -> 1D : Line Load (Mag={mag:.1f} N/m)")    
    # Calcul des composantes (LineLoad demande comp1, comp2, comp3)
    p1, p2 = vec
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dz = p2[2] - p1[2]
    
    c1 = mag * dx
    c2 = mag * dy
    c3 = mag * dz
    
    # Arguments pour LineLoad
    args = {
        'name': load_name,
        'createStepName': step_name,
        'region': region,
        'amplitude': amp_name,
        'comp1': c1, 'comp2': c2, 'comp3': c3
    }
    
    # Note : LineLoad supporte aussi 'distributionType=FIELD' dans les versions récentes,
    # mais souvent appliqué via scaleFactor.
    if field_name:
        args['distributionType'] = FIELD
        args['field'] = field_name
        
    model.LineLoad(**args)

def apply_force_automatic(model, names, stepName, data, directionVector, magnitude, h_cut, ampName, mask_side, surf_key, param_geom):
    """
    Gère tout : l'amplitude, le masque, la conversion d'unités (1D vs 3D) et l'application.
    """
    print(f"\n--- Application Force : {ampName} ---")
    
    # 1. Analyse du mode (1D ou 3D) et Conversion de la Magnitude
    is_1d = (param_geom['dim_tour'] == '1D')
    
    if is_1d:
        # --- CAS 1D : Conversion Pression (Pa) -> Force Linéique (N/m) ---
        # Formule : F_lin = Pression * Diamètre_Projeté
        diametre = 2.0 * param_geom['r_moy']
        final_mag = magnitude * diametre
        
        print(f"   [INFO] Mode 1D détecté : Conversion Pression -> Charge Linéique")
        print(f"          Input: {magnitude} Pa -> Applied: {final_mag:.2f} N/m")
    else:
        # --- CAS 3D : On garde la Pression (Pa) ---
        final_mag = magnitude
        print(f"   [INFO] Mode 3D : Application directe de la pression ({final_mag} Pa)")

    # 2. Création de l'Amplitude (Commun)
    if ampName not in model.amplitudes:
        model.TabularAmplitude(name=ampName, data=data, smooth=SOLVER_DEFAULT)

    # 3. Création du Masque Hauteur (Commun)
    field_mask_name = create_height_mask(model, mask_side, h_cut)

    # Nom unique pour la charge
    suffix = str(directionVector).replace(' ', '').replace('(', '').replace(')', '')[:6]
    load_name = f"Load_{ampName}_{suffix}"
    
    if load_name in model.loads: del model.loads[load_name]

    # 4. Aiguillage vers l'ouvrier spécialisé
    if is_1d:
        # --- OUVRIER 1D (Poutre) ---
        inst_name = names['inst_tower']
        try:
            # On récupère le Set créé dans def_geometrie.create_tower_1d
            region = model.rootAssembly.instances[inst_name].sets['Set_Beam_All']
            
            apply_line_load_1d(
                model, stepName, load_name, region, 
                ampName, field_mask_name, final_mag, directionVector
            )
        except KeyError:
            print("ERREUR : Set 'Set_Beam_All' introuvable. Vérifiez def_geometrie.")
            
    else:
        # --- OUVRIER 3D (Surface) ---
        surf_name_key = surf_key
        if surf_name_key not in names:
            print(f"ERREUR : Clé '{surf_name_key}' absente du dictionnaire.")
            return
            
        real_surf_name = names[surf_name_key]
        try:
            region = model.rootAssembly.surfaces[real_surf_name]
            
            apply_surface_traction_3d(
                model, stepName, load_name, region, 
                ampName, field_mask_name, final_mag, directionVector
            )
        except KeyError:
             print(f"ERREUR : Surface '{real_surf_name}' introuvable dans l'assemblage.")

def process_load_data(raw_data):
    """
    Analyse une série temporelle (Temps, Valeur).
    - Trouve la durée totale.
    - Normalise les valeurs entre -1 et 1 si elles dépassent 1.0.
    - Calcule la magnitude correspondante.
    
    Returns:
        tuple: (data_normalisee, magnitude_calculee, duree_max)
    """
    # 1. Extraction des valeurs pour analyse
    values = [abs(point[1]) for point in raw_data]
    times = [point[0] for point in raw_data]
    
    max_val = max(values) if values else 0.0
    duration = max(times) if times else 0.0
    
    # 2. Logique de Normalisation
    # Si la valeur max > 1, on normalise tout par rapport à ce max.
    # Sinon, on garde tel quel (magnitude = 1.0).
    if max_val > 1.0:
        magnitude = max_val
        # On divise chaque valeur par le max pour avoir un profil entre 0 et 1
        norm_data = tuple((t, v / max_val) for t, v in raw_data)
        print(f"   -> Données normalisées (Max initial: {max_val} -> Magnitude)")
    else:
        magnitude = 1.0
        norm_data = raw_data
        print(f"   -> Données conservées brutes (Max <= 1)")

    return norm_data, magnitude, duration

def configure_step_and_outputs(model, names, total_time, target_frames=50):
    """
    Configure ou met à jour le Step et les requêtes de sortie (Field/History).
    """
    step_name = names['step_name']
    calc_inc = total_time / float(target_frames)


    
    print(f"\n--- Configuration du Step '{step_name}' ---")
    print(f"   Durée: {total_time}s | Incrément: {calc_inc:.4f}s")

    # 1. Création / Mise à jour Step
    if step_name not in model.steps:
        model.StaticStep(name=step_name, previous='Initial')

    model.steps[step_name].setValues(
        timePeriod=total_time,
        initialInc=calc_inc,
        maxInc=calc_inc,
        minInc=1e-5
    )

    # 2. Field Output (Animation complète)
    # On force la sauvegarde à chaque incrément calculé
    if 'F-Output-1' in model.fieldOutputRequests:
        model.fieldOutputRequests['F-Output-1'].setValues(frequency=1)

    # 3. History Output (Monitoring précis)
    # Suppression préventive pour éviter les doublons/erreurs
    hist_name = 'H_Out_Top_Disp'
    if hist_name in model.historyOutputRequests:
        del model.historyOutputRequests[hist_name]
    
    set_monitor_name = names['set_monitor']
    # VERIFICATION D'EXISTENCE
    if set_monitor_name in model.rootAssembly.sets:
        model.HistoryOutputRequest(
            name=hist_name,
            createStepName=step_name,
            variables=('U', 'RF'),
            region=model.rootAssembly.sets[set_monitor_name],
            frequency=1
        )
    else:
        print(f"   [INFO] Set '{set_monitor_name}' absent : Pas de sortie historique demandée.")

    model.HistoryOutputRequest(
        name=hist_name,
        createStepName=step_name,
        variables=('U', 'RF'),
        region=model.rootAssembly.sets[names['set_monitor']],
        frequency=1
    )
    print(f"   -> Sorties configurées (Field + History sur '{names['set_monitor']}')")