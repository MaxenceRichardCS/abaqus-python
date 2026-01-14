from abaqus import mdb
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup


## Améliorer la taille du seed part 
def MeshGBS(part_obj):
    """
    Applique un maillage tétraédrique linéaire (C3D4) optimisé
    pour la version étudiante (limite de noeuds).
    """
    # -------------------------------------------------------
    # 1. Application des graines (Seeds)
    # -------------------------------------------------------
    # deviationFactor=0.4 : Tolérance élevée pour accepter 
    # que les gros éléments ne collent pas parfaitement à la courbure.
    part_obj.seedPart(size=5.0, deviationFactor=0.4, minSizeFactor=0.1)
    
    # -------------------------------------------------------
    # 2. Contrôle du maillage
    # -------------------------------------------------------
    # On force des tétraèdres (TET) en méthode libre (FREE)
    # C'est la seule méthode capable de mailler des géométries complexes
    part_obj.setMeshControls(
        regions=part_obj.cells, 
        elemShape=TET, 
        technique=FREE
    )
    
    # -------------------------------------------------------
    # 3. Type d'élément (Économie de noeuds)
    # -------------------------------------------------------
    # On impose EXCLUSIVEMENT du C3D4 (Tétraèdre linéaire à 4 noeuds).
    # Cela génère environ 2.5x moins de noeuds que le C3D10 standard.
    part_obj.setElementType(
        regions=(part_obj.cells,),
        elemTypes=(
            mesh.ElemType(elemCode=C3D4),
        )
    )
    
    # -------------------------------------------------------
    # 4. Génération
    # -------------------------------------------------------
    part_obj.generateMesh()
    
    # Vérification console pour le debug
    print('Maillage GBS termine. Nombre de noeuds :', len(part_obj.nodes))


def MeshTower(part_obj):
    """
    Applique le maillage hexaédrique par balayage (Sweep) spécifique à la tour.
    """
    # Application des graines avec facteurs de déviation
    part_obj.seedPart(size=6, deviationFactor=0.1, minSizeFactor=0.1)

    # Définition des contrôles de maillage (Hexaèdres par balayage)
    part_obj.setMeshControls(
        regions=part_obj.cells,
        elemShape=HEX,
        technique=SWEEP
    )

    # Préparation des types d'éléments
    elemType1 = mesh.ElemType(elemCode=C3D8R)    # Hexaèdre linéaire réduit
    elemType2 = mesh.ElemType(elemCode=C3D20R)   # Hexaèdre quadratique réduit

    # Application des types d'éléments
    part_obj.setElementType(
        regions=(part_obj.cells,),
        elemTypes=(elemType1, elemType2)
    )

    # Génération du maillage
    part_obj.generateMesh()

    print('Maillage de la tour termine. Nombre de noeuds :', len(part_obj.nodes))



