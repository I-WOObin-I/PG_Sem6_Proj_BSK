import json
from base64 import b64encode, b64decode
import struct

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

KEY_SIZE_BYTE = 32

class sessionKeyHandler():
    def __init__(self):
        self.session_key = None

    def generate_session_key(self):
        self.session_key = get_random_bytes(KEY_SIZE_BYTE)
        return self.session_key



    def encrypt_ECB(self, data):
        cipher_ECB = AES.new(self.session_key, AES.MODE_ECB)
        ct_bytes = cipher_ECB.encrypt(pad(data.encode(), AES.block_size))
        ct = b64encode(ct_bytes).decode('utf-8')
        return ct

    def decrypt_ECB(self, data):
        ct = b64decode(data)
        cipher_ECB = AES.new(self.session_key, AES.MODE_ECB)
        pt = unpad(cipher_ECB.decrypt(ct), AES.block_size)
        return pt

    def encrypt_text_CBC(self, data):
        cipher_CBC = AES.new(self.session_key, AES.MODE_CBC)
        ct_bytes = cipher_CBC.encrypt(pad(data.encode('utf-8'), AES.block_size))
        iv = b64encode(cipher_CBC.iv).decode('utf-8')
        ct = b64encode(ct_bytes).decode('utf-8')
        result = json.dumps({'iv': iv, 'ciphertext': ct})
        return result

    def decrypt_text_CBC(self, json_input):
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




    def encrypt_file(self, encryption_type, file_name, data):
        if encryption_type == 'x':
            return self.encrypt_file_EAX(file_name, data)
        else:
            print("Error unexpected encryption type: " + encryption_type)
            return None
    def decrypt_file(self, data):
        encryption_type = struct.unpack('B', data[:1])[0]
        if encryption_type == ord('x'):
            file_name, file = self.decrypt_file_EAX(data[1:])
        else:
            print("Error unexpected encryption type: " + encryption_type)
            return None
        return file_name, file


    def encrypt_file_EAX(self, file_name, file):
        cipher_EAX = AES.new(self.session_key, AES.MODE_EAX)

        encryption_type = struct.pack('B', ord('x'))
        file_name_len = struct.pack('I', len(file_name))
        print("File name len: " + str(file_name_len))
        print("File name: " + file_name)

        data = file_name_len + file_name.encode() + file
        data = cipher_EAX.encrypt(data)

        packed = encryption_type + data

        # <encryption type>[[<file name len><file name><file>]]

        return packed

    def decrypt_file_EAX(self, data):
        cipher_EAX = AES.new(self.session_key, AES.MODE_EAX)
        data = cipher_EAX.decrypt(data)

        file_name_len = struct.unpack('I', data[:4])[0]
        print("File name len: " + str(file_name_len))

        file_name = data[4:4+file_name_len].decode()
        print("File name: " + file_name)

        file = data[4+file_name_len:]

        return file_name, file













