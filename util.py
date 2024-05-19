import os
import sqlite3
import tkinter as tk
from tkinter import messagebox
import face_recognition
import pickle

def init_db(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (name TEXT PRIMARY KEY, course TEXT, batch TEXT, encoding BLOB)''')
    conn.commit()
    conn.close()



def add_user_to_db(db_path, name, course, batch, encoding):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    encoding_pickled = pickle.dumps(encoding)
    c.execute("INSERT INTO users (name, course, batch, encoding) VALUES (?, ?, ?, ?)", (name, course, batch, encoding_pickled))
    conn.commit()
    conn.close()

def get_user_from_db(db_path, unknown_encoding):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT name, encoding FROM users")
    users = c.fetchall()
    conn.close()

    for user in users:
        name, encoding_pickled = user
        known_encoding = pickle.loads(encoding_pickled)
        match = face_recognition.compare_faces([known_encoding], unknown_encoding)[0]
        if match:
            return name

    return 'unknown_person'

def get_button(window, text, color, command, fg='white'):
    button = tk.Button(
        window,
        text=text,
        activebackground="black",
        activeforeground="white",
        fg=fg,
        bg=color,
        command=command,
        height=2,
        width=20,
        font=('Helvetica bold', 20)
    )
    return button

def get_img_label(window):
    label = tk.Label(window)
    label.grid(row=0, column=0)
    return label

def get_text_label(window, text):
    label = tk.Label(window, text=text)
    label.config(font=("sans-serif", 21), justify="left")
    return label

def get_entry_text(window):
    inputtxt = tk.Text(window, height=2, width=15, font=("Arial", 32))
    return inputtxt

def msg_box(title, description):
    messagebox.showinfo(title, description)
