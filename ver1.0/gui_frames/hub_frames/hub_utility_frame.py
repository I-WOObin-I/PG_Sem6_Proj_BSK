import customtkinter as ctk
import config as cfg
from cryptography.hazmat.primitives import serialization

from encryption.asym_key_handler import asymKeyHandler
from encryption.session_key_handler import sessionKeyHandler
from gui_frames.gui_key_generator_frame import KeyGeneratorFrame


class SettingsHubFrame(ctk.CTkFrame):
    def __init__(self, parent, asymm_key_handler, session_key_handler):
        super().__init__(parent)

        self.parent = parent
        self.asymm_key_handler = asymm_key_handler
        self.session_key_handler = session_key_handler

        self.configure(fg_color=cfg.HUB_LEFT_COLUMN_COLOR)

        # Create username label
        #username = self.parent.user_data_manager.get_username()
        username = "testUser"
        self.username_label = ctk.CTkLabel(self, text=username)
        self.username_label.pack(fill="x")

        # Create key length label
        self.key_length_label = ctk.CTkLabel(self, text="Key length: -")
        self.key_length_label.pack(fill="x")

        # Create public key fingerprint label
        self.public_key_fingerprint_label = ctk.CTkLabel(self, text="Public key fingerprint")
        self.public_key_fingerprint_label.pack(fill="x")

        # Create label to show public key fingerprint
        self.public_key_fingerprint = ctk.CTkLabel(self, text="<Public key fingerprint>", anchor='w', justify='left', wraplength=160)
        self.public_key_fingerprint.pack(fill="x")

        # Create button to load public key
        self.load_public_key_button = ctk.CTkButton(self, text="Load public key", command=self.upload_pub_key_button_action)
        self.load_public_key_button.pack(fill="x")

        # Create label to show if private key is loaded
        self.private_key_loaded_label = ctk.CTkLabel(self, text="Private key loaded")
        self.private_key_loaded_label.pack(fill="x")

        # Create button to load private key
        self.load_private_key_button = ctk.CTkButton(self, text="Load private key", command=self.upload_priv_key_button_action)
        self.load_private_key_button.pack(fill="x")

        # Create button to generate key pair
        self.generate_key_pair_button = ctk.CTkButton(self, text="Generate key pair",
                                                      command=self.frame_go_to_keyGeneratorFrame())
        self.generate_key_pair_button.pack(fill="x")

        # Create button to log out
        # it calls callback function from parent
        self.logout_button = ctk.CTkButton(self, text="Log out", command=self.logout_button_action)
        self.logout_button.pack(fill="x")


    def frame_go_to_keyGeneratorFrame(self):
        self.parent.show_frame(KeyGeneratorFrame)




    # methods for buttons

    def upload_pub_key_button_action(self):
        file_path = ctk.filedialog.askopenfilename(title="Select Public Key File", initialfile=cfg.DEFAULT_PUBLIC_KEY_FILE_NAME, filetypes=cfg.KEY_FILE_TYPES)
        self.asymm_key_handler.decrypt_and_load_public_key(file_path)
        self.public_key_fingerprint.configure(text=str(self.asymm_key_handler.get_public_key_fingerprint()))
        self.key_length_label.configure(text="Key length: " + str(self.asymm_key_handler.get_public_key_length()))

    def upload_priv_key_button_action(self):
        file_path = ctk.filedialog.askopenfilename(title="Select Private Key File", initialfile=cfg.DEFAULT_PRIVATE_KEY_FILE_NAME, filetypes=cfg.KEY_FILE_TYPES)
        self.asymm_key_handler.decrypt_and_load_private_key(file_path)
        self.private_key_loaded_label.configure(text="Private Key Loaded")

    def logout_button_action(self):
        self.parent.parent.go_back()
