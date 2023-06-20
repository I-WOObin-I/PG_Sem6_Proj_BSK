from encryption.asym_key_handler import asymKeyHandler
from encryption.session_key_handler import sessionKeyHandler


class UserManager():
    def __init__(self):
        self.username = None
        self.user_password = None

        self.asym_key_handler = asymKeyHandler(self)
        self.session_key_handler = sessionKeyHandler()
