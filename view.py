from models import joueurs, Tournoi, tournois
import datetime
from exception import NotYetAvailable


def print_num_choix(num_choix, choice):
    print(f"[{num_choix}] {choice}")


def message_tournois_terminer():
    print("-------------------------")
    print("/!\\ Tournoi terminé /!\\ ")
    print("-------------------------")


def print_separation():
    print("------")


def afficher_matchs(tournoi_choisi):
    for match in tournoi_choisi.last_turn.matchs:
        print(
            f"Blancs: {match.joueur_blanc}({match.joueur_blanc.classement}) vs "
            f"Noirs:{match.joueur_noir}({match.joueur_noir.classement})"
        )
    print(f"Tour n°{len(tournoi_choisi.tours)} / {tournoi_choisi.nombre_de_tours}")


def joueurs_data():
    for i, joueur in enumerate(joueurs, start=1):
        print_separation()
        print(f"Joueur n°{i}:")
        print("Nom" + " : " + joueur.nom)
        print("Prenom" + " : " + joueur.prenom)
        print(f"Date : {joueur.date_de_naissance.strftime('%d/%m/%Y')}")
        print("sexe" + " : " + joueur.sexe)
        print(f"classement : {joueur.classement}")

        print("\n")


def lister_joueurs_tournoi(tournoi_choisi: Tournoi):
    for joueur in tournoi_choisi.joueurs:
        print(joueur)


def lister_info_tournoi(tournoi_choisi: Tournoi):
    print(tournoi_choisi.nom)
    if tournoi_choisi.tournoi_cloture:
        message_tournois_terminer()
    print(tournoi_choisi.lieu)
    date: datetime.datetime = tournoi_choisi.date
    print(date.strftime("%d/%m/%Y"))
    print(tournoi_choisi.description)
    print(tournoi_choisi.nombre_de_tours)
    print(tournoi_choisi.controle_du_temps)


def historique_general():
    for tournoi in tournois:
        print(f"Non du tournoi: {tournoi.nom} du {tournoi.date} à {tournoi.lieu}")
        tableau_des_scores(tournoi)
        print_separation()


def tableau_des_scores(tournoi_choisi: Tournoi):
    if (
        tournoi_choisi.scores
    ):  # est-ce que le dict tournoi_choisi.scores est vide, si oui on va dans le else:
        for i, (joueur, score) in enumerate(
            sorted(
                list(tournoi_choisi.scores.items()),
                key=lambda i: (i[1], i[0].classement),
                reverse=True,
            ),
            start=1,
        ):
            print(f"[{i}]{joueur}: {score}")
    else:
        raise NotYetAvailable(
            "Veuillez lancer au moin le 1er tour avant de voir le tableau des scores !"
        )


def afficher_pairs_tournois(tournoi_choisi: Tournoi):
    pairs_du_tournois = tournoi_choisi.generer_paires()
    for pairs in pairs_du_tournois:
        print(f"joueur:{pairs[0]} vs joueur:{pairs[1]}")
