from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

PUBLIC_EXPONENT = 65537
KEY_LENGTHS = ['2048', '4096', '8192']

class asymKeyHandler():
    def __init__(self, user_manager):
        self.private_key = None
        self.public_key = None
        self.guest_key = None

        self.user_manager = user_manager


    def generate_keys(self, key_length):
        print("Generating keys: " + str(key_length))
        self.private_key = RSA.generate(key_length, e=PUBLIC_EXPONENT)
        self.public_key = self.private_key.publickey()



    def encrypt_session_key(self, session_key):
        cipher_rsa = PKCS1_OAEP.new(self.guest_key)
        encrypted_session_key = cipher_rsa.encrypt(session_key)
        return encrypted_session_key

    def decrypt_session_key(self, encrypted_session_key):
        cipher_rsa = PKCS1_OAEP.new(self.private_key)
        decrypted_session_key = cipher_rsa.decrypt(encrypted_session_key)
        return decrypted_session_key




    # SAVING KEYS
    def save_public_key(self, file_path):
        self.save_key(file_path, self.public_key)
    def save_private_key(self, file_path):
        self.save_key(file_path, self.private_key)
    def save_guest_key(self, file_path):
        self.save_key(file_path, self.guest_key)

    def save_key(self, file_path, key):
        encrypted_key = key.exportKey("PEM", passphrase=self.user_manager.user_password)
        try:
            with open(file_path, "wb") as file:
                file.write(encrypted_key)
        except:
            print("Error saving key")


    # LOADING KEYS
    def load_public_key(self, file_path):
        try:
            self.public_key = self.load_key(file_path)
            return 0
        except:
            print("Error loading public key")
            return 1
    def load_private_key(self, file_path):
        try:
            self.private_key = self.load_key(file_path)
            return 0
        except:
            print("Error loading private key")
            return 1
    def load_guest_key(self, guest_public_key):
        try:
            self.guest_key = RSA.import_key(guest_public_key)
        except:
            print("Error loading guest key")


    def load_key(self, file_path):
        with open(file_path, "rb") as file:
            key = RSA.importKey(file.read(), passphrase=self.user_manager.user_password)
            return key








    def get_public_key_fingerprint(self):
        return SHA256.new(self.public_key.exportKey("PEM").decode()).hexdigest()
    def get_guest_key_fingerprint(self):
        return SHA256.new(self.guest_key.exportKey("PEM").decode()).hexdigest()

    def set_user_password(self, password):
        self.user_password = password
        self.user_password_hash = SHA256.new(password.encode())

    def get_key_length(self):
        return int(self.public_key.size_in_bits())

    def get_key_length_options(self):
        return KEY_LENGTHS


