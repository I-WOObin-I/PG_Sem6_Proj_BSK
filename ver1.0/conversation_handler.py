''' class for handling conversation '''
'''
- retrieving conversation from chat files using ChatFilesHandler
- saving conversation to chat files using ChatFilesHandler
- encrypting and decrypting conversation using fernet and key from chat file
- returning conversation to gui dictionary format
'''

from chat_files_handler import ChatFilesHandler
from cryptography.fernet import Fernet
from socket_manager import SocketManager
import threading

class ConversationHandler():
    def __init__(self, address, port, conversation_frame, chats_frame):
        self.address = address
        self.port = int(port)
        self.conversation_frame = conversation_frame
        self.chats_frame = chats_frame
        conversation_frame.set_conversation_handler(self)

        self.socket_manager = SocketManager(self, self.address, self.port, self.received)


    def new_conversation(self):
        self.socket_manager.listen()
    def connect(self):
        self.socket_manager.connect()

    def send_text(self, text):
        self.socket_manager.send_text(text)
        self.conversation_frame.add_message('t', text, local_sender=True)

    def send_file(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                file_data = file.read()
                message = self.conversation_frame.add_message('f', file_data, local_sender=True)
                self.socket_manager.send_file(file_data, message)
        except:
            self.log("Error sending file")


    def received(self, message_type, data):
        message = self.conversation_frame.add_message(message_type, data, local_sender=False)
        return message

    def log(self, text):
        self.chats_frame.log(text)

    '''
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
    
    
    
    '''