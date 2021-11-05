from typing import Callable
from exception import UserException
from views.errors import afficher_erreur


class Action:
    def __init__(
        self, intitule, callback: Callable, args: list = [], kwargs: dict = {}
    ):
        self.intitule = intitule
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return self.intitule

    def executer(self, args=tuple(), kwargs={}, **kw):
        try:
            return self.callback(*self.args, *args, **self.kwargs, **kwargs, **kw)
        except UserException as e:
            e.afficher_erreur()
        except Exception as e:  # faudra vraiment utiliser une exception custom
            afficher_erreur(e, msg="Erreur inattendue (bug): ")
            raise
