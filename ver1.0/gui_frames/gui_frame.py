
import customtkinter as ctk
import config

class GuiFrame(ctk.CTkFrame):

    def __init__(self, parent, callback):
        super().__init__(parent)
        self.parent = parent
        self.callback = callback

    def go_back(self):
        self.callback()

    def pack(self, *args, **kwargs):
        super().pack(ipadx=config.PADX, ipady=config.PADY, *args, **kwargs)
