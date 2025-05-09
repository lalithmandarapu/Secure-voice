import tkinter as tk
from tkinter import messagebox
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import base64
import pyttsx3

# Derive AES key from password
def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

# Encrypt message
def encrypt_message(message, password):
    salt = os.urandom(16)
    key = derive_key(password, salt)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ct = encryptor.update(message.encode()) + encryptor.finalize()
    return base64.b64encode(salt + iv + ct).decode()

# Decrypt message
def decrypt_message(enc_message, password):
    raw = base64.b64decode(enc_message)
    salt = raw[:16]
    iv = raw[16:32]
    ct = raw[32:]
    key = derive_key(password, salt)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return (decryptor.update(ct) + decryptor.finalize()).decode()

# Text-to-speech
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# GUI Application
class SecureVoiceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SecureVoice Communication")
        self.password = None

        # Login Frame
        self.login_frame = tk.Frame(root)
        tk.Label(self.login_frame, text="Enter Password:").pack()
        self.pass_entry = tk.Entry(self.login_frame, show="*")
        self.pass_entry.pack()
        tk.Button(self.login_frame, text="Login", command=self.authenticate).pack()
        self.login_frame.pack()

        # Main Frame
        self.main_frame = tk.Frame(root)
        tk.Label(self.main_frame, text="Enter Message:").pack()
        self.message_entry = tk.Entry(self.main_frame, width=40)
        self.message_entry.pack()

        tk.Button(self.main_frame, text="Encrypt & Speak", command=self.encrypt_and_speak).pack()
        tk.Button(self.main_frame, text="Decrypt Last Message", command=self.decrypt_last_message).pack()

        self.encrypted_msg = ""

    def authenticate(self):
        pwd = self.pass_entry.get()
        if pwd:
            self.password = pwd
            self.login_frame.pack_forget()
            self.main_frame.pack()
        else:
            messagebox.showerror("Error", "Password required")

    def encrypt_and_speak(self):
        msg = self.message_entry.get()
        if msg:
            try:
                self.encrypted_msg = encrypt_message(msg, self.password)
                speak(msg)
                messagebox.showinfo("Encrypted Message", self.encrypted_msg)
            except Exception as e:
                messagebox.showerror("Error", f"Encryption failed: {str(e)}")
        else:
            messagebox.showerror("Error", "Message cannot be empty")

    def decrypt_last_message(self):
        if self.encrypted_msg:
            try:
                decrypted = decrypt_message(self.encrypted_msg, self.password)
                messagebox.showinfo("Decrypted Message", decrypted)
            except Exception as e:
                messagebox.showerror("Error", f"Decryption failed: {str(e)}")
        else:
            messagebox.showwarning("Warning", "No encrypted message")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = SecureVoiceApp(root)
    root.mainloop()
