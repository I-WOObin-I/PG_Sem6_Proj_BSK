from cryptography.fernet import Fernet

class sessionKeyHandler():
    def __init__(self):
        self.session_key = None

    def generate_session_key(self):
        self.session_key = Fernet.generate_key()
        return self.session_key

    def set_session_key(self, session_key):
        self.session_key = session_key


    def encrypt_message(self, message):
        return Fernet(self.session_key).encrypt(message)

    def decrypt_message(self, message):
        return Fernet(self.session_key).decrypt(message)