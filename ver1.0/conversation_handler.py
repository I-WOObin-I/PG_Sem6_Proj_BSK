''' class for handling conversation '''
'''
- retrieving conversation from chat files using ChatFilesHandler
- saving conversation to chat files using ChatFilesHandler
- encrypting and decrypting conversation using fernet and key from chat file
- returning conversation to gui dictionary format
'''

from socket_manager import SocketManager


class ConversationHandler():
    def __init__(self, address, port, conversation_frame, chats_frame, user_manager):
        self.address = address
        self.port = int(port)
        self.conversation_frame = conversation_frame
        self.chats_frame = chats_frame
        conversation_frame.set_conversation_handler(self)

        self.user_manager = user_manager
        self.asymmetric_key_handler = user_manager.asym_key_handler
        self.session_key_handler = user_manager.session_key_handler

        self.socket_manager = SocketManager(self, self.address, self.port, self.received)


    def new_conversation(self):
        self.socket_manager.listen()
    def connect(self):
        self.socket_manager.connect()
        self.send_public_key()

    def send_public_key(self):
        self.socket_manager.send_public_key(self.asymmetric_key_handler.public_key.exportKey('PEM'))

    def received_guest_key(self, guest_key):
        self.asymmetric_key_handler.load_guest_key(guest_key)
        self.session_key_handler.generate_session_key()
        #self.log("Session key: " + str(self.session_key_handler.session_key))
        self.send_session_key()

    def send_session_key(self):
        encrypted_session_key = self.asymmetric_key_handler.encrypt_session_key(self.session_key_handler.session_key)
        self.socket_manager.send_session_key(encrypted_session_key)

    def received_session_key(self, encrypted_session_key):
        decrypted_session_key = self.asymmetric_key_handler.decrypt_session_key(encrypted_session_key)
        self.session_key_handler.session_key = decrypted_session_key
        #self.log("Session key: " + str(self.session_key_handler.session_key))





    def send_text(self, text):
        encrypted = self.session_key_handler.encrypt_text_CBC(text)
        self.socket_manager.send_text(encrypted)
        self.conversation_frame.add_message('t', text, local_sender=True)

    def send_file(self, file_path):
        with open(file_path, 'rb') as file:
            file_data = file.read()
            message = self.conversation_frame.add_message('f', file_data, local_sender=True)
            data = self.session_key_handler.encrypt_file_EAX(file_data)
            self.socket_manager.send_file(data, message)
        self.log("Error sending file")


    def received(self, message_type, data):
        if message_type == 'g':
            self.received_guest_key(data)
        elif message_type == 'k':
            self.received_session_key(data)
        elif message_type == 't':
            data = self.session_key_handler.decrypt_text_CBC(data)
            message = self.conversation_frame.add_message(message_type, data, local_sender=False)
            return message
        elif message_type == 'f':
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