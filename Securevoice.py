# SecureVoice - Modular Version Using 'cryptography' Library (Working)

import tkinter as tk
from tkinter import messagebox
from encryption_utils import encrypt_message, decrypt_message
from tts_utils import speak

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
