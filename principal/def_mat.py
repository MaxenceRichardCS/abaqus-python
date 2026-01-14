from abaqusConstants import *

def create_and_assign_solid_material(model, part, mat_name, props):
    """
    Crée un matériau, une section solide, et l'assigne à toute la pièce.

    Args:
        model: Le modèle Abaqus.
        part: L'objet Part auquel appliquer le matériau.
        mat_name: Nom donné au matériau (ex: 'Steel').
        props: Dictionnaire contenant:
            - 'density': Masse volumique (ex: 7850.0)
            - 'young': Module d'Young (ex: 210e9)
            - 'poisson': Coefficient de Poisson (ex: 0.3)
    """
    
    # --- Etape 1 : Création du Matériau ---
    # On vérifie s'il existe déjà pour ne pas le recréer en double
    if mat_name not in model.materials:
        mat = model.Material(name=mat_name)
        
        # Propriétés Elastiques (Isotropes)
        if 'young' in props and 'poisson' in props:
            mat.Elastic(table=((props['young'], props['poisson']), ))
            
        # Densité (Requise pour les calculs dynamiques ou de gravité)
        if 'density' in props:
            mat.Density(table=((props['density'], ), ))
    
    # --- Etape 2 : Création de la Section ---
    # Une section fait le lien entre le matériau et la géométrie
    section_name = 'Section_' + mat_name
    if section_name not in model.sections:
        model.HomogeneousSolidSection(
            name=section_name, 
            material=mat_name, 
            thickness=None # Non utilisé pour les solides
        )
        
    # --- Etape 3 : Création du Set géométrique ---
    # Pour assigner une section, il faut cibler des cellules (Cells)
    # Ici, on prend toutes les cellules de la pièce
    set_name = 'Set_Material_WholePart'
    region = part.Set(name=set_name, cells=part.cells[:])
    
    # --- Etape 4 : Assignation de la Section ---
    part.SectionAssignment(
        region=region, 
        sectionName=section_name, 
        offset=0.0, 
        offsetType=MIDDLE_SURFACE, 
        offsetField='', 
        thicknessAssignment=FROM_SECTION
    )
    
    print("Materiau '{}' applique a la part '{}'.".format(mat_name, part.name))

