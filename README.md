# PG_Sem6_Proj_BSK
project repository for subject Bezpieczenstwo Systemow Komputerowych (Computer Systems Security)

to run app you first need to setup a python enviroment with following packages:
- import customtkinter
- from cryptography.hazmat.primitives import serialization
- from cryptography.hazmat.primitives.asymmetric import rsa
- from cryptography.fernet import Fernet
- import json
- import os
- from tkinter import messagebox

to run app run main() in gui_manager.py

# conventions

chat - chat object containing all messeges, name of conversation and its symmetric key for communication
conversation - list of all messeges

# file conventions

- users.json - file for all users in local machine
  - username -
  - password hash -
  - user keys file name - name to file contaning all chat files keys and names
    note: this is only file name, user password is needed to decrypt this file
- <user_keys>.json - encrypted file containing all chat file names and keys to decrypt them
  - chat name - name for given chat
  - chat file name - file name containing whole encrypted chat
  - chat key - key to decrypt chat file
- <chat_file>.json - file containing name, symmetric key and all messeges 
  - chat name - name for given chat
  - chat key - symmetric key used in communication over unsecured channel
  - chat conversation <dictionary list> [
    - username - username that sent messege
    - time stamp - time when messege was received
    - messege - messege encrypted with symmetric key
    ]
  
