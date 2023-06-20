import customtkinter as ctk
from gui_frames.gui_frame import GuiFrame
from gui_frames.gui_hub_frame import HubFrame
from user_manager import UserManager

PACK_EXPAND = False
PACK_ANCHOR = ctk.CENTER


class LoginFrame(GuiFrame):
    def __init__(self, parent, callback, user_manager):
        super().__init__(parent, callback, user_manager)


        # Create a CTkLabel for the login prompt
        self.login_prompt = ctk.CTkLabel(self, text="Username:")
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


    def pack(self):
        super().pack(expand=PACK_EXPAND, anchor=PACK_ANCHOR)

    def toggle_show_password(self):
        current_show_value = self.password_CTkEntry.cget("show")
        if current_show_value == "":
            self.password_CTkEntry.configure(show="*")
            self.show_CTkButton.configure(text="Show password")
        else:
            self.password_CTkEntry.configure(show="")
            self.show_CTkButton.configure(text="Hide password")


    def login(self):
        self.user_manager.username = self.login_CTkEntry.get()
        self.user_manager.user_password = self.password_CTkEntry.get()
        self.login_CTkEntry.delete(0, ctk.END)
        self.password_CTkEntry.delete(0, ctk.END)
        self.parent.show_frame(HubFrame)


if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Tk")
    root.geometry("600x400")
    login_frame = LoginFrame(root, lambda: (), UserManager())
    login_frame.pack()
    root.mainloop()
