''' file with classes for retrieving data from files such as conversations, chats, config'''
''' file format for all conversations is as follows (json, each chat encrypted with symetric key, one file per chat):
    "chat":
        {
            "chat_name": "name",
            "chat_key": "key",
            "chat_conversation": [
                {
                    "username": "username",
                    "time_stamp": "time_stamp",
                    "message": "message"
                }
            ]
        }
    
    file format for symetric keys is as follows (json, encrypted with user's password):
    "chat_keys": [
        {
            "chat_name": "name",
            "chat_file_name": "file_name",
            "chat_key": "key"
        }
    ]
    
    file format for users is as follows (json):
    "users": [
        {
            "username": "username",
            "password_hash": "password_hash",
            "keys_file_name": "file_name",
        }
    ]
    
'''


import json
import os
from cryptography.fernet import Fernet
import hashlib

class ChatFilesHandler():
    def __init__(self):

        self.users_file_path = "users.json"


    def retrieve_all_chat_names(self, username, password):

        user_keys_data = self._get_user_keys_data(username, password)
        chat_names = []
        for chat in user_keys_data["chat_keys"]:
            chat_names.append(chat["chat_name"])

        return chat_names


    def add_new_chat(self, chat_name, chat_key, new_chat_file_name, username, password):

        # create and save new encrypted chat file
        chat_data = {
            "chat": {
                "chat_name": chat_name,
                "chat_key": chat_key,
                "chat_conversation": []
            }
        }
        new_file_key = Fernet.generate_key()
        self._encrypt_and_save_chat(new_chat_file_name, new_file_key, chat_data)

        # save new chat file name and key to proper User_Keys file

        user_keys = self._get_user_keys_data(username, password)

        # add new chat key to User_Keys file
        user_keys["chat_keys"].append({
            "chat_name": chat_name,
            "chat_file_name": new_chat_file_name,
            "chat_key": new_file_key
        })

        self._encrypt_and_save_user_keys(username, password, user_keys)


    def save_chat(self, chat_name, chat_key, file_name, username, password, chat_conversation):

        user_keys = self._get_user_keys_data(username, password)
        chat_file_name = user_keys["chat_keys"][user_keys["chat_keys"].index({"chat_name": chat_name})]["chat_file_name"]
        chat = self._get_chat_data(chat_file_name, chat_key)
        chat["chat"]["chat_conversation"].append(chat_conversation)

        self._encrypt_and_save_chat(chat_file_name, chat_key, chat)


    def get_chat(self, chat_name, chat_key, username, password):

        user_keys = self._get_user_keys_data(username, password)
        chat_file_name = user_keys["chat_keys"][user_keys["chat_keys"].index({"chat_name": chat_name})]["chat_file_name"]
        chat = self._get_chat_data(chat_file_name, chat_key)

        return chat



    ''' util functions '''

    def _get_user_keys_data(self, username, password):

        # load Users json file to get proper User_Keys file name
        with open(self.users_file_path, "r") as file:
            users_data = json.load(file)

        # find User_Keys file name
        user_keys_file_name = users_data["users"][users_data["users"].index({"username": username})]["keys_file_name"]

        # decrypt User_Keys file
        with open(user_keys_file_name, "rb") as file:
            user_keys_file = file.read()
        fernet = Fernet(password)
        user_keys = json.loads(fernet.decrypt(user_keys_file).decode())

        return user_keys

    def _get_chat_data(self, chat_file_name, chat_file_key):

        with open(chat_file_name, "rb") as file:
            chat_file = file.read()
        fernet = Fernet(chat_file_key)
        chat_data = json.loads(fernet.decrypt(chat_file).decode())

        return chat_data

    def _encrypt_and_save_chat(self, chat_file_name, chat_file_key, chat_data):

        fernet = Fernet(chat_file_key)
        json_data = json.dumps(chat_data)
        encrypted_chat_file = fernet.encrypt(json_data.encode())
        with open(chat_file_name, "wb") as file:
            file.write(encrypted_chat_file)

    def _encrypt_and_save_user_keys(self, user_keys_data, username, password):

        # load Users json file to get proper User_Keys file name
        with open(self.users_file_path, "r") as file:
            users_data = json.load(file)

        # find User_Keys file name
        user_keys_file_name = users_data["users"][users_data["users"].index({"username": username})]["keys_file_name"]

        fernet = Fernet(password)
        json_data = json.dumps(user_keys_data)
        encrypted_file = fernet.encrypt(json_data.encode())
        with open(user_keys_file_name, "wb") as file:
            file.write(encrypted_file)