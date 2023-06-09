from io import BytesIO

import customtkinter as ctk
from PIL import Image

import config as cfg


class Message:
    def __init__(self, type, session_key_handler, data=None):
        self.type = type
        self.text = None
        self.file = None
        self.file_name = "file"
        if type == "t":
            self.text = data
        elif type == "f":
            self.file = data

        self.message_frame = None
        self.progressbar = None

        self.session_key_handler = session_key_handler

        self.message_button = None

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
                message_button = ctk.CTkButton(message_frame, text=self.file_name, fg_color=cfg.MESSAGE_BACKGROUND_COLOR, corner_radius=10, command=self.save_file)
                message_button.pack()
                return message_frame
            except:
                message_frame = ctk.CTkFrame(parent_frame, fg_color="transparent", corner_radius=10)
                self.message_button = ctk.CTkButton(message_frame, text=self.file_name, fg_color=cfg.MESSAGE_BACKGROUND_COLOR, corner_radius=10, command=self.save_file)
                self.message_button.pack()
                self.message_frame = message_frame
                return message_frame


    def save_file(self):
        if self.type == "t":
            return

        file_path = ctk.filedialog.asksaveasfilename(title="Save File", initialfile=self.file_name, filetypes=[("All Files", "*.*")])
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

    def decrypt_file(self):
        self.file_name, self.file = self.session_key_handler.decrypt_file(self.file)
        self.message_button.configure(text=self.file_name)
