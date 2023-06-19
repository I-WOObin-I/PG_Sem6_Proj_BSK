'''this is the main menu frame for the gui contains:
- menu list on the left with (seperate frame class in this file):
    - a label showing the username
    - a label showing length of the keys
    - a label showing the public key fingerprint
    - a button tu load a public key
    - a label showing if the private key is loaded
    - a button to load a private key
    - a button to generate a key pair
    - a button to logout
- list of conversations on the right (seperate frame class in this file):
    - a button to start a new conversation
    - list of conversations
- current conversation in the middle (seperate frame class in this file):
    - a title label on top
    - a frame to display the conversation under the title label (seperate frame in this file):
'''

import customtkinter as ctk
from encryption.asym_key_handler import asymKeyHandler
from encryption.session_key_handler import sessionKeyHandler
from gui_frames.gui_frame import GuiFrame
from gui_frames.hub_frames.hub_chats_frame import ChatsHubFrame
from gui_frames.hub_frames.hub_conversation_frame import ConversationHubFrame
from gui_frames.hub_frames.hub_utility_frame import SettingsHubFrame

LEFT_COLUMN_WIDTH = 100
LEFT_COLUMN_COLOR = "#212121"
MIDDLE_COLUMN_COLOR = "#1a1a1a"
RIGHT_COLUMN_WIDTH = 200
RIGHT_COLUMN_COLOR = "#212121"

FRAMES_PADX = 3
FRAMES_PADY = 3

class MainMenuFrame(GuiFrame):
    def __init__(self, parent, callback):
        super().__init__(parent, callback)

        self.session_key_handler = sessionKeyHandler()
        self.asymm_key_handler = asymKeyHandler()

        self.parent = parent
        self.pack(fill="both", expand=True)

        self.columnconfigure(0, minsize=LEFT_COLUMN_WIDTH)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, minsize=RIGHT_COLUMN_WIDTH)
        self.rowconfigure(0, weight=1)

        self.settings_frame = SettingsHubFrame(self, self.asymm_key_handler, self.session_key_handler)
        self.settings_frame.grid(row=0, column=0, sticky="nsew", padx=FRAMES_PADX, pady=FRAMES_PADY)

        self.conversation_frame = ConversationHubFrame(self)
        self.conversation_frame.grid(row=0, column=1, sticky="nsew", padx=FRAMES_PADX, pady=FRAMES_PADY)

        self.chats_frame = ChatsHubFrame(self, self.asymm_key_handler, self.session_key_handler)
        self.chats_frame.grid(row=0, column=2, sticky="nsew", padx=FRAMES_PADX, pady=FRAMES_PADY)

    def show_frame(self, frame_class):
        #self.parent.show_frame(frame_class)
        pass

    def set_conversation_frame(self, conversation_frame):
        self.conversation_frame = conversation_frame
        self.conversation_frame.grid(row=0, column=1, sticky="nsew", padx=FRAMES_PADX, pady=FRAMES_PADY)

if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Tk")
    root.geometry("800x400")
    login_frame = MainMenuFrame(root, lambda: ())
    login_frame.pack(expand=True, fill="both")
    root.mainloop()
