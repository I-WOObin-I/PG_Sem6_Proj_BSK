import customtkinter as ctk

import config
from gui_frames.gui_frame import GuiFrame
from gui_frames.gui_login_frame import LoginFrame
from user_manager import UserManager


class GuiManager(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode(config.CTK_APPEARANCE_MODE)
        ctk.set_default_color_theme(config.CTK_DEFAULT_COLOR_THEME)

        self.user_manager = UserManager()

        # Set the window title
        self.title("Secure Foreplay")

        # Set the window size
        self.geometry("800x600")

        self.frame_stack = []

        self.show_frame(LoginFrame)

    def go_back(self):
        try:
            self.frame_stack[-1].pack_forget()
            self.frame_stack.pop()
            self.frame_stack[-1].pack()
            self.frame_stack[-1].tkraise()

        except IndexError:
            if config.DEBUG_LOG_ON:
                print("# ERR # gui_manager.show_frame: only one frame on stack")

    def show_frame(self, frame_class_ref: GuiFrame):

        new_frame = frame_class_ref.__new__(frame_class_ref)
        new_frame.__init__(self, self.go_back, self.user_manager)

        if len(self.frame_stack) != 0:
            self.frame_stack[-1].pack_forget()

        self.frame_stack.append(new_frame)

        new_frame.pack()
        new_frame.tkraise()

    def clear_window(self):
        # Remove all widgets from the window
        for widget in self.winfo_children():
            widget.destroy()



    def show_main_menu_frame(self):
        return

if __name__ == "__main__":
    root = GuiManager()

    root.mainloop()