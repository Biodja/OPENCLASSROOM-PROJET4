class UserException(Exception):
    def __init__(self, msg="Erreur") -> None:
        self.msg = msg
        super().__init__(msg)

    def afficher_erreur(self):
        print(self.msg)


class WrongFieldException(UserException):
    def __init__(self, field, raw_user_input):
        self.field = field
        self.raw_user_input = raw_user_input
        msg = f'{field.field_name}: Mauvaise valeur\nTapé: "{raw_user_input}" ; Attendu : {type(field)}'
        super().__init__(msg=msg)


class NotYetAvailable(UserException):
    def __init__(self, msg):
        super().__init__("Option indisponible: " + msg)
