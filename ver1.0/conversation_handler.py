''' class for handling conversation '''
'''
- retrieving conversation from chat files using ChatFilesHandler
- saving conversation to chat files using ChatFilesHandler
- encrypting and decrypting conversation using fernet and key from chat file
- returning conversation to gui dictionary format
'''

from chat_files_handler import ChatFilesHandler
from cryptography.fernet import Fernet

class ConversationHandler():
    def __init__(self, chat_name, username, password):
        self.chat_name = chat_name
        self.username = username
        self.password = password

        self.chat_files_handler = ChatFilesHandler()

        # get chat data from chat file
        self.chat_data = self.chat_files_handler.get_chat(self.chat_name, self.username, self.password)
        self.chat_key = self.chat_data["chat_key"]

        self.encrypted_conversation = self.chat_data["chat_conversation"]
        self.encrypted_conversation_new = []
        self.decrypted_conversation = self._decrypt_conversation()




    def _decrypt_conversation(self):
        # decrypt all messages in conversation using ferent and chat key
        decrypted_conversation = []
        fernet = Fernet(self.chat_key)
        for message in self.encrypted_conversation:

            encrypted_message = message["message"]
            decrypted_message = fernet.decrypt(encrypted_message).decode()

            decrypted_conversation.append({
                "username": message["username"],
                "time_stamp": message["time_stamp"],
                "message": decrypted_message
            })

        return decrypted_conversation

    def _append_message_to_conversation(self, message):

        # add encrypted message to encrypted conversation
        self.encrypted_conversation.append(message)

        # add decrypted message to encrypted conversation (new massages)
        self.encrypted_conversation_new.append(message)

        # add decrypted message to decrypted conversation
        ferent = Fernet(self.chat_key)
        decrypted_message = ferent.decrypt(message["message"]).decode()
        self.decrypted_conversation.append({
            "username": message["username"],
            "time_stamp": message["time_stamp"],
            "message": decrypted_message
        })

    def _save_conversation(self):
        self.chat_files_handler.save_chat(self.chat_name, self.username, self.password, self.encrypted_conversation_new)