import config as cfg
import customtkinter as ctk
from conversation_handler import ConversationHandler
from gui_frames.hub_frames.hub_conversation_frame import ConversationHubFrame


class ChatsHubFrame(ctk.CTkFrame):
    def __init__(self, parent, user_manager):
        super().__init__(parent)

        self.parent = parent
        self.user_manager = user_manager
        self.asym_key_handler = user_manager.asym_key_handler
        self.session_key_handler = user_manager.session_key_handler

        self.configure(fg_color=cfg.HUB_RIGHT_COLUMN_COLOR)

        self.address_entry = ctk.CTkEntry(self, placeholder_text="address")
        self.address_entry.insert(0, "localhost")
        self.address_entry.pack()

        self.port_entry = ctk.CTkEntry(self, placeholder_text="port")
        self.port_entry.insert(0, "5001")
        self.port_entry.pack()

        # Create buttons
        self.new_conversation_button = ctk.CTkButton(self, text="New Conversation", command=self.new_conversation_button_action)

        self.connect_button = ctk.CTkButton(self, text="Connect", command=self.connect_button_action)

        # Pack buttons
        self.new_conversation_button.pack(fill="x")
        self.connect_button.pack(fill="x")

        self.log_frame = ctk.CTkScrollableFrame(self)
        self.log_frame.pack(fill="both", expand=True)

    def new_conversation_button_action(self):
        address = self.address_entry.get()
        port = self.port_entry.get()
        hub_conversation_frame = ConversationHubFrame(self.parent, "waiting for connection...")
        self.parent.set_conversation_frame(hub_conversation_frame)
        new_conversation_handler = ConversationHandler(address, port, hub_conversation_frame, self, self.user_manager)
        new_conversation_handler.new_conversation()

    def connect_button_action(self):
        address = self.address_entry.get()
        port = self.port_entry.get()
        hub_conversation_frame = ConversationHubFrame(self.parent, "waiting for connection...")
        self.parent.set_conversation_frame(hub_conversation_frame)
        new_conversation_handler = ConversationHandler(address, port, hub_conversation_frame, self, self.user_manager)
        new_conversation_handler.connect()

    def log(self, text):
        new_label = ctk.CTkLabel(self.log_frame, text=text, anchor='w', justify='left', wraplength=150)
        new_label.pack()


