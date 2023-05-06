'''this is class for user data manager which manages all the data of the user
- username
- password
- public key
- private key
- key length
'''

class UserDataManager():
    def __init__(self):
        self.username = ""
        self.password = ""
        self.public_key = ""
        self.private_key = ""
        self.key_length = 0

    def set_username(self, username):
        self.username = username

    def set_password(self, password):
        self.password = password

    def set_public_key(self, public_key):
        self.public_key = public_key

    def set_private_key(self, private_key):
        self.private_key = private_key

    def set_key_length(self, key_length):
        self.key_length = key_length

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_public_key(self):
        return self.public_key

    def get_private_key(self):
        return self.private_key

    def get_key_length(self):
        return self.key_length

    def get_user_data(self):
        return {
            "username": self.username,
            "password": self.password,
            "public_key": self.public_key,
            "private_key": self.private_key,
            "key_length": self.key_length
        }

    def set_user_data(self, user_data):
        self.username = user_data["username"]
        self.password = user_data["password"]
        self.public_key = user_data["public_key"]
        self.private_key = user_data["private_key"]
        self.key_length = user_data["key_length"]