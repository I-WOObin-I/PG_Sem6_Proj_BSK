''' this is class for managing files with users data and long term conversation saving'''
import json
import os


class UserLoginHandler():
    def __init__(self):
        self.file_path = "users.json"

        # if file does not exist create it
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as file:
                file.write("{}")
                self.file_data = [{}]
        else:
            with open(self.file_path, "r") as file:
                self.file_data = json.load(file)

    def save_users(self):
        with open(self.file_path, "w") as file:
            json.dump(self.file_data, file)

    # add new user to file
    def add_user(self, username, password_hash):
        self.file_data.append({
            "username": username,
            "password_hash": password_hash
        })
        self.save_users()

    def validate_user(self, username, password_hash):
        if {"username": username, "password_hash": password_hash} in self.file_data:
            return True
        return False

