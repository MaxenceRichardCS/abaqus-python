from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup
import regionToolset

# =============================================================================
# FONCTION : ENCASTREMENT DE LA BASE (SOL)
# =============================================================================

def encastrement_GBS(model):
    """
    Bloque tous les mouvements de la base du GBS (Encastrement parfait).
    S'applique sur le Step 'Initial' pour être actif dès le début de la simulation.
    """
    print("\n--- Application de l'Encastrement (Sol) ---")

    # 1. Récupération de l'instance
    # On travaille sur l'assemblage racine qui contient les instances positionnées
    a = model.rootAssembly
    inst_gbs = a.instances['GBS-1']

    # 2. Sélection géométrique des faces au sol
    # On utilise une "Bounding Box" (Boîte englobante) pour capturer les faces à Y=0.
    # On prend une petite marge (+/- 0.1) pour être sûr de ne rien rater à cause des arrondis numériques.
    bottom_faces = inst_gbs.faces.getByBoundingBox(
        xMin=-1000.0, yMin=-0.1, zMin=-1000.0,
        xMax=1000.0,  yMax=0.1,  zMax=1000.0
    )

    # Vérification de sécurité
    if len(bottom_faces) == 0:
        print("ERREUR : Aucune face trouvée à Y=0 pour l'encastrement du GBS.")
        return

    # 3. Création du Set (Groupe)
    # Abaqus a besoin d'un 'Set' nommé pour appliquer une condition limite.
    region_base = a.Set(name='Base_GBS_Set', faces=bottom_faces)

    # 4. Application de la Condition Limite (BC)
    # Type : Encastre (U1=U2=U3=0 et UR1=UR2=UR3=0)
    # Step : 'Initial' (Indispensable pour que la structure soit stable dès t=0)
    model.EncastreBC(
        name='BC_Encastrement_Base',
        createStepName='Initial', 
        region=region_base
    )

    print(f"-> Succès : {len(bottom_faces)} face(s) encastrée(s) à la base.")


# =============================================================================
# FONCTION : COLLAGE RIGIDE TOUR / GBS (INTERACTION TIE)
# =============================================================================

def create_tie_tower_gbs(model, inst_tower, inst_gbs, h_interface):
    """
    Crée une liaison rigide ('Tie') entre la Tour et le GBS.
    C'est l'équivalent d'une soudure ou d'un boulonnage indéformable.
    
    Utilise la syntaxe moderne Abaqus : 
    - Main (Maître) : La surface la plus rigide ou avec le maillage le plus grossier (Ici le GBS).
    - Secondary (Esclave) : La surface la plus fine (Ici la Tour).
    """
    print(f"\n--- Création du Tie (Collage) à l'altitude Y={h_interface} ---")
    
    a = model.rootAssembly

    # 1. Définition de la Surface Secondary (La Tour)
    # On cherche les faces de la tour situées exactement à la hauteur de l'interface.
    faces_tower = inst_tower.faces.getByBoundingBox(
        yMin=h_interface - 0.1,
        yMax=h_interface + 0.1
    )
    
    # Sécurité : Si la géométrie a changé et qu'on ne trouve rien, on arrête tout.
    if len(faces_tower) == 0:
        raise ValueError(f"ERREUR CRITIQUE : Aucune face de la TOUR trouvée à Y={h_interface}.")

    surf_secondary = a.Surface(
        name='Surf_Tie_Secondary_Tower',
        side1Faces=faces_tower
    )

    # 2. Définition de la Surface Main (Le GBS)
    # Idem, on capture le haut du cône en béton.
    faces_gbs = inst_gbs.faces.getByBoundingBox(
        yMin=h_interface - 0.1,
        yMax=h_interface + 0.1
    )

    if len(faces_gbs) == 0:
        raise ValueError(f"ERREUR CRITIQUE : Aucune face du GBS trouvée à Y={h_interface}.")

    surf_main = a.Surface(
        name='Surf_Tie_Main_GBS',
        side1Faces=faces_gbs
    )

    # 3. Création de la Contrainte Tie
    tie_name = 'Constraint_Tie_Tower_GBS'

    # Nettoyage préventif : on supprime l'ancienne contrainte si elle existe déjà
    if tie_name in model.constraints:
        del model.constraints[tie_name]
        print(f"-> Ancienne contrainte '{tie_name}' supprimée.")

    # Paramètres importants du Tie :
    # - positionToleranceMethod=COMPUTED : Abaqus calcule tout seul la tolérance de distance.
    # - adjust=ON : Déplace légèrement les nœuds esclaves pour fermer les petits espaces (snap).
    # - tieRotations=ON : Bloque aussi les rotations (indispensable pour un encastrement parfait).
    model.Tie(
        name=tie_name,
        main=surf_main,           # Surface Maître (Béton)
        secondary=surf_secondary, # Surface Esclave (Acier)
        positionToleranceMethod=COMPUTED,
        adjust=ON,
        tieRotations=ON,
        thickness=ON
    )

    print("-> Succès : Liaison Tie créée entre la Tour et le GBS.")