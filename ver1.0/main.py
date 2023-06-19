import tkinter as tk
from tkinter import filedialog

def show_password():
    password = password_entry.get()
    password_label.config(text="Password: " + password)

def load_public_key():
    file_path = filedialog.askopenfilename(title="Select Public Key File")
    with open(file_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(key_file.read())
    public_key_label.config(text="Public Key: " + str(public_key))

def load_private_key():
    file_path = filedialog.askopenfilename(title="Select Private Key File")
    with open(file_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )
    private_key_label.config(text="Private Key: " + str(private_key))

root = tk.Tk()
root.title("Hello World")

# Create a label for the "Hello World!" text
hello_label = tk.Label(root, text="Hello World!")
hello_label.pack()

# Create a label for the password prompt
password_prompt = tk.Label(root, text="Enter your password:")
password_prompt.pack()

# Create an entry widget for the password
password_entry = tk.Entry(root, show="*")
password_entry.pack()

# Create a button to show the password
show_button = tk.Button(root, text="Show Password", command=show_password)
show_button.pack()

# Create a button to load the public key
public_key_button = tk.Button(root, text="Load Public Key", command=load_public_key)
public_key_button.pack()

# Create a label to display the public key
public_key_label = tk.Label(root, text="")
public_key_label.pack()

# Create a button to load the private key
private_key_button = tk.Button(root, text="Load Private Key", command=load_private_key)
private_key_button.pack()

# Create a label to display the private key
private_key_label = tk.Label(root, text="")
private_key_label.pack()

root.mainloop()
