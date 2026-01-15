from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup
import regionToolset

# =============================================================================
# FONCTION : ENCASTREMENT DE LA BASE (SOL)
# =============================================================================

def encastrement_GBS(model, names):
    """
    Bloque tous les mouvements de la base du GBS (Encastrement parfait).
    Utilise le dictionnaire 'names' pour cibler la bonne instance dynamiquement.
    """
    print("\n--- Application de l'Encastrement (Sol) ---")

    a = model.rootAssembly
    
    # 1. Récupération du nom de l'instance depuis le dictionnaire
    # Plus besoin d'écrire 'GBS-1' en dur ici !
    inst_name = names['inst_gbs'] 
    
    # Vérification de sécurité pour éviter le crash si l'instance manque
    if inst_name not in a.instances:
        raise KeyError(f"ERREUR : L'instance '{inst_name}' est introuvable dans l'assemblage.")
        
    inst_gbs = a.instances[inst_name]

    # 2. Sélection géométrique des faces au sol (Bounding Box)
    # On cherche tout ce qui est à Y=0 (avec une tolérance +/- 0.1)
    bottom_faces = inst_gbs.faces.getByBoundingBox(
        xMin=-1000.0, yMin=-0.1, zMin=-1000.0,
        xMax=1000.0,  yMax=0.1,  zMax=1000.0
    )

    # Vérification que la sélection a marché
    if len(bottom_faces) == 0:
        print(f"ERREUR CRITIQUE : Aucune face trouvée à Y=0 sur l'instance {inst_name}.")
        return

    # 3. Création du Set (Groupe nommé)
    # Abaqus a besoin d'un 'Set' pour appliquer une BC.
    region_base = a.Set(name='Set_Base_GBS', faces=bottom_faces)

    # 4. Application de la Condition Limite (Encastre)
    # On l'applique sur le Step 'Initial' pour qu'elle soit active tout le temps.
    model.EncastreBC(
        name='BC_Encastrement_Sol',
        createStepName='Initial', 
        region=region_base
    )

    print(f"-> Succès : {len(bottom_faces)} face(s) encastrée(s) à la base de '{inst_name}'.")

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