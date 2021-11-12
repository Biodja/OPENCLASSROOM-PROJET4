from exception import NotYetAvailable
import datetime
from models import Joueur, Tournoi, save_to_db
from fields import UserException
from views.errors import afficher_erreur
from fields import ChoiceField
from formulaire import Formulaire
from view import (
    message_tournois_terminer,
    print_separation,
    joueurs_data,
    lister_info_tournoi,
    lister_joueurs_tournoi,
    tableau_des_scores,
    afficher_pairs_tournois,
    afficher_matchs,
)


def ask_user(
    message="",
    message_error="Valeur invalide",
    validator=lambda s: len(s) > 0,
    convertor=lambda s: s,
):
    user_input = ""
    while True:
        user_input = input(message)
        try:
            user_input = convertor(user_input)
        except Exception as e:
            print(message_error, e)
            continue
        if not validator(user_input):
            print(message_error)
        else:
            return user_input


def info_joueurs():
    print_separation()
    nom = ask_user(f"Entre le nom du joueur : ")
    prenom = ask_user(f"Entre le prenom du joueur : ")
    date_de_naissance = ask_user(
        f"Enter date du joueur : ",
        message_error="Le format date (**/**/****) doit être respecter!",
        convertor=lambda s: datetime.datetime.strptime(s, "%d/%m/%Y"),
        validator=lambda _: True,
    )
    sexe = ask_user(
        f"Enter sexe du joueur H/F : ",
        message_error="Doit être H ou F",
        validator=lambda s: s in {"H", "F"},
        convertor=lambda s: s.upper(),
    )
    classement = ask_user(
        f"Enter classement du joueur : ",
        message_error=" le classement doit être un nombre positif",
        validator=lambda n: n > 0,
        convertor=int,
    )
    print_separation()
    joueur = Joueur(nom, prenom, date_de_naissance, sexe, classement)
    save_to_db()
    return joueur


def ajouter_joueurs_tournois(tournoi_choisi: Tournoi, joueurs):
    tournoi_choisi.ajouter_joueurs(joueurs=joueurs)
    save_to_db()


def lancer_tour_suivant(tournoi_choisi: Tournoi):
    if tournoi_choisi.tournoi_cloture:
        message_tournois_terminer()
        return
    try:
        tournoi_choisi.passer_au_tour_suivant()
    except UserException as e:
        afficher_erreur(e)
    else:
        afficher_matchs(tournoi_choisi)
        save_to_db()


def selection_gagnant_match(tournoi_choisi: Tournoi):
    def post_formulaire(tournoi_choisi, match, gagnant):
        try:
            if gagnant == "Blancs":
                gagnant = match.joueur_blanc
            elif gagnant == "Noirs":
                gagnant = match.joueur_noir
            else:
                gagnant = None
            match.finir_match(gagnant)
        except NotYetAvailable as e:
            afficher_erreur(e)

    if not tournoi_choisi.last_turn:
        raise NotYetAvailable(
            "Veuillez générer les pairs avant de déclaré un gagnant !"
        )
    reponses = Formulaire(
        "Choisir match",
        [
            ChoiceField("match", "Quel Match ?", tournoi_choisi.last_turn.matchs),
            ChoiceField(
                "gagnant", "Quelle couleur a gagné", ["Blancs", "Noirs", "Match nul"]
            ),
        ],
        post_formulaire,
    ).executer(tournoi_choisi=tournoi_choisi)
    save_to_db()
