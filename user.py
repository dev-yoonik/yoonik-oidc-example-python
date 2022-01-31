from flask_login import UserMixin


# Simulate user database
USERS_DB = {}


class User(UserMixin):

    """Custom User class."""

    def __init__(self, id_, name):
        self.id = id_
        self.name = name

    def claims(self):
        """Use this method to render all assigned claims on profile page."""
        return {'name': self.name}.items()

    @staticmethod
    def get(user_id):
        return USERS_DB.get(user_id)

    @staticmethod
    def create(user_id, name):
        USERS_DB[user_id] = User(user_id, name)
