from cryptography.hazmat.primitives import hashes, padding, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.fernet import Fernet

PUBLIC_EXPONENT = 65537
KEY_LENGTHS = [2048, 4096, 8192]

class asymKeyHandler():
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.guest_public_key = None
        self.user_password = None

    def generate_keys(self, key_length):
        self.private_key = rsa.generate_private_key(
            public_exponent=PUBLIC_EXPONENT,
            key_size=key_length
        )
        self.public_key = self.private_key.public_key()
        return self.get_public_key_fingerprint()

    def encrypt_session_key(self, session_key, public_key):
        return public_key.encrypt(
            session_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    def decrypt_session_key(self, encrypted_session_key):
        return self.private_key.decrypt(
            encrypted_session_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )



    # public key methods
    def encrypt_and_save_public_key(self, file_path):
        self.encrypt_and_save_key(file_path, self.public_key)

    def decrypt_and_load_public_key(self, file_path):
        self.public_key = self.decrypt_and_load_key(file_path)

    def get_public_key(self):
        return self.public_key

    def get_public_key_fingerprint(self):
        return self.get_key_fingerprints(self.public_key)





    # guest public key methods
    def encrypt_and_save_guest_public_key(self, file_path):
        self.encrypt_and_save_key(file_path, self.guest_public_key)

    def decrypt_and_load_guest_public_key(self, file_path):
        self.guest_public_key = self.decrypt_and_load_key(file_path)

    def get_guest_public_key_fingerprint(self):
        return self.get_key_fingerprints(self.guest_public_key)

    def encrypt_and_save_key(self, file_path, key):
        with open(file_path, "wb") as file:
            public_key_pem = key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            file.write(Fernet(self.user_password).encrypt(public_key_pem))




    # key methods
    def decrypt_and_load_key(self, file_path):
        with open(file_path, "rb") as file:
            key_encrypted = file.read()
        key_decrypted = serialization.load_pem_public_key(
            Fernet(self.user_password).decrypt(key_encrypted),
            backend=None
        )
        return key_decrypted

    def get_key_fingerprints(self, key):
        serialized_public_key = key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        hash_algorithm = hashes.SHA256()
        hasher = hashes.Hash(hash_algorithm)
        hasher.update(serialized_public_key)
        public_key_hash = hasher.finalize()

        fingerprint = public_key_hash.hex()
        return fingerprint




    # private key methods
    def encrypt_and_save_private_key(self, file_path):
        with open(file_path, "wb") as file:
            private_key_pem = self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            file.write(Fernet(self.user_password).encrypt(private_key_pem))

    def decrypt_and_load_private_key(self, file_path):
        with open(file_path, "rb") as file:
            key = file.read()
        self.private_key = serialization.load_pem_private_key(
            Fernet(self.user_password).decrypt(key),
            password=None,
            backend=None
        )



    def get_key_lengths(self):
        return KEY_LENGTHS


