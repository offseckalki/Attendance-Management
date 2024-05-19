import sqlite3
import os
import tkinter as tk
from tkinter import messagebox
import face_recognition
import pickle

def get_button(window, text, color, command, fg='white'):
    return tk.Button(
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

def get_img_label(window):
    label = tk.Label(window)
    label.grid(row=0, column=0)
    return label

def get_text_label(window, text):
    label = tk.Label(window, text=text)
    label.config(font=("sans-serif", 21), justify="left")
    return label

def get_entry_text(window):
    return tk.Text(window, height=2, width=15, font=("Arial", 32))

def msg_box(title, description):
    messagebox.showinfo(title, description)

def init_db(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY,
                 name TEXT NOT NULL,
                 embedding BLOB NOT NULL)''')
    conn.commit()
    conn.close()

def add_user_to_db(db_path, name, embedding):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO users (name, embedding) VALUES (?, ?)", (name, pickle.dumps(embedding)))
    conn.commit()
    conn.close()

def get_user_from_db(db_path, embedding_to_compare):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT name, embedding FROM users")
    users = c.fetchall()
    conn.close()

    for name, embedding_blob in users:
        embedding = pickle.loads(embedding_blob)
        if face_recognition.compare_faces([embedding], embedding_to_compare)[0]:
            return name
    return 'unknown_person'
