# -*- coding: utf-8 -*-
from abaqus import *
from abaqusConstants import *
import odbAccess
import csv
import matplotlib
matplotlib.use('Agg') # Indispensable
import matplotlib.pyplot as plt

def get_history_data_from_set(odb, step_name, set_name_target):
    """
    Récupère les données historiques de manière robuste :
    1. Gère la casse (Majuscule/Minuscule).
    2. Gère la structure en tableau des nœuds ODB (Correction du bug Array).
    3. Trouve l'historique via le Label du nœud (sans deviner le nom de l'Instance).
    """
    
    # --- 1. Vérification du Step ---
    if step_name not in odb.steps:
        return None, None, f"Step '{step_name}' introuvable."
    step = odb.steps[step_name]
    
    # --- 2. Recherche du Set (Insensible à la casse) ---
    root_sets = odb.rootAssembly.nodeSets
    real_set_name = None
    
    # Recherche exacte ou approchante
    if set_name_target in root_sets:
        real_set_name = set_name_target
    else:
        target_upper = set_name_target.upper()
        for key in root_sets.keys():
            if key.upper() == target_upper:
                real_set_name = key
                print(f"   (Info : Set trouvé sous le nom '{real_set_name}')")
                break
    
    if real_set_name is None:
        dispo = list(root_sets.keys())
        return None, None, f"Set '{set_name_target}' introuvable. Dispo: {dispo[:5]}..."

    # --- 3. Extraction du Numéro de Nœud (CORRECTION DU BUG) ---
    try:
        nset = root_sets[real_set_name]
        
        # Le piège : nset.nodes est souvent une liste de "MeshNodeArray", pas de nœuds.
        # On tente d'accéder au premier nœud du premier tableau.
        first_item = nset.nodes[0]
        
        # Est-ce un tableau (Array) ou un objet ?
        if hasattr(first_item, 'label'):
            # C'est directement un nœud (Rare)
            target_label = first_item.label
        else:
            # C'est un tableau, il faut prendre le premier élément (Fréquent)
            target_label = first_item[0].label
            
        print(f"   (Info : Le Set pointe vers le Nœud n°{target_label})")

    except Exception as e:
        return None, None, f"Erreur lors de la lecture du Set (Set vide ?) : {e}"

    # --- 4. Recherche dans l'Historique via le Label ---
    # On ne devine pas le nom de l'instance ("INST_TOWER..."), on cherche le Label.
    # Les clés ressemblent à : "Node INSTANCE_NAME.154"
    
    target_region = None
    found_key = ""
    suffix = f".{target_label}" # ex: ".154"
    
    for key, region in step.historyRegions.items():
        # On vérifie si la clé finit par ".154" et commence par "Node"
        if key.endswith(suffix) and key.startswith("Node"):
            target_region = region
            found_key = key
            break
            
    if target_region is None:
        return None, None, f"Aucun historique trouvé pour le Nœud {target_label}."

    # --- 5. Extraction des Variables ---
    data = None
    var_found = ""
    
    # Priorité : X > Z > Y
    if 'U1' in target_region.historyOutputs:
        data = target_region.historyOutputs['U1'].data
        var_found = "U1 (X)"
    elif 'U3' in target_region.historyOutputs:
        data = target_region.historyOutputs['U3'].data
        var_found = "U3 (Z)"
    elif 'U2' in target_region.historyOutputs:
        data = target_region.historyOutputs['U2'].data
        var_found = "U2 (Y)"
        
    if not data:
        return None, None, f"Variable U absente pour {found_key}."
        
    times = [x[0] for x in data]
    values = [x[1] for x in data]
    
    info = f"Set '{real_set_name}' -> Nœud {target_label} [{var_found}]"
    return times, values, info


def export_history_to_csv(odb_name, step_name, set_name, csv_filename):
    print(f"\n--- Export CSV : {set_name} -> {csv_filename} ---")
    odb = None
    try:
        odb = odbAccess.openOdb(path=odb_name)
        times, values, info = get_history_data_from_set(odb, step_name, set_name)
        
        if times is None:
            print(f"ERREUR : {info}")
            return

        print(f"-> Succès : {info}")

        with open(csv_filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['Temps (s)', 'Deplacement (m)'])
            for t, v in zip(times, values):
                writer.writerow([t, v])
        print(f"-> Fichier CSV écrit.")

    except Exception as e:
        print(f"Erreur globale Export : {e}")
    finally:
        if odb: odb.close()


def create_plot_from_csv(csv_filename, image_filename, title="Graphique"):
    print(f"--- Génération Image : {image_filename} ---")
    try:
        times = []
        values = []
        with open(csv_filename, 'r') as f:
            reader = csv.reader(f)
            next(reader) 
            for row in reader:
                if row:
                    times.append(float(row[0]))
                    values.append(float(row[1]))
        
        if not times: 
            print("Erreur : CSV vide.")
            return

        plt.clf()
        plt.figure(figsize=(10, 6))
        plt.plot(times, values, label='Déplacement', color='navy', linewidth=2)
        plt.xlabel('Temps (s)')
        plt.ylabel('Déplacement (m)')
        plt.title(title)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()
        plt.savefig(image_filename)
        plt.close()
        print("-> Image créée.")
        
    except IOError:
        print(f"Erreur : Le fichier {csv_filename} n'existe pas.")
    except Exception as e:
        print(f"Erreur Graphique : {e}")