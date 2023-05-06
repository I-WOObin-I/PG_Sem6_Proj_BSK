import abc

import tkinter as tk
import customtkinter as ctk


class GuiFrame(ctk.CTkFrame):

    def __int__(self, parent, callback):
        super().__init__(parent)
        self.parent = parent
        self.callback = callback

    def go_back(self):
        print("go_back")
        print(self.callback)
        self.callback()
