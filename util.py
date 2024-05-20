# util.py

import tkinter as tk
from tkinter import messagebox
import sqlite3
import numpy as np
import face_recognition
import datetime
import os

def get_button(frame, text, bg, command, fg='white'):
    return tk.Button(frame, text=text, bg=bg, fg=fg, font=("Helvetica", 12), command=command, width=20, height=2)

def get_text_label(frame, text):
    return tk.Label(frame, text=text, bg="#e1e1e1", font=("Helvetica", 14))

def get_entry_text(frame):
    return tk.Text(frame, height=1, width=30, font=("Helvetica", 14))

def get_img_label(frame):
    label = tk.Label(frame)
    label.pack(pady=20)
    return label

def msg_box(title, message):
    messagebox.showinfo(title, message)

def init_db(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (name TEXT, course TEXT, batch TEXT, encoding BLOB)''')
    conn.commit()
    conn.close()

def add_user_to_db(db_path, name, course, batch, encoding):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    encoding_blob = np.array(encoding, dtype=np.float64).tobytes()  # Ensure proper dtype and conversion to bytes
    c.execute("INSERT INTO users (name, course, batch, encoding) VALUES (?, ?, ?, ?)", 
              (name, course, batch, sqlite3.Binary(encoding_blob)))
    conn.commit()
    conn.close()

def get_user_from_db(db_path, unknown_encoding):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT name, encoding FROM users")
    users = c.fetchall()
    conn.close()
    
    for user in users:
        name, encoding_blob = user
        known_encoding = np.frombuffer(encoding_blob, dtype=np.float64)  # Ensure proper dtype conversion
        results = face_recognition.compare_faces([known_encoding], unknown_encoding)
        if results[0]:
            return name
    return 'unknown_person'

def can_mark_attendance(log_path, name):
    if not os.path.exists(log_path):
        return True

    today = datetime.datetime.now().date()
    with open(log_path, 'r') as f:
        for line in f:
            logged_name, timestamp, status = line.strip().split(',')
            if logged_name == name and datetime.datetime.fromisoformat(timestamp).date() == today and status == 'in':
                return False
    return True

def calculate_attendance_percentage(log_path):
    if not os.path.exists(log_path):
        return {}

    with open(log_path, 'r') as f:
        lines = f.readlines()
    
    attendance_counts = {}
    total_days = (datetime.datetime.now() - datetime.datetime.strptime(lines[0].split(',')[1], '%Y-%m-%d %H:%M:%S.%f')).days + 1
    for line in lines:
        name, timestamp, status = line.strip().split(',')
        if status == 'in':
            if name not in attendance_counts:
                attendance_counts[name] = set()
            attendance_counts[name].add(datetime.datetime.fromisoformat(timestamp).date())
    
    attendance_percentage = {name: (len(days) / total_days) * 100 for name, days in attendance_counts.items()}
    return attendance_percentage
