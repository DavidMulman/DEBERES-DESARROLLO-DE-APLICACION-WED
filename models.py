from flask_login import UserMixin


class Usuario(UserMixin):
    def __init__(self, id, usuario):
        self.id = str(id)
        self.usuario = usuario