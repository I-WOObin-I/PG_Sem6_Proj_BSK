from io import BytesIO

import customtkinter as ctk
from PIL import Image

import config as cfg


class Message:
    def __init__(self, type, data=None):
        self.type = type
        self.text = None
        self.file = None
        if type == "t":
            self.text = data
        elif type == "f":
            self.file = data

        self.message_frame = None
        self.progressbar = None

    def get_frame(self, parent_frame):

        if self.type == "t":
            message_frame = ctk.CTkFrame(parent_frame, fg_color="transparent", corner_radius=10)
            message_label = ctk.CTkLabel(message_frame, text=self.text, fg_color=cfg.MESSAGE_BACKGROUND_COLOR, corner_radius=10)
            message_label.pack()
            self.message_frame = message_frame
            return message_frame

        elif self.type == "f":
            try:
                image_stream = BytesIO(self.file)
                image = Image.open(image_stream)
                imageTk = ctk.CTkImage(image, size=(200, 200))
                message_frame = ctk.CTkFrame(parent_frame, fg_color="transparent", corner_radius=10)
                message_label = ctk.CTkLabel(message_frame, text="", fg_color=cfg.MESSAGE_BACKGROUND_COLOR, corner_radius=10, image=imageTk, height=220)
                message_label.pack(expand=True)
                message_button = ctk.CTkButton(message_frame, text="save file", fg_color=cfg.MESSAGE_BACKGROUND_COLOR, corner_radius=10, command=self.save_file)
                message_button.pack()
                return message_frame
            except:
                message_frame = ctk.CTkFrame(parent_frame, fg_color="transparent", corner_radius=10)
                message_button = ctk.CTkButton(message_frame, text="save file", fg_color=cfg.MESSAGE_BACKGROUND_COLOR, corner_radius=10, command=self.save_file)
                message_button.pack()
                self.message_frame = message_frame
                return message_frame


    def save_file(self):
        if self.type == "t":
            return

        file_path = ctk.filedialog.asksaveasfilename(title="Save File", filetypes=[("All Files", "*.*")])
        if file_path:
            # Save the file to the chosen location
            with open(file_path, 'wb') as file:
                file.write(self.file)

    def set_progressbar(self):
        self.progressbar = ctk.CTkProgressBar(self.message_frame)
        self.progressbar.set(0)
        self.progressbar.pack(fill="x")

    def set_progressbar_value(self, value):
        self.progressbar.set(value)

    def finish_progressbar(self):
        self.progressbar.destroy()
