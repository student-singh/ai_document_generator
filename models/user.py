from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id, email):
        self.id = str(id)
        self.email = email
