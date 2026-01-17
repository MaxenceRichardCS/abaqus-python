# -*- coding: utf-8 -*-
from abaqus import *
from abaqusConstants import *
import os
import glob


def lancement_job(model, job_name='Job-GBS-Tower'):
    """
    Crée le Job, le soumet et renvoie l'objet Job pour l'attente.
    """
    print(f"\n--- Création du Job : {job_name} ---")
    
    # 1. Nettoyage
    if job_name in mdb.jobs:
        del mdb.jobs[job_name]
        
    # 2. Création du Job (Version corrigée)
    # J'ai retiré 'globalJob' et 'paramFile' qui provoquent l'erreur.
    my_job = mdb.Job(
        name=job_name, 
        model=model.name,
        description='Simulation GBS + Tour', 
        type=ANALYSIS, 
        atTime=None, 
        waitMinutes=0, 
        waitHours=0, 
        queue=None,             # Remplaçant standard (souvent None en local)
        memory=90, 
        memoryUnits=PERCENTAGE, 
        getMemoryFromAnalysis=True, 
        explicitPrecision=SINGLE, 
        nodalOutputPrecision=SINGLE, 
        echoPrint=OFF, 
        modelPrint=OFF, 
        contactPrint=OFF, 
        historyPrint=OFF, 
        userSubroutine='', 
        scratch='', 
        resultsFormat=ODB, 
        multiprocessingMode=DEFAULT, 
        numCpus=1, 
        numDomains=1, 
        numGPUs=0
    )
    
    # 3. Soumission
    print(f"-> Soumission au solveur...")
    my_job.submit()
    
    # On renvoie l'objet pour que le main.py puisse faire le .waitForCompletion()
    return my_job


def clean_abaqus_temp_files(job_name):
    """
    Supprime les fichiers auxiliaires générés par Abaqus (.log, .lck, .msg, etc.)
    ainsi que les fichiers d'erreurs globaux (.exception, abaqus.rpy).
    
    Ne touche PAS aux résultats (.odb, .csv, .png) ni aux scripts (.py).
    """
    print(f"\n--- Nettoyage du dossier de travail ---")
    
    # 1. Liste des extensions spécifiques au Job à supprimer
    # .lck : Verrou (inutile après calcul)
    # .log : Journal (utile si bug, sinon poubelle)
    # .msg : Messages détaillés du solveur
    # .prt : Détails des parts
    # .sta : Status (résumé des incréments)
    # .com : Fichier de commande
    # .sim : Base de données simulation
    # .ipm : Internal Process Message
    # .ipm : Recovery File
    extensions_to_delete = ['.lck', '.log', '.msg', '.prt', '.sta', '.com', '.sim', '.ipm', '.dat','.rec']
    
    count = 0
    
    # A. Suppression des fichiers liés au JOB
    for ext in extensions_to_delete:
        filename = job_name + ext
        if os.path.exists(filename):
            try:
                os.remove(filename)
                count += 1
            except Exception as e:
                print(f"   Impossible de supprimer {filename} : {e}")

    # B. Suppression des fichiers "Poubelle" globaux (rpy, exception)
    # abaqus.rpy* : Ce sont les macros enregistrées automatiquement (s'accumulent vite !)
    for f in glob.glob("abaqus.rpy*"):
        try:
            os.remove(f)
            count += 1
        except: pass

    # *.exception : Les fichiers dump en cas de crash
    for f in glob.glob("*.exception"):
        try:
            os.remove(f)
            count += 1
        except: pass
        
    print(f"-> Nettoyage terminé : {count} fichiers supprimés.")