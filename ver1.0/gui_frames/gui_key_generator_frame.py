import customtkinter as ctk

from encryption.asym_key_handler import asymKeyHandler
from gui_frames.gui_frame import GuiFrame
import config as cfg

FRAME_WIDTH = 2000
CTkLabel_LENGTH = 60

class KeyGeneratorFrame(GuiFrame):
    def __init__(self, parent, callback, asym_key_handler):
        super().__init__(parent, callback)

        self.parent = parent
        self.asym_key_handler = asym_key_handler
        self.key_lenght_options = self.asym_key_handler.get_key_lengths()
        self.configure(width=FRAME_WIDTH)

        # Create a CTkLabel for the key size prompt
        key_size_prompt = ctk.CTkLabel(self, text="Key Size (in bits):")
        key_size_prompt.pack()

        # Create an entry widget for the key size
        self.key_size_value = ctk.StringVar()
        self.key_size_value.set(str(self.key_lenght_options[0]))
        self.key_size_entry = ctk.CTkOptionMenu(self, values=[str(option) for option in self.key_lenght_options])
        self.key_size_entry.pack()

        # Create a CTkButton to generate the public and private keys
        generate_CTkButton = ctk.CTkButton(self, text="Generate Keys", command=self.generate_keys_button_action)
        generate_CTkButton.pack(pady=10)

        # Create a CTkLabel to display the public key
        self.public_key_CTkLabel = ctk.CTkLabel(self, text="\n\n\n", width=CTkLabel_LENGTH)
        self.public_key_CTkLabel.pack()

        # Create a CTkButton to save the public key
        save_public_CTkButton = ctk.CTkButton(self, text="Save Public Key", command=self.save_public_key_button_action)
        save_public_CTkButton.pack(pady=10)

        # Create a CTkLabel to display the private key
        self.private_key_CTkLabel = ctk.CTkLabel(self, text="\n\n\n", width=CTkLabel_LENGTH)
        self.private_key_CTkLabel.pack()

        # Create a CTkButton to save the private key
        save_private_CTkButton = ctk.CTkButton(self, text="Save Private Key", command=self.save_private_key_button_action)
        save_private_CTkButton.pack(pady=10)

        # Create a CTkButton to go back to login page
        save_private_CTkButton = ctk.CTkButton(self, text="Back", command=self.go_back)
        save_private_CTkButton.pack(pady=10)

    def generate_keys_button_action(self):
        public_key_fingerprint = self.asym_key_handler.generate_keys(int(self.key_size_value.get()))
        self.public_key_CTkLabel.configure(text="public key generated\n fingerprint: \n" + public_key_fingerprint)
        self.private_key_CTkLabel.configure(text="private key generated\n" + "*****")

    def save_public_key_button_action(self):
        file_path = ctk.filedialog.asksaveasfilename(title="Save Public Key As", initialfile=cfg.DEFAULT_PUBLIC_KEY_FILE_NAME, filetypes=cfg.KEY_FILE_TYPES)
        if file_path == '':
            return
        self.asym_key_handler.encrypt_and_save_public_key(file_path)

    def save_private_key_button_action(self):
        file_path = ctk.filedialog.asksaveasfilename(title="Save Private Key As", initialfile=cfg.DEFAULT_PUBLIC_KEY_FILE_NAME, filetypes=cfg.KEY_FILE_TYPES)
        if file_path == '':
            return
        self.asym_key_handler.encrypt_and_save_private_key(file_path)


if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Tk")
    root.geometry("600x400")
    root.update()
    key_generator_frame = KeyGeneratorFrame(root, lambda: (), asymKeyHandler())
    key_generator_frame.pack()
    root.mainloop()