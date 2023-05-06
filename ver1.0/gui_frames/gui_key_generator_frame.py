import tkinter as tk
import customtkinter as ctk
from customtkinter import filedialog
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from gui_frames.gui_frame import GuiFrame


OPTIONS = [2048, 4096, 8192]
PUBLIC_EXPONENT = 65537
CTkLabel_LENGTH = 60

class KeyGeneratorFrame(GuiFrame):
    def __init__(self, parent, callback):
        super().__init__(parent, callback)

        self.parent = parent

        # Create a CTkLabel for the key size prompt
        key_size_prompt = ctk.CTkLabel(self, text="Key Size (in bits):")
        key_size_prompt.pack()

        # Create an entry widget for the key size
        self.key_size_value = ctk.StringVar()
        self.key_size_value.set(str(OPTIONS[0]))
        self.key_size_entry = ctk.CTkOptionMenu(self, values=[str(option) for option in OPTIONS])
        #self.key_size_entry = tk.OptionMenu(self, self.key_size_value, *OPTIONS)
        self.key_size_entry.pack()

        # Create a CTkButton to generate the public and private keys
        generate_CTkButton = ctk.CTkButton(self, text="Generate Keys", command=self.generate_keys)
        generate_CTkButton.pack(pady=10)

        # Create a CTkLabel to display the public key
        self.public_key_CTkLabel = ctk.CTkLabel(self, text="\n\n\n", width=CTkLabel_LENGTH)
        self.public_key_CTkLabel.pack()

        # Create a CTkButton to save the public key
        save_public_CTkButton = ctk.CTkButton(self, text="Save Public Key", command=self.save_public_key)
        save_public_CTkButton.pack(pady=10)

        # Create a CTkLabel to display the private key
        self.private_key_CTkLabel = ctk.CTkLabel(self, text="\n\n\n", width=CTkLabel_LENGTH)
        self.private_key_CTkLabel.pack()

        # Create a CTkButton to save the private key
        save_private_CTkButton = ctk.CTkButton(self, text="Save Private Key", command=self.save_private_key)
        save_private_CTkButton.pack(pady=10)

        # Create a CTkButton to go back to login page
        save_private_CTkButton = ctk.CTkButton(self, text="Back", command=self.go_back)
        save_private_CTkButton.pack(pady=10)

    def generate_keys(self):
        # Generate the private key
        private_key = rsa.generate_private_key(
            public_exponent=PUBLIC_EXPONENT,
            key_size=int(self.key_size_value.get())
        )

        # Serialize the private key to PEM format
        pem_private_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        # Display the private key
        self.private_key_CTkLabel.config(text="Private Key:\n" + "GENERATED\n" + "*****" + "\n(" + str(self.key_size_value.get()) + ")")

        # Extract the public key from the private key
        public_key = private_key.public_key()

        # Serialize the public key to PEM format
        pem_public_key = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        # Display the public key
        self.public_key_CTkLabel.config(text="Public Key:\n" + "GENERATED\n" +str(pem_public_key) + "\n(" + str(self.key_size_value.get()) + ")")

        # Store the private and public keys in instance variables
        self.private_key = pem_private_key
        self.public_key = pem_public_key

    def save_public_key(self):
        # Get the file path to save the public key
        file_path = filedialog.asksaveasfilename(title="Save Public Key As", defaultextension=".pem")

        # Write the public key to the file
        with open(file_path, "wb") as key_file:
            key_file.write(self.public_key)

    def save_private_key(self):
        # Get the file path to save the private key
        file_path = filedialog.asksaveasfilename(title="Save Private Key As", defaultextension=".pem")

        # Write the private key to the file
        with open(file_path, "wb") as key_file:
            key_file.write(self.private_key)

if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Tk")
    root.geometry("600x400")
    root.update()
    key_generator_frame = KeyGeneratorFrame(root, lambda: ())
    key_generator_frame.pack()
    root.mainloop()