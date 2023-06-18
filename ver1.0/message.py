import customtkinter as ctk
import config as cfg
from PIL import Image, ImageTk


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
            message_frame = ctk.CTkFrame(parent_frame, fg_color="transparent", corner_radius=10)
            message_button = ctk.CTkButton(message_frame, text="save file", fg_color=cfg.MESSAGE_BACKGROUND_COLOR, corner_radius=10, command=self.save_file)
            message_button.pack()
            self.message_frame = message_frame
            return message_frame

            # try:
            #     with Image.open(self.file) as image:
            #         imageTk = ctk.CTkImage(image)
            #         message_frame = ctk.CTkFrame(parent_frame, fg_color="transparent", corner_radius=10)
            #         message_label = ctk.CTkLabel(message_frame, fg_color=cfg.MESSAGE_BACKGROUND_COLOR, corner_radius=10, image=imageTk)
            #         message_label.pack()
            #         return message_frame
            # except IOError:
            #     # file cant be displayed as an image


    def save_file(self):
        if self.type == "t":
            return

        file_path = ctk.filedialog.asksaveasfilename(title="Save File", filetypes=[("All Files", "*.*")])
        if file_path:
            # Save the file to the chosen location
            with open(file_path, 'wb') as file:
                file.write(self.file)

    def set_progressbar(self, length):
        self.progressbar = ctk.CTkProgressBar(self.message_frame)
        self.progressbar.pack(fill="x")
        self.progressbar_length = length

    def step_progressbar(self, progress):
        self.progressbar['determinate_speed'] = progress / self.progressbar_length
        self.progressbar.step()
        pass
