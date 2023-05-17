''' class for frame that allows user to create a new profile '''
import hashlib

import customtkinter as ctk
from tkinter import messagebox

import config

from gui_frames.gui_frame import GuiFrame
from user_data_manager import UserDataManager
from user_login_handler import UserLoginHandler

PACK_EXPAND = False
PACK_ANCHOR = ctk.CENTER

class NewProfileFrame(GuiFrame):
    def __init__(self, parent, callback, user_data_manager: UserDataManager):
        super().__init__(parent, callback)

        self.parent = parent
        self.user_data_manager = user_data_manager

        # Create a CTkLabel for the login prompt
        self.login_prompt = ctk.CTkLabel(self, text="New login:")
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

        # Create a CTkLabel for the password prompt
        self.password_prompt = ctk.CTkLabel(self, text="Repeat Password:")
        self.password_prompt.pack()

        # Create an CTkEntry widget for the password
        self.rep_password_CTkEntry = ctk.CTkEntry(self, show="*")
        self.rep_password_CTkEntry.pack()

        # Create a CTkButton to Login
        self.go_CTkButton = ctk.CTkButton(self, text="Create Profile", command=self.create_profile)
        self.go_CTkButton.pack()

        # Create a CTkButton to go back
        self.go_CTkButton = ctk.CTkButton(self, text="Go Back", command=self.go_back)
        self.go_CTkButton.pack()

    def pack(self):
        super().pack(expand=PACK_EXPAND, anchor=PACK_ANCHOR)

    def create_profile(self):
        username = self.login_CTkEntry.get()
        password = self.password_CTkEntry.get()
        rep_password = self.rep_password_CTkEntry.get()

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        hashed_rep_password = hashlib.sha256(rep_password.encode()).hexdigest()
        if hashed_password != hashed_rep_password:
            if config.DEBUG_LOG_ON:
                print("# ERR # gui_new_profile.create_profile: passwords don't match")
                messagebox.showerror("Error", "Passwords don't match")
                self.password_CTkEntry.delete(0, ctk.END)
                self.rep_password_CTkEntry.delete(0, ctk.END)
                return
        else:
            file_manager = UserLoginHandler()
            file_manager.add_user(username, hashed_password)

        self.parent.go_back()

if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Tk")
    root.geometry("600x400")
    login_frame = NewProfileFrame(root, lambda: (), 0)
    login_frame.pack()
    root.mainloop()