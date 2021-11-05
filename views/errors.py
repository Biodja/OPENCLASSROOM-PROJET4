def afficher_erreur(e, msg=""):
    print("Impossible de réaliser l'action demandée pour la raison suivante : ", str(e))
    if msg:
        print(msg)


def afficher_erreur_champ(e, champ):
    print(f"Champ invalide: {champ.nom}")
    print(f"Raison: {str(e)}")
