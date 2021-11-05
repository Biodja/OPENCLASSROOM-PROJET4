from action import Action
from views.errors import afficher_erreur_champ
from models import save_to_db


class Formulaire(Action):
    def __init__(self, titre, champs, callback):
        self.intitule = titre
        self.callback = self.executer
        self.post_formulaire = callback
        self.champs = champs

    def executer(self, args=tuple(), kwargs={}, **kw):
        data = {**kwargs, **kw}
        try:
            for champ in self.champs:
                data[champ.nom] = champ.poser_question()
        except KeyboardInterrupt:
            return
        except Exception as e:
            afficher_erreur_champ(e, champ)
        else:
            self.post_formulaire(**data)
            save_to_db()
