from flask_login import UserMixin


# Simulate user database
USERS_DB = {}


class User(UserMixin):

    """Custom User class."""

    def __init__(self, id_, username, identity_card_info, email=None):
        self.id = id_
        self.username = username
        self.identity_card_info = identity_card_info
        self.email = email

    def claims(self):
        """Use this method to render all assigned claims on profile page."""
        return {'id': self.id,
                'username': self.username,
                'email': self.email,
                'card type': self.identity_card_info['type'] if self.identity_card_info else None,
                'card status': self.identity_card_info['status'] if self.identity_card_info else None,
                'card fields': self.identity_card_info['fields'] if self.identity_card_info else None}.items()

    @staticmethod
    def get(user_id):
        return USERS_DB.get(user_id)

    @staticmethod
    def create(user_id, username, identity_card_info, email=None):
        USERS_DB[user_id] = User(user_id, username, identity_card_info, email)
