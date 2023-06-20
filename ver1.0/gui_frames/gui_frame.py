
import config
import customtkinter as ctk


class GuiFrame(ctk.CTkFrame):

    def __init__(self, parent, callback, user_manager):
        super().__init__(parent)
        self.parent = parent
        self.user_manager = user_manager
        self.callback = callback

    def go_back(self):
        self.callback()

    def pack(self, *args, **kwargs):
        super().pack(ipadx=config.PADX, ipady=config.PADY, *args, **kwargs)
