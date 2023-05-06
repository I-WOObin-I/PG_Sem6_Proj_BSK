import customtkinter as ctk
from gui_frames.gui_login_frame import LoginFrame
from gui_frames.gui_key_generator_frame import KeyGeneratorFrame
from gui_frames.frame_switcher_interface import GuiFrameID
from gui_frames.gui_frame import GuiFrame
import config



class GuiManager(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set the window title
        self.title("Quick Safe Messenger")

        # Set the window size
        self.geometry("600x500")

        self.frame_stack = []

        self.show_loginFrame(lambda :())




    def clear_window(self):
        # Remove all widgets from the window
        for widget in self.winfo_children():
            widget.destroy()

    def show_frame(self, frame_id: GuiFrameID):
        frame_dictionary = {
            GuiFrameID.LOGIN: LoginFrame,
            GuiFrameID.KEY_GENERATOR: KeyGeneratorFrame,
        }
        try:
            frame_class_ref = frame_dictionary.get(frame_id)
            frame:GuiFrame = frame_class_ref(self, self.go_back())
            frame = frame_class_ref.__new__(frame_class_ref)
            GuiFrame.__init__(frame, self, self.go_back)

            self.frame_stack.append(frame)
            frame.tkraise(self)

        except KeyError:
            if config.DEBUG_LOG_ON:
                print("# ERR # gui_manager.show_frame: invalid frame ID")


    def go_back(self):
        try:
            self.frame_stack[-2].tkraise()
            self.frame_stack.pop()

        except IndexError:
            if config.DEBUG_LOG_ON:
                print("# ERR # gui_manager.show_frame: only one frame on stack")




    def show_loginFrame(self, callback):
        self.clear_window()
        login_frame = LoginFrame(self, callback)
        login_frame.pack()

    def show_KeyGeneratorFrame(self, callback):
        self.clear_window()
        key_generator_frame = KeyGeneratorFrame(self, callback)
        key_generator_frame.pack()


    def show_main_menu_frame(self):
        return

if __name__ == "__main__":
    ctk.set_appearance_mode(config.CTK_APPEARANCE_MODE)
    ctk.set_default_color_theme(config.CTK_DEFAULT_COLOR_THEME)
    root = GuiManager()

    root.mainloop()