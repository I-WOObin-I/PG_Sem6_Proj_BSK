'''this is the main menu frame for the gui contains:
- menu list on the left with (seperate frame class in this file):
    - a label showing the username
    - a label showing length of the keys
    - a label showing the public key fingerprint
    - a button tu load a public key
    - a label showing if the private key is loaded
    - a button to load a private key
    - a button to generate a key pair
    - a button to logout
- list of conversations on the right (seperate frame class in this file):
    - a button to start a new conversation
    - list of conversations
- current conversation in the middle (seperate frame class in this file):
    - a title label on top
    - a frame to display the conversation under the title label (seperate frame in this file):
'''
from tkinter import filedialog

from cryptography.hazmat.primitives import serialization

from gui_frames.gui_frame import GuiFrame
import customtkinter as ctk
from user_data_manager import UserDataManager
from gui_frames.gui_key_generator_frame import KeyGeneratorFrame

LEFT_COLUMN_WIDTH = 100
LEFT_COLUMN_COLOR = "#212121"
MIDDLE_COLUMN_COLOR = "#1a1a1a"
RIGHT_COLUMN_WIDTH = 200
RIGHT_COLUMN_COLOR = "#212121"

FRAMES_PADX = 3
FRAMES_PADY = 3

class MainMenuFrame(GuiFrame):
    def __init__(self, parent, callback, user_data_manager: UserDataManager):
        super().__init__(parent, callback)

        self.parent = parent
        self.user_data_manager = user_data_manager
        self.pack(fill="both", expand=True)


        self.columnconfigure(0, minsize=LEFT_COLUMN_WIDTH)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, minsize=RIGHT_COLUMN_WIDTH)
        self.rowconfigure(0, weight=1)

        self.menu_frame = LeftMenuFrame(self)
        self.menu_frame.grid(row=0, column=0, sticky="nsew", padx=FRAMES_PADX, pady=FRAMES_PADY)

        self.conversation_frame = CurrentConversationFrame(self)
        self.conversation_frame.grid(row=0, column=1, sticky="nsew", padx=FRAMES_PADX, pady=FRAMES_PADY)

        self.conversation_list_frame = ConversationListFrame(self)
        self.conversation_list_frame.grid(row=0, column=2, sticky="nsew", padx=FRAMES_PADX, pady=FRAMES_PADY)

    def show_frame(self, frame_class):
        self.parent.show_frame(frame_class)

#class for Left manu frame
class LeftMenuFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.configure(fg_color=LEFT_COLUMN_COLOR)

        # Create username label
        username = self.parent.user_data_manager.get_username()
        self.username_label = ctk.CTkLabel(self, text=username)
        self.username_label.pack(fill="x")

        # Create key length label
        self.key_length_label = ctk.CTkLabel(self, text="Key length: <key length>")
        self.key_length_label.pack(fill="x")

        # Create public key fingerprint label
        self.public_key_fingerprint_label = ctk.CTkLabel(self, text="Public key fingerprint")
        self.public_key_fingerprint_label.pack(fill="x")

        # Create label to show public key fingerprint
        self.public_key_fingerprint = ctk.CTkLabel(self, text="<Public key fingerprint>")
        self.public_key_fingerprint.pack(fill="x")

        # Create button to load public key
        self.load_public_key_button = ctk.CTkButton(self, text="Load public key", command=self.upload_public_key)
        self.load_public_key_button.pack(fill="x")

        # Create label to show if private key is loaded
        self.private_key_loaded_label = ctk.CTkLabel(self, text="Private key loaded")
        self.private_key_loaded_label.pack(fill="x")

        # Create button to load private key
        self.load_private_key_button = ctk.CTkButton(self, text="Load private key", command=self.upload_private_key)
        self.load_private_key_button.pack(fill="x")

        # Create button to generate key pair
        self.generate_key_pair_button = ctk.CTkButton(self, text="Generate key pair", command=self.frame_go_to_keyGeneratorFrame())
        self.generate_key_pair_button.pack(fill="x")

        # Create button to log out
        # it calls callback function from parent
        self.logout_button = ctk.CTkButton(self, text="Log out", command=self.parent.parent.go_back)
        self.logout_button.pack(fill="x")

    # method to uploade public key
    def upload_public_key(self):
        file_path = filedialog.askopenfilename(title="Select Public Key File")
        with open(file_path, "rb") as key_file:
            public_key = serialization.load_pem_public_key(key_file.read())
        self.public_key_fingerprint_label.config(text="Public Key: " + str(public_key))

    # method to upload private key
    def upload_private_key(self):
        file_path = filedialog.askopenfilename(title="Select Private Key File")
        with open(file_path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None
            )
        self.private_key_loaded_label.config(text="Private Key Loaded")

    def frame_go_to_keyGeneratorFrame(self):
        self.parent.show_frame(KeyGeneratorFrame)

# class for current conversation frame
class CurrentConversationFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.configure(fg_color=MIDDLE_COLUMN_COLOR)

        # Create conversation label for title
        # it spreads over the whole width of the frame
        # has black background and white text
        self.conversation_title_frame = ctk.CTkFrame(self)
        self.conversation_label = ctk.CTkLabel(self.conversation_title_frame, text="Conversation Title")
        self.conversation_label.pack(fill="x")
        self.conversation_title_frame.pack(fill="x")

        # Create conversation frame
        self.conversation_frame = ctk.CTkFrame(self, fg_color=MIDDLE_COLUMN_COLOR)
        self.conversation_frame.pack(fill="both", expand=True)

# class for conversation list frame
class ConversationListFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.configure(fg_color=RIGHT_COLUMN_COLOR)

        # Create buttons
        self.new_conversation_button = ctk.CTkButton(self, text="New Conversation")

        # Pack buttons
        self.new_conversation_button.pack(fill="x")

if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Tk")
    root.geometry("800x400")
    login_frame = MainMenuFrame(root, lambda: ())
    login_frame.pack(expand=True, fill="both")
    root.mainloop()
