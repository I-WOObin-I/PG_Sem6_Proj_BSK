import config as cfg
import customtkinter as ctk
from gui_frames.gui_key_generator_frame import KeyGeneratorFrame


class UtilityHubFrame(ctk.CTkFrame):
    def __init__(self, parent, user_manager):
        super().__init__(parent)

        self.parent = parent
        self.user_manager = user_manager
        self.asymm_key_handler = user_manager.asym_key_handler
        self.session_key_handler = user_manager.session_key_handler

        self.configure(fg_color=cfg.HUB_LEFT_COLUMN_COLOR)

        # Create username label
        self.username_label = ctk.CTkLabel(self, text=self.user_manager.username)
        self.username_label.pack(fill="x")

        # Create key length label
        self.key_length_label = ctk.CTkLabel(self, text="")
        self.key_length_label.pack(fill="x")

        # Create public key fingerprint label
        self.public_key_loaded_label = ctk.CTkLabel(self, text="")
        self.public_key_loaded_label.pack(fill="x")


        # Create button to load public key
        self.load_public_key_button = ctk.CTkButton(self, text="Load public key", command=self.upload_pub_key_button_action)
        self.load_public_key_button.pack(fill="x")

        # Create label to show if private key is loaded
        self.private_key_loaded_label = ctk.CTkLabel(self, text="")
        self.private_key_loaded_label.pack(fill="x")

        # Create button to load private key
        self.load_private_key_button = ctk.CTkButton(self, text="Load private key", command=self.upload_priv_key_button_action)
        self.load_private_key_button.pack(fill="x")

        # Create button to generate key pair
        self.generate_key_pair_button = ctk.CTkButton(self, text="Generate key pair", command=self.generate_key_pair_button_action)
        self.generate_key_pair_button.pack(fill="x")

        # Create button to log out
        # it calls callback function from parent
        self.logout_button = ctk.CTkButton(self, text="Logout", command=self.logout_button_action)
        self.logout_button.pack(fill="x")


    # methods for buttons

    def upload_pub_key_button_action(self):
        file_path = ctk.filedialog.askopenfilename(title="Select Public Key File", initialfile=cfg.DEFAULT_PUBLIC_KEY_FILE_NAME, filetypes=cfg.KEY_FILE_TYPES)
        if file_path == "":
            return
        self.asymm_key_handler.load_public_key(file_path)
        self.public_key_loaded_label.configure(text="Public Key Loaded")
        self.key_length_label.configure(text="Key length: " + str(self.asymm_key_handler.get_key_length()))

    def upload_priv_key_button_action(self):
        file_path = ctk.filedialog.askopenfilename(title="Select Private Key File", initialfile=cfg.DEFAULT_PRIVATE_KEY_FILE_NAME, filetypes=cfg.KEY_FILE_TYPES)
        if file_path == "":
            return
        self.asymm_key_handler.load_private_key(file_path)
        self.private_key_loaded_label.configure(text="Private Key Loaded")

    def generate_key_pair_button_action(self):
        self.parent.parent.show_frame(KeyGeneratorFrame)

    def logout_button_action(self):
        self.parent.go_back()
