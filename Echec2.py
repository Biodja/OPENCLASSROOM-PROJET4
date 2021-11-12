
from formulaire import Formulaire
from fields import AskJoueursField, Field, ChoiceField, IntField, dateField
from action import Action
from models import Tournoi, Blitz, Bullet, CoupRapide, joueurs, tournois
from menu import Menu, ACTION_BREAK, QUIT
from view import historique_general
from controllers import (
    info_joueurs,
    lister_joueurs_tournoi,
    lister_info_tournoi,
    lancer_tour_suivant,
    selection_gagnant_match,
    tableau_des_scores,
    ajouter_joueurs_tournois,
    afficher_pairs_tournois,
)

YES_NO_TO_BOOL = {
    "O": True,
    "o": True,
    "N": False,
    "n": False,
}


"""
class MenuLancerTournoi(Menu):
    def __init__(self):
        super().__init__("Lancement du tournoi", "début du tournois"), [Action, Action, ....]
"""


if __name__ == "__main__":
    # Initialisation du programe, et debut du tournois

    formulaire_creation_tournoi = Formulaire(
        "Formulaire création tournoi",
        [
            Field("nom", "Nom tournoi"),
            Field("lieu", "Lieu du tournoi"),
            dateField("date", "Date du tournoi"),
            IntField("nombre_de_tours", "Nombre de tours"),
            ChoiceField(
                "controle_du_temps",
                "Quel est votre méthode de contrôle du temps ?",
                [Blitz(), Bullet(), CoupRapide()],
            ),
            Field("description", "Description"),
        ],
        Tournoi,
    )
    lancer_tournois = Menu(
        "Lancement du tournois",
        "Debut du tournois",
        [
            Action("Générer les paires de joueurs", afficher_pairs_tournois),
            Action("Lancer le tour suivant", lancer_tour_suivant),
            Action("Déclarer gagnant match", selection_gagnant_match),
            Action("Tableau des scores", tableau_des_scores),
            ACTION_BREAK,
        ],
    )

    ajouter_un_joueurs = Formulaire(
        "Ajoutez les joueurs",
        [
            ChoiceField("tournoi_choisi", "Tournoi", tournois),
            AskJoueursField(
                "joueurs", joueurs, IntField("nb_joueurs", "Nombre de participants")
            ),
        ],
        ajouter_joueurs_tournois,
    )

    menu_gestion_un_tournoi = Menu(
        "Gestion d'un tournoi",
        "Gestion tournoi",
        [
            Action("Lister les joueurs", lister_joueurs_tournoi),
            Action("Afficher informations globales", lister_info_tournoi),
            Action("Ajoutez les joueurs", ajouter_un_joueurs.executer),
            Action("Lancer le tournois", lancer_tournois.executer),
            ACTION_BREAK,
        ],
    )

    form_gestion_un_tournoi = Formulaire(
        "Formulaire choix tournoi",
        [ChoiceField("tournoi_choisi", "Sur quel tournoi intervenir", tournois)],
        menu_gestion_un_tournoi.executer,
    )
    menu_gestion_tournoi = Menu(
        "Tournois",
        "Gestion tournois",
        [
            Action("Créer tournoi", formulaire_creation_tournoi.executer),
            Action("Ajoutez les joueurs", ajouter_un_joueurs.executer),
            Action("Gérer un tournoi", form_gestion_un_tournoi.executer),
            ACTION_BREAK,
        ],
    )
    menu_gestion_joueurs = Menu(
        "Menu gestion joueurs",
        "Gestion joueurs",
        [Action("Créer joueur", info_joueurs), ACTION_BREAK],
    )

    menu_principal = Menu(
        "Menu principal",
        "Voici le menu principal pour gérer les tournois d'échecs",
        [
            Action("Ajoutez les joueurs", menu_gestion_joueurs.executer),
            menu_gestion_tournoi,
            Action("Historique", historique_general),
            QUIT,
        ],
    )

    action_choisie: Action = menu_principal.executer()
    action_choisie.executer()
