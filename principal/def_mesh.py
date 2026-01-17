# -*- coding: utf-8 -*-
# =============================================================================
# FICHIER : def_mesh.py
# DESCRIPTION : Gestion du maillage (Discrétisation) des pièces.
#               Définit la taille, la forme et le type des éléments finis.
# =============================================================================

from abaqus import *
from abaqusConstants import *
import mesh # Indispensable pour utiliser mesh.ElemType

# =============================================================================
# MAILLAGE DE LA TOUR (HEXAÈDRES - C3D8R)
# =============================================================================

def MeshTower(part_obj, size):
    """
    Applique un maillage structuré en "Briques" (Hexaèdres) sur la Tour.
    Comme la tour est un cylindre simple, on peut utiliser la technique de balayage (Sweep),
    qui est très précise et économique.
    """
    print(f"\n--- Maillage de la Tour (Taille demandée : {size}) ---")
    
    # 1. Ensemencement (Seeding)
    # On définit la taille cible des éléments sur les arêtes.
    part_obj.seedPart(size=size, deviationFactor=0.1, minSizeFactor=0.1)

    # 2. Stratégie de maillage (Controls)
    # - HEX   : On veut des éléments cubiques (briques).
    # - SWEEP : On balaie la section le long de l'axe (parfait pour les tubes).
    part_obj.setMeshControls(
        regions=part_obj.cells,
        elemShape=HEX,
        technique=SWEEP
    )

    # 3. Choix du type d'élément
    # C3D8R : Cube 3D à 8 noeuds, Intégration Réduite.
    # C'est le standard pour l'acier : robuste et ne "verrouille" pas en cisaillement.
    elemType = mesh.ElemType(elemCode=C3D8R)

    part_obj.setElementType(
        regions=(part_obj.cells,),
        elemTypes=(elemType, )
    )

    # 4. Génération
    part_obj.generateMesh()

    # Bilan
    nb_noeuds = len(part_obj.nodes)
    nb_elems = len(part_obj.elements)
    print(f"-> Terminé : {nb_noeuds} noeuds / {nb_elems} éléments (C3D8R).")

def MeshTower1D(part, size):
    """Maillage 1D avec éléments B31"""
    print(f"--- Maillage Tour 1D (Taille={size}) ---")
    
    # Seed
    part.seedPart(size=size, deviationFactor=0.1)
    
    # Type d'élément : B31 (Beam, 3D, 2-node, linear)
    elem_type = mesh.ElemType(elemCode=B31, elemLibrary=STANDARD)
    
    # On applique sur toutes les arêtes (il n'y en a qu'une en 1D)
    part.setElementType(regions=(part.edges,), elemTypes=(elem_type,))
    
    part.generateMesh()
    print(f"-> Maillage généré : {len(part.nodes)} nœuds, {len(part.elements)} éléments.")


# =============================================================================
# MAILLAGE DU GBS (TÉTRAÈDRES - C3D4)
# =============================================================================

def MeshGBS(part_obj, size):
    """
    Applique un maillage libre en "Pyramides" (Tétraèdres) sur le GBS.
    La géométrie fusionnée (Cône + Cylindre + Plateau) est trop complexe pour faire des cubes.
    On utilise des tétraèdres linéaires (C3D4) pour limiter drastiquement le nombre de noeuds.
    """
    print(f"\n--- Maillage du GBS (Taille demandée : {size}) ---")

    # 1. Ensemencement (Seeding) avec tolérance
    # deviationFactor=0.4 : On autorise les éléments à s'éloigner un peu de la courbe parfaite.
    # Cela permet de réduire le nombre d'éléments dans les zones courbes non critiques.
    part_obj.seedPart(size=size, deviationFactor=0.4, minSizeFactor=0.1)
    
    # 2. Stratégie de maillage (Controls)
    # - TET  : Tétraèdres (Pyramides à base triangulaire).
    # - FREE : Maillage libre (l'algorithme remplit le volume comme il peut).
    part_obj.setMeshControls(
        regions=part_obj.cells, 
        elemShape=TET, 
        technique=FREE
    )
    
    # 3. Choix du type d'élément (Optimisation Version Étudiante)
    # C3D4 : Tétraèdre linéaire (4 noeuds).
    # Contre-exemple : Le C3D10 (quadratique) a 10 noeuds. Pour un même volume,
    # le C3D4 consomme ~3x moins de noeuds, évitant de dépasser la limite de 1000 noeuds.
    elemType = mesh.ElemType(elemCode=C3D4)

    part_obj.setElementType(
        regions=(part_obj.cells,),
        elemTypes=(elemType, )
    )
    
    # 4. Génération
    part_obj.generateMesh()
    
    # Bilan
    nb_noeuds = len(part_obj.nodes)
    nb_elems = len(part_obj.elements)
    print(f"-> Terminé : {nb_noeuds} noeuds / {nb_elems} éléments (C3D4).")