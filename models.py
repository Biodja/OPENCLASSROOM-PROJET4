
import operator
import random
from exception import UserException, NotYetAvailable
import pickle

joueurs = []
tournois = []


def save_to_db():
    with open("joueurs.db", "wb") as file:
        pickle.dump(joueurs, file)
    with open("tournois.db", "wb") as file:
        pickle.dump(tournois, file)


def read_from_db():
    global joueurs
    global tournois
    with open("joueurs.db", "rb") as file:
        joueurs = pickle.load(file)
    with open("tournois.db", "rb") as file:
        tournois = pickle.load(file)


class Tournoi:
    nb_tournois = 0

    def __init__(
        self,
        nom,
        lieu,
        date,
        nombre_de_tours,
        controle_du_temps,
        description,
        tournees=[],
        joueurs=[],
    ):
        """ """
        Tournoi.nb_tournois += 1

        self.nom = nom
        self.lieu = lieu
        self.date = date
        self.nombre_de_tours = nombre_de_tours

        assert isinstance(tournees, list) and all(
            isinstance(t, Ronde) for t in tournees
        )

        self.joueurs = joueurs.copy()
        assert isinstance(joueurs, list) and all(isinstance(j, Joueur) for j in joueurs)

        if joueurs and (len(joueurs) % 2 != 0):
            raise ValueError("Le nombre de joueurs doit être pair.")

        self.controle_du_temps = controle_du_temps
        assert isinstance(controle_du_temps, (Blitz, CoupRapide, Bullet))

        self.description = description
        self.tours = []
        tournois.append(self)

    def ajouter_joueurs(self, joueurs: list):
        if (len(joueurs) + len(self.joueurs)) % 2 != 0:
            raise UserException(
                "Impossible d'avoir un tournoi avec un nombre de joueurs impair"
            )
        doublons = []
        for joueur in self.joueurs:
            if any(hash(joueur) == hash(j) for j in joueurs):
                doublons.append(joueur)
        if doublons:
            doublons = '\n'.join(f'- {joueur}' for joueur in doublons)
            raise UserException(
                "Impossible d'avoir des joueurs en doublon. Ces joueurs participent déjà au tournoi : \n" + doublons
            )
        for j in joueurs:
            self.joueurs.append(j)

    def lister_joueurs(self):
        for i, joueur in enumerate(self.joueurs):
            print(f"{i}) {joueur.nom}")
        
    def resultats(self):
        pass

    def __str__(self):

        return f"{self.nom}"

    @property
    def nb_joueurs(self):
        return len(self.joueurs)

    @property
    def tournoi_cloture(self):
        return len(self.tours) >= self.nombre_de_tours

    @property
    def tours_passes(self):
        return len(self.tours)

    @property
    def last_turn(self):
        if self.tours:
            return self.tours[-1]
        return None

    @property
    def scores(self):
        score = {}
        for tour in self.tours:
            for j, s in tour.scores.items():
                if j in score:
                    score[j] += s
                else:
                    score[j] = s
        return score

    def passer_au_tour_suivant(self):
        if self.tournoi_cloture:
            raise UserException("Le tournoi est déjà terminé")
        # Pseudo code

        if self.last_turn and all(
            not match.finished for match in self.last_turn.matchs
        ):
            raise UserException("Le dernier tour n'est même pas encore terminé")
        if not self.joueurs:
            raise UserException("Impossible de passer au tour suivant sans joueurs")
        matchs = []
        for paire in self.generer_paires():
            joueur_blanc, joueur_noir = random.sample(paire, 2)
            matchs.append(Match(joueur_blanc, joueur_noir))
        assert len(matchs) > 0

        self.tours.append(Tour(matchs))

    def generer_paires(self) -> list:
        if self.tours_passes == 0:
            joueurs_tournois = sorted(
                self.joueurs, key=operator.attrgetter("classement"), reverse=True
            )

            index_milieu_liste = len(joueurs_tournois) // 2
            classement_superieur = joueurs_tournois[0:index_milieu_liste]
            classement_inferieur = joueurs_tournois[index_milieu_liste:]

            matchs = []

            for joueur_blanc, joueur_noir in zip(
                classement_superieur, classement_inferieur
            ):
                match = [joueur_blanc, joueur_noir]
                matchs.append(match)
            return matchs
        else:  # cas des tours après le premier
            joueurs = sorted(self.joueurs, key=lambda j: self.scores[j], reverse=True)
            matchs = []
            while joueurs:  # équivalent à len(joueurs) > 0
                j1 = joueurs.pop(0)
                j2 = sorted(
                    joueurs,
                    key=lambda j: (self.nb_match_between(j1, j), -self.scores[j]),
                )[0]
                joueurs.remove(j2)
                matchs.append([j1, j2])
        return matchs

    def nb_match_between(self, j1, j2) -> int:
        """Cette fonction permet de savoir le nombre de fois qu'un joueurs "j1" joue contre un autre joueurs "j2" ."""

        return sum(1 for t in self.tours for m in t.matchs if j1 in m and j2 in m)


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


class ControleDuTemps:
    def __init__(self):
        pass


class Blitz(ControleDuTemps):
    def __str__(self):
        self.nom = "Blitz"
        return f"{self.nom}"


class Bullet(ControleDuTemps):
    def __init__(self):
        super().__init__()

    def __str__(self):
        self.nom = "Bullet"
        return f"{self.nom}"


class CoupRapide(ControleDuTemps):
    def __init__(self):
        super().__init__()

    def __str__(self):
        self.nom = "Coup Rapide"
        return f"{self.nom}"


class Ronde:
    def __init__(self):
        super().__init__()

    def __str__(self):
        self.nom = "Ronde"
        return f"{self.nom}"


class Joueur:
    joueurs_cree = 0

    def __init__(self, nom, prenom, date_de_naissance, sexe, classement):
        self.nom = nom
        self.prenom = prenom
        self.date_de_naissance = date_de_naissance
        self.sexe = sexe
        self.classement = classement
        joueurs.append(self)

    def __lt__(self, other):
        return self.classement < other.classement

    def __eq__(self, other):
        return self.classement == other.classement

    def __str__(self):
        return f"{self.nom} {self.prenom}"

    def __repr__(self):
        return f"{self.nom} {self.prenom} ({self.classement} pts)"

    def __hash__(self):
        return hash((self.nom, self.prenom, self.classement, self.sexe))


class Tour:
    def __init__(self, matchs) -> None:
        assert len(matchs) > 0
        self.matchs = matchs

    @property
    def scores(self):
        score = {}
        for match in self.matchs:
            score.update(match.scores)

        return score


class Match:
    def __init__(self, joueur_blanc, joueur_noir) -> None:
        assert isinstance(joueur_blanc, Joueur)
        assert isinstance(joueur_noir, Joueur)
        assert joueur_blanc is not joueur_noir

        self.joueur_blanc, self.joueur_noir = joueur_blanc, joueur_noir
        self.scores = {
            joueur_blanc: 0,
            joueur_noir: 0,
        }
        self.gagnant = None
        self.finished = False

    def __str__(self):
        return f"Blancs: {self.joueur_blanc} VS Noirs: {self.joueur_noir}"

    def finir_match(self, gagnant):
        if self.finished:
            # importer NotYetAvailable
            # raise NotYetAvailable("Le match est déjà terminé")
            raise NotYetAvailable("Le match est déjà terminé")
        self.gagnant = gagnant
        if self.gagnant:
            self.scores[gagnant] += 1.0
        else:
            self.scores[self.joueur_blanc] += 0.5
            self.scores[self.joueur_noir] += 0.5
        self.finished = True

    def __contains__(self, joueurs):
        return joueurs in (self.joueur_noir, self.joueur_blanc)


try:
    read_from_db()
except FileNotFoundError:
    save_to_db()
