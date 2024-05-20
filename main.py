import os
import datetime
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import face_recognition
import util

class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x600+350+100")
        self.main_window.title("Attendance Management System")
        self.main_window.configure(bg="#e1e1e1")

        title_label = tk.Label(self.main_window, text="MEERUT INSTITUTE OF TECHNOLOGY", font=("Helvetica", 28, "bold"), bg="#FF4242", fg="#FFFFFF", padx=20, pady=10)
        title_label.pack(pady=20)

        button_frame = tk.Frame(self.main_window, bg="#e1e1e1")
        button_frame.pack(pady=50)

        self.login_button = util.get_button(button_frame, 'Mark Attendance', '#4CAF50', self.login)
        self.login_button.pack(side=tk.LEFT, padx=20, pady=10)

        self.logout_button = util.get_button(button_frame, 'Early Dismissal', '#FF5733', self.logout)
        self.logout_button.pack(side=tk.LEFT, padx=20, pady=10)

        self.register_button = util.get_button(button_frame, 'Register new user', '#808080', self.register_new_user, fg='black')
        self.register_button.pack(side=tk.LEFT, padx=20, pady=10)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.pack(pady=20)

        self.add_webcam(self.webcam_label)

        self.db_path = './users.db'
        util.init_db(self.db_path)
        self.log_path = './log.txt'

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)  # Default camera index

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()

        if not ret:
            print("Failed to capture image from webcam")
            self._label.after(20, self.process_webcam)
            return

        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)

    def login(self):
        embeddings_unknown = face_recognition.face_encodings(self.most_recent_capture_arr)
        if not embeddings_unknown:
            util.msg_box('Error', 'No face found.')
            return

        name = util.get_user_from_db(self.db_path, embeddings_unknown[0])
        if name == 'unknown_person':
            util.msg_box('Ups...', 'Unknown user. Please register new user or try again.')
        else:
            util.msg_box('Welcome back!', f'Welcome, {name}.')
            with open(self.log_path, 'a') as f:
                f.write(f'{name},{datetime.datetime.now()},in\n')

    def logout(self):
        embeddings_unknown = face_recognition.face_encodings(self.most_recent_capture_arr)
        if not embeddings_unknown:
            util.msg_box('Error', 'No face found.')
            return

        name = util.get_user_from_db(self.db_path, embeddings_unknown[0])
        if name == 'unknown_person':
            util.msg_box('Ups...', 'Unknown user. Please register new user or try again.')
        else:
            util.msg_box('Hasta la vista!', f'Goodbye, {name}.')
            with open(self.log_path, 'a') as f:
                f.write(f'{name},{datetime.datetime.now()},out\n')

    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x600+370+120")
        self.register_new_user_window.title("Register New User")
        self.register_new_user_window.configure(bg="#e1e1e1")

        title_label = tk.Label(self.register_new_user_window, text="Register New User", font=("Helvetica", 24, "bold"), bg="#4CAF50", fg="#ffffff", padx=20, pady=10)
        title_label.pack(pady=20)

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.pack(pady=20)

        self.add_img_to_label(self.capture_label)

        form_frame = tk.Frame(self.register_new_user_window, bg="#e1e1e1")
        form_frame.pack(pady=20)

        username_label = util.get_text_label(form_frame, 'Please, Enter username:')
        username_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.entry_text_register_new_user = util.get_entry_text(form_frame)
        self.entry_text_register_new_user.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        course_label = util.get_text_label(form_frame, 'Please, Enter Course/Department:')
        course_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.entry_text_course = util.get_entry_text(form_frame)
        self.entry_text_course.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        batch_label = util.get_text_label(form_frame, 'Please, Enter Batch/Year:')
        batch_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

        self.entry_text_batch = util.get_entry_text(form_frame)
        self.entry_text_batch.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        button_frame = tk.Frame(self.register_new_user_window, bg="#e1e1e1")
        button_frame.pack(pady=20)

        accept_button = util.get_button(button_frame, 'Accept', '#4CAF50', self.accept_register_new_user)
        accept_button.pack(side=tk.LEFT, padx=20, pady=10)

        try_again_button = util.get_button(button_frame, 'Try again', '#FF5733', self.try_again_register_new_user)
        try_again_button.pack(side=tk.LEFT, padx=20, pady=10)

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)
        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def start(self):
        self.main_window.mainloop()

    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get(1.0, "end-1c")
        course = self.entry_text_course.get(1.0, "end-1c")
        batch = self.entry_text_batch.get(1.0, "end-1c")

        embeddings = face_recognition.face_encodings(self.register_new_user_capture)
        if not embeddings:
            util.msg_box('Error', 'No face found. Please try again.')
            return

        util.add_user_to_db(self.db_path, name, course, batch, embeddings[0])
        util.msg_box('Success', 'User registered successfully.')
        self.register_new_user_window.destroy()

if __name__ == "__main__":
    app = App()
    app.start()
