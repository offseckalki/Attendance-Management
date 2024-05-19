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

        self.main_window.title("Meerut Institute of Technology")

        self.login_button_main_window = util.get_button(self.main_window, 'Mark Attendance', 'green', self.login)
        self.login_button_main_window.place(x=750, y=200)

        self.logout_button_main_window = util.get_button(self.main_window, 'Early Dismissal', 'red', self.logout)
        self.logout_button_main_window.place(x=750, y=300)

        self.register_new_user_button_main_window = util.get_button(self.main_window, 'Register new user', 'gray', self.register_new_user, fg='black')
        self.register_new_user_button_main_window.place(x=750, y=400)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

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

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label)

        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window, 'Please, Enter username:')
        self.text_label_register_new_user.place(x=750, y=20)

        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=750, y=70)

        self.text_label_course = util.get_text_label(self.register_new_user_window, 'Please, Enter Course/Department:')
        self.text_label_course.place(x=750, y=140)

        self.entry_text_course = util.get_entry_text(self.register_new_user_window)
        self.entry_text_course.place(x=750, y=190)

        self.text_label_batch = util.get_text_label(self.register_new_user_window, 'Please, Enter Batch/Year:')
        self.text_label_batch.place(x=750, y=260)

        self.entry_text_batch = util.get_entry_text(self.register_new_user_window)
        self.entry_text_batch.place(x=750, y=310)

        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept', 'green', self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=750, y=380)

        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try again', 'red', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=750, y=450)

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
        util.msg_box('Success!', 'User was registered successfully!')
        self.register_new_user_window.destroy()

if __name__ == "__main__":
    app = App()
    app.start()
