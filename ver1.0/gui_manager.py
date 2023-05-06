import customtkinter as ctk
from gui_frames.gui_login_frame import LoginFrame
from gui_frames.gui_key_generator_frame import KeyGeneratorFrame
from gui_frames.gui_frame import GuiFrame
from gui_frames import frames_list
import config



class GuiManager(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set the window title
        self.title("Secure Foreplay")

        # Set the window size
        self.geometry("600x500")

        self.frame_stack = []

        #self.frames_list = frames_list.FRAMES_LIST

        #self.show_loginFrame(lambda :())

    def go_back(self):
        try:
            self.frame_stack[-1].pack_forget()
            self.frame_stack.pop()
            self.frame_stack[-1].tkraise()

        except IndexError:
            if config.DEBUG_LOG_ON:
                print("# ERR # gui_manager.show_frame: only one frame on stack")

    def show_frame(self, frame_class_ref: GuiFrame):
        #new_frame = frame_class_ref(self, self.go_back)

        new_frame = frame_class_ref.__new__(frame_class_ref)
        new_frame.__init__(self, self.go_back)

        if len(self.frame_stack) != 0:
            self.frame_stack[-1].pack_forget()

        self.frame_stack.append(new_frame)

        new_frame.pack(fill="both", expand=True)
        new_frame.tkraise()

    def clear_window(self):
        # Remove all widgets from the window
        for widget in self.winfo_children():
            widget.destroy()



    def show_main_menu_frame(self):
        return

if __name__ == "__main__":
    ctk.set_appearance_mode(config.CTK_APPEARANCE_MODE)
    ctk.set_default_color_theme(config.CTK_DEFAULT_COLOR_THEME)
    root = GuiManager()
    root.show_frame(frames_list.LoginFrame)

    root.mainloop()