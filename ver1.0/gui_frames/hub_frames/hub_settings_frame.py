import customtkinter as ctk
import config as cfg
from cryptography.hazmat.primitives import serialization
from gui_frames.gui_key_generator_frame import KeyGeneratorFrame



class SettingsHubFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.configure(fg_color=cfg.HUB_LEFT_COLUMN_COLOR)

        # Create username label
        #username = self.parent.user_data_manager.get_username()
        username = "testUser"
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
        file_path = ctk.filedialog.askopenfilename(title="Select Public Key File")
        with open(file_path, "rb") as key_file:
            public_key = serialization.load_pem_public_key(key_file.read())
        self.public_key_fingerprint_label.config(text="Public Key: " + str(public_key))

    def upload_priv_key_button_action(self):
        file_path = ctk.filedialog.askopenfilename(title="Select Private Key File")
        with open(file_path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None
            )
        self.private_key_loaded_label.config(text="Private Key Loaded")

    def logout_button_action(self):
        self.parent.parent.go_back()
