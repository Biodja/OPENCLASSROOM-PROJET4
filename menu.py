from controllers import tournoi
from typing import List
from action import Action
from views.errors import afficher_erreur
from exception import UserException

QUIT = Action("Arrêter programme", callback=quit)
ACTION_BREAK = Action("Retourner en arrière", callback=lambda: None)


class Menu(Action):
    def __init__(self, titre, sous_titre, choix: List[Action]):
        self.titre = titre
        self.sous_titre = sous_titre
        self.intitule = titre
        self.callback = self.executer
        self.choix = choix

    def _afficher(self):
        START = 1
        while True:
            print(self.titre.center(40, "-").upper())
            print(self.sous_titre)
            for num_choix, choix in enumerate(self.choix, start=START):
                print(f"[{num_choix}] {choix}")
            option_choisie = input("Votre choix ?")
            try:
                return self.choix[int(option_choisie) - START]
            except IndexError:
                afficher_erreur(UserException("Veuillez choisir une option valide"))
            except ValueError:
                afficher_erreur(UserException("Veuillez taper un nombre"))

    def executer(self, args=tuple(), kwargs={}, **kw):
        while True:
            try:
                choix = self._afficher()
            except KeyboardInterrupt:
                break
            if choix is ACTION_BREAK:
                break
            choix.executer(*args, **kwargs, **kw)


class Menutournois(Action):
    def __init__(self, titre, sous_titre, choix: List[Action]):
        self.titre = titre
        self.sous_titre = sous_titre
        self.intitule = titre
        self.callback = self.executer
        self.choix = choix

    def _afficher(self):
        print(f"Tour n°{len(tournoi_choisi.tours)} / {tournoi_choisi.nombre_de_tours}")

        START = 1
        while True:
            print(self.titre.center(40, "-").upper())
            print(self.sous_titre)
            for num_choix, choix in enumerate(self.choix, start=START):
                print(f"[{num_choix}] {choix}")
            option_choisie = input("Votre choix ?")
            try:
                return self.choix[int(option_choisie) - START]
            except IndexError:
                afficher_erreur(UserException("Veuillez choisir une option valide"))
            except ValueError:
                afficher_erreur(UserException("Veuillez taper un nombre"))

    def executer(self, args=tuple(), kwargs={}, **kw):
        while True:
            try:
                choix = self._afficher()
            except KeyboardInterrupt:
                break
            if choix is ACTION_BREAK:
                break
            choix.executer(*args, **kwargs, **kw)
