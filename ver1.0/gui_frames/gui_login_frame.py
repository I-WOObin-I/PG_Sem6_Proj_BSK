import hashlib

import customtkinter as ctk
from tkinter import messagebox

from gui_frames.gui_frame import GuiFrame
from gui_frames.gui_key_generator_frame import KeyGeneratorFrame
from gui_frames.gui_hub_frame import MainMenuFrame
from gui_frames.gui_new_profile import NewProfileFrame
from user_data_manager import UserDataManager
from user_login_handler import UserLoginHandler

PACK_EXPAND = False
PACK_ANCHOR = ctk.CENTER


class LoginFrame(GuiFrame):
    def __init__(self, parent, callback, user_data_manager: UserDataManager):
        super().__init__(parent, callback)

        self.parent = parent
        self.user_data_manager = user_data_manager

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

        # Create a CTkButton to Login
        self.go_CTkButton = ctk.CTkButton(self, text="Login", command=self.login)
        self.go_CTkButton.pack()

        # Create a CTkButton to create a new profile
        self.go_CTkButton = ctk.CTkButton(self, text="Create New Profile", command=self.create_new_profile)
        self.go_CTkButton.pack()

    def pack(self):
        super().pack(expand=PACK_EXPAND, anchor=PACK_ANCHOR)

    def toggle_show_password(self):
        current_show_value = self.password_CTkEntry.cget("show")
        if current_show_value == "":
            self.password_CTkEntry.config(show="*")
            self.show_CTkButton.config(text="Show password")
        else:
            self.password_CTkEntry.config(show="")
            self.show_CTkButton.config(text="Hide password")

    def frame_go_to_keyGeneratorFrame(self):
        self.parent.show_frame(KeyGeneratorFrame)

    def login(self):
        username = self.login_CTkEntry.get()
        password = self.password_CTkEntry.get()
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        user_login_handler = UserLoginHandler()
        if user_login_handler.validate_user(username, password_hash):
            self.user_data_manager.set_username(self.login_CTkEntry.get())
            self.user_data_manager.set_password(self.password_CTkEntry.get())
            self.parent.show_frame(MainMenuFrame)
        else:
            print("Wrong password")
            messagebox.showerror("Error", "Wrong password or username")
    def create_new_profile(self):
        self.parent.show_frame(NewProfileFrame)

if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Tk")
    root.geometry("600x400")
    login_frame = LoginFrame(root, lambda: ())
    login_frame.pack()
    root.mainloop()
