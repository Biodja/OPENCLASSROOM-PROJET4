import datetime
from view import print_num_choix
from exception import UserException
from views.errors import afficher_erreur_champ


class Field:
    def __init__(
        self,
        nom,
        question,
        convertisseur=lambda s: s,
        validateur=lambda s: True,
        show_error_function=afficher_erreur_champ,
    ):
        # convertisseur: fonction qui prend la donnée brute de l'utilisateur (str)
        # et qui retourne la donnée dans un format utilisable par Python et nos modèles
        # validateur: fonction qui prend la donnée brute de l'utilisateur (str)
        # et qui retourne True si la donnée est dans un format considéré comme valide
        # sinon False
        self.nom = nom
        self.question = question
        self.convertisseur = convertisseur
        self.validateur = validateur
        self.error_view = lambda e: show_error_function(e, self)

    def poser_question(self):
        while True:
            data = input(f"{self.question}: ")
            if self.validateur(data):
                try:
                    return self.convertisseur(data)
                except Exception as e:
                    self.error_view(e)
            else:
                self.error_view(UserException("Champ invalide"))


class IntField(Field):
    def __init__(self, nom, question):
        super().__init__(
            nom,
            question,
            int,
            str.isdigit,
            show_error_function=lambda e, s: afficher_erreur_champ(
                UserException("Veuillez taper un nombre entier"), s
            ),
        )


class dateField(Field):
    def __init__(self, nom, question):
        self.nom = nom
        self.question = question
        self.date = lambda s: datetime.datetime.strptime(s, "%d/%m/%Y")

    def poser_question(self):
        while True:
            try:
                raw_data = input(f"{self.question}: ")
                return self.date(raw_data)

            except ValueError:
                afficher_erreur_champ(
                    "Le format date (**/**/****) doit être respecter!", self
                )


class ChoiceField(Field):
    def __init__(self, nom, question, choices):
        self.nom = nom
        self.question = question
        self.choices: list = choices

    def poser_question(self):
        if not self.choices:
            raise Exception(
                "Veuillez créer un tournoi avant de crée les joueurs / géré un tournois ! "
            )
        while True:
            print(self.question)
            for num_choix, choice in enumerate(self.choices, start=1):
                print_num_choix(num_choix, choice)
            option_choisi: str = input("Votre choix?")
            try:
                if int(option_choisi) - 1 < 0:
                    raise ValueError("Veuillez choisir une option valide")
                return self.choices[int(option_choisi) - 1]
            except (IndexError, ValueError) as e:
                afficher_erreur_champ(e, self)


class MultipleChoiceField(ChoiceField):
    def __init__(self, nom, question, choices, nb_choices, unique=False):
        super().__init__(nom, question, choices)
        self.nb_choices = nb_choices
        self.unique = unique

    def poser_question(self):
        # str.split (délimiteur): découper une chaine de caractères en liste
        # de sous chaines séparées par un délimiteur
        choices = []
        if isinstance(self.nb_choices, IntField):
            nb_choices = self.nb_choices.poser_question()
        else:
            nb_choices = self.nb_choices
        if not self.choices:
            raise Exception("Impossible de choisir 1 choix parmi aucune possibilité")
        while len(choices) < nb_choices:
            print(f"Choix n°{len(choices) + 1}/{nb_choices}")

            choice = super().poser_question()
            if self.unique and choice in choices:
                print(f"impossible de faire ce choix: {choice} car déjà choisi !")

            else:
                choices.append(choice)

        return choices


class AskJoueursField(MultipleChoiceField):
    def __init__(self, nom, joueurs, nb_choices, unique=True):
        super().__init__(nom, "Joueurs", joueurs, nb_choices, unique=unique)

    def poser_question(self):
        try:
            return super().poser_question()
        except Exception as e:
            raise Exception(
                "Veuillez créer une liste des joueurs avant de créer un tournoi"
            ) from e
