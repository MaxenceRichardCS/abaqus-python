from abaqus import mdb


def lancement_job(model):
    job_name = 'Job-GBS-Tower'

    # Création du Job
    mdb.Job(name=job_name, model=model, description='Calcul GBS et Tour')

    # Soumission du Job
    print("Soumission du job {}...".format(job_name))
    mdb.jobs[job_name].submit()

    # Attente de la fin du calcul
    print("Calcul en cours...")
    mdb.jobs[job_name].waitForCompletion()

    print("Calcul terminé. Le fichier .odb est généré.")