#import tkinter as tk
import customtkinter as ctk
from customtkinter import filedialog
#from tkinter import filedialog
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from gui_frames.gui_frame import GuiFrame
from gui_frames.gui_key_generator_frame import KeyGeneratorFrame


class LoginFrame(GuiFrame):
    def __init__(self, parent, callback):
        #super().__init__(parent, callback)
        super().__init__(parent)

        self.parent = parent

        # Create a CTkLabel for the login prompt
        self.login_prompt = ctk.CTkLabel(self, text="Login:")
        self.login_prompt.pack()

        # Create an CTkEntry widget for the login
        self.login_CTkEntry = ctk.CTkEntry(self)
        self.login_CTkEntry.pack()

        # Create a CTkLabel for the password prompt
        self.password_prompt = ctk.CTkLabel(self, text="Password:")
        self.password_prompt.pack()

        # Create an CTkEntry widget for the password
        self.password_CTkEntry = ctk.CTkEntry(self, show="*")
        self.password_CTkEntry.pack()

        # Create a CTkButton to show the password
        self.show_CTkButton = ctk.CTkButton(self, text="Show Password", command=self.toggle_show_password)
        self.show_CTkButton.pack()

        # Create a CTkLabel for margin
        self.margin_CTkLabel = ctk.CTkLabel(self, text="")
        self.margin_CTkLabel.pack()

        # Create a CTkButton to load the public key
        self.public_key_CTkButton = ctk.CTkButton(self, text="Load Public Key", command=self.load_public_key)
        self.public_key_CTkButton.pack()

        # Create a CTkLabel to display the public key
        self.public_key_CTkLabel = ctk.CTkLabel(self, text="")
        self.public_key_CTkLabel.pack()

        # Create a CTkButton to load the private key
        self.private_key_CTkButton = ctk.CTkButton(self, text="Load Private Key", command=self.load_private_key)
        self.private_key_CTkButton.pack()

        # Create a CTkLabel to display the private key
        self.private_key_CTkLabel = ctk.CTkLabel(self, text="")
        self.private_key_CTkLabel.pack()

        # Create a CTkButton to load the private key
        self.gen_keys_CTkButton = ctk.CTkButton(self, text="Generate Keys", command=self.frame_go_to_keyGeneratorFrame)
        self.gen_keys_CTkButton.pack()

        # Create a CTkButton to load the private key
        self.go_CTkButton = ctk.CTkButton(self, text="Login", command=self.go_back)
        self.go_CTkButton.pack()


    def toggle_show_password(self):
        current_show_value = self.password_CTkEntry.cget("show")
        if current_show_value == "":
            self.password_CTkEntry.config(show="*")
            self.show_CTkButton.config(text="Show password")
        else:
            self.password_CTkEntry.config(show="")
            self.show_CTkButton.config(text="Hide password")

    def load_public_key(self):
        file_path = filedialog.askopenfilename(title="Select Public Key File")
        with open(file_path, "rb") as key_file:
            public_key = serialization.load_pem_public_key(key_file.read())
        self.public_key_CTkLabel.config(text="Public Key: " + str(public_key))

    def load_private_key(self):
        file_path = filedialog.askopenfilename(title="Select Private Key File")
        with open(file_path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None
            )
        self.private_key_CTkLabel.config(text="Private Key: " + str(private_key))

    def frame_go_to_keyGeneratorFrame(self):
        self.parent.show_frame(KeyGeneratorFrame)


if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Tk")
    root.geometry("600x400")
    login_frame = LoginFrame(root, lambda: ())
    login_frame.pack()
    root.mainloop()
