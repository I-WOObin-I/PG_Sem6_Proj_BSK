import json
from base64 import b64encode, b64decode

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

KEY_SIZE = 256

class sessionKeyHandler():
    def __init__(self):
        self.session_key = None

    def generate_session_key(self):
        self.session_key = get_random_bytes(KEY_SIZE)
        return self.session_key



    def encrypt_ECB(self, data):
        cipher_ECB = AES.new(self.session_key, AES.MODE_ECB)
        ct_bytes = cipher_ECB.encrypt(pad(data, AES.block_size))
        ct = b64encode(ct_bytes).decode('utf-8')
        return ct

    def decrypt_ECB(self, data):
        ct = b64decode(data)
        cipher_ECB = AES.new(self.session_key, AES.MODE_ECB)
        pt = unpad(cipher_ECB.decrypt(ct), AES.block_size)
        return pt

    def encrypt_CBC(self, data):
        cipher_CBC = AES.new(self.session_key, AES.MODE_CBC)
        ct_bytes = cipher_CBC.encrypt(pad(data, AES.block_size))
        iv = b64encode(cipher_CBC.iv).decode('utf-8')
        ct = b64encode(ct_bytes).decode('utf-8')
        result = json.dumps({'iv': iv, 'ciphertext': ct})
        return result

    def decrypt_CBC(self, json_input):
        try:
            b64 = json.loads(json_input)
            iv = b64decode(b64['iv'])
            ct = b64decode(b64['ciphertext'])
            cipher_CBC = AES.new(self.session_key, AES.MODE_CBC, iv)
            pt = unpad(cipher_CBC.decrypt(ct), AES.block_size)
            return pt
        except:
            print("Error decrypting")
            return None
