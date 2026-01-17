from abaqusConstants import MIDDLE_SURFACE, FROM_SECTION, DURING_ANALYSIS, LINEAR, N1_COSINES

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
        # CORRECTION : Utilisation du constructeur direct
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
    # Nettoyage si le set existe déjà
    if set_name in part.sets: del part.sets[set_name]
    
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

    print(f"Materiau {mat_name} applique a la part {part.name} (Solid).")


def create_and_assign_beam_material(model, part, mat_name, props, param):
    """
    Pour la tour 1D : Crée le matériau, le profil Tube et la Section Beam.
    Définit aussi l'orientation de la poutre.
    """
    print("--- Assignation Matériau Poutre (1D) ---")
    
    # 1. Matériau
    if mat_name not in model.materials:
        # CORRECTION : Syntaxe correcte pour créer le matériau
        m = model.Material(name=mat_name)
        m.Elastic(table=((props['young'], props['poisson']), ))
        m.Density(table=((props['density'], ), ))

    # 2. Profil (Tube constant avec Rayon Moyen)
    r_moy = param['r_moy']
    thick = param['thickness_tower']
    
    prof_name = 'Profile_Tower_Pipe'
    if prof_name in model.profiles: del model.profiles[prof_name]
    
    # PipeProfile prend r (rayon) et t (épaisseur)
    model.PipeProfile(name=prof_name, r=r_moy, t=thick)
    
    # 3. Section Poutre
    sec_name = 'Section_Tower_Beam'
    if sec_name in model.sections: del model.sections[sec_name]
        
    model.BeamSection(name=sec_name, integration=DURING_ANALYSIS, 
                      profile=prof_name, material=mat_name, 
                      temperatureVar=LINEAR)
    
    # 4. Assignation
    # Le Set 'Set_Beam_All' doit avoir été créé dans def_geometrie.create_tower_1d
    if 'Set_Beam_All' not in part.sets:
        print("ERREUR : Le Set 'Set_Beam_All' est introuvable sur la part.")
        return

    region = part.sets['Set_Beam_All']
    part.SectionAssignment(region=region, sectionName=sec_name)
    
    # 5. Orientation de la poutre (CRITIQUE : Sans ça, le calcul plante)
    # On définit le vecteur n1 (direction normale locale).
    # Pour une poutre verticale selon Y, on oriente n1 vers -Z (0,0,-1).
    part.assignBeamSectionOrientation(region=region, method=N1_COSINES, n1=(0.0, 0.0, -1.0))
    
    print("-> Section Poutre et Orientation assignées.")