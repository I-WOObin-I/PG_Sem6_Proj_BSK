from time import sleep

import customtkinter as ctk
root = ctk.CTk()
root.title("Tk")
root.geometry("800x400")

max = 18000
step = 4000
current = 0
progress_bar = ctk.CTkProgressBar(root, determinate_speed=max/step*2)
progress_bar.set(0)
progress_bar.pack(fill="x")
root.mainloop()

while current < max:
    current += step
    progress_bar.step()
    print(progress_bar.get())
    sleep(0.2)
progress_bar.step()
print(progress_bar.get())
#progress_bar.step()


