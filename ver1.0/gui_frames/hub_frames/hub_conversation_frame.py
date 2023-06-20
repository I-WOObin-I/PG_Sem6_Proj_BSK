import tkinter

import config as cfg
import customtkinter as ctk
from message import Message


class ConversationHubFrame(ctk.CTkFrame):
    def __init__(self, parent, conversation_name="Conversation"):
        super().__init__(parent)

        self.conversation_name = conversation_name

        self.configure(fg_color=cfg.HUB_MIDDLE_COLUMN_COLOR)

        # Create conversation label for title
        # it spreads over the whole width of the frame
        # has black background and white text
        self.conversation_title_frame = ctk.CTkFrame(self)
        self.conversation_label = ctk.CTkLabel(self.conversation_title_frame, text=self.conversation_name)
        self.conversation_label.pack(fill="x")
        self.conversation_title_frame.pack(fill="x")

        # Create conversation frame
        self.conversation_frame = ctk.CTkScrollableFrame(self, fg_color=cfg.HUB_MIDDLE_COLUMN_COLOR)
        self.conversation_frame.pack(fill="both", expand=True)

        self.send_file_button = ctk.CTkButton(self, text="Send File", command=self.send_file_message, width=50)
        self.send_file_button.pack(fill="x", side=tkinter.LEFT)

        self.sendbox = ctk.CTkEntry(self)
        self.sendbox.bind("<Return>", self.send_text_message)
        self.sendbox.pack(fill="x", side=tkinter.LEFT, expand=True)

        self.send_button = ctk.CTkButton(self, text="Send", command=self.send_text_message, width=50)
        self.send_button.pack(side=tkinter.LEFT)

    def set_conversation_handler(self, conversation_handler):
        self.conversation_handler = conversation_handler

    def add_message(self, message_type, data, local_sender):
        new_message = Message(message_type, self.conversation_handler.session_key_handler, data)
        outer_frame = ctk.CTkFrame(self.conversation_frame, fg_color=cfg.HUB_MIDDLE_COLUMN_COLOR)
        new_message_frame = new_message.get_frame(outer_frame)
        if local_sender:
            new_message_frame.pack(fill="x", side=tkinter.RIGHT, )
            outer_frame.pack(fill="x")
        else:
            new_message_frame.pack(fill="x", side=tkinter.LEFT)
            outer_frame.pack(fill="x")

        return new_message

    def send_text_message(self, event=None):
        text = self.sendbox.get()
        if text == "":
            return
        self.conversation_handler.send_text(text)
        self.sendbox.delete(0, "end")

    def send_file_message(self):
        file_path = ctk.filedialog.askopenfilename(title="Select file to send")
        if file_path == "":
            return

        self.conversation_handler.send_file(file_path)


