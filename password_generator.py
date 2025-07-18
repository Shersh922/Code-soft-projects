import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import random
import string
import os

password_file = "saved_passwords.txt"
master_file = "master.txt"
master_password = None

def load_master_password():
    global master_password
    if os.path.exists(master_file):
        with open(master_file, "r") as f:
            master_password = f.read().strip()

def generate_password():
    length = int(length_slider.get())
    chars = ""
    types = 0
    if var_upper.get():
        chars += string.ascii_uppercase
        types += 1
    if var_lower.get():
        chars += string.ascii_lowercase
        types += 1
    if var_digits.get():
        chars += string.digits
        types += 1
    if var_symbols.get():
        chars += string.punctuation
        types += 1
    if not chars:
        result.set("Please select at least one character set 🙏")
        strength_label.config(text="")
        return
    password = ''.join(random.choice(chars) for _ in range(length))
    result.set(password)
    evaluate_strength(length, types)

def evaluate_strength(length, types):
    if length < 8 or types == 1:
        strength_label.config(text="Strength: Weak 💔", fg="#ef4444")
    elif 8 <= length <= 12 and types >= 2:
        strength_label.config(text="Strength: Moderate 🤏", fg="#f59e0b")
    elif length > 12 and types >= 3:
        strength_label.config(text="Strength: Strong 💪", fg="#10b981")
    else:
        strength_label.config(text="Strength: Okay 😐", fg="#6366f1")

def copy_to_clipboard():
    if result.get():
        app.clipboard_clear()
        app.clipboard_append(result.get())
        result.set(result.get() + "  ✓ Copied")
        result_label.config(fg="#22c55e")

def reset_all():
    result.set("")
    strength_label.config(text="")
    result_label.config(fg="#111827")
    var_upper.set(True)
    var_lower.set(True)
    var_digits.set(True)
    var_symbols.set(True)
    length_slider.set(12)

def set_master():
    global master_password
    if os.path.exists(master_file):
        messagebox.showinfo("Locked", "Master password already set.")
        return
    pwd = simpledialog.askstring("Set Master Password", "Create a master password:", show="*")
    if pwd:
        with open(master_file, "w") as f:
            f.write(pwd)
        master_password = pwd
        messagebox.showinfo("Done", "Master password saved permanently.")

def change_master():
    global master_password
    load_master_password()
    if not master_password:
        messagebox.showwarning("Not Set", "Master password not set yet.")
        return
    old = simpledialog.askstring("Current Password", "Enter current master password:", show="*")
    if old != master_password:
        messagebox.showerror("Incorrect", "Old password is incorrect ❌")
        return
    new_pwd = simpledialog.askstring("New Password", "Enter new master password:", show="*")
    if new_pwd:
        with open(master_file, "w") as f:
            f.write(new_pwd)
        master_password = new_pwd
        messagebox.showinfo("Success", "Master password updated 🔐")

def save_password():
    if not result.get() or "Nothing" in result.get():
        messagebox.showwarning("Empty", "No password to save!")
        return
    raw_password = result.get().replace("✓ Copied", "").strip()
    label = simpledialog.askstring("Label", "Label this password as:")
    if label:
        with open(password_file, "a") as f:
            f.write(f"{label}: {raw_password}\n")
        messagebox.showinfo("Saved", "Password saved permanently ✅")

def view_passwords():
    load_master_password()
    if not master_password:
        messagebox.showwarning("Not Set", "Master password not set yet.")
        return
    entered = simpledialog.askstring("Master Password", "Enter master password to view saved:", show="*")
    if entered != master_password:
        messagebox.showerror("Incorrect", "Wrong password ❌")
        return
    if not os.path.exists(password_file):
        messagebox.showinfo("None", "No saved passwords yet.")
        return
    with open(password_file, "r") as f:
        data = f.read()
    win = tk.Toplevel(app)
    win.title("Saved Passwords")
    win.geometry("400x300")
    win.configure(bg="#f7f7f7")
    tk.Label(win, text="🔐 Saved Passwords", font=("Segoe UI", 14), bg="#f7f7f7").pack(pady=10)
    txt = tk.Text(win, font=("Consolas", 11), bg="#fff")
    txt.insert(tk.END, data)
    txt.config(state=tk.DISABLED)
    txt.pack(padx=10, pady=5)

app = tk.Tk()
app.title("🔐 Password Generator")
app.geometry("510x580")
app.configure(bg="#f7f7f7")

tk.Label(app, text="🔐 Password Generator", font=("Segoe UI", 20), bg="#f7f7f7", fg="#1e293b").pack(pady=(20, 10))

tk.Label(app, text="Choose Length:", font=("Segoe UI", 12), bg="#f7f7f7").pack()
length_slider = ttk.Scale(app, from_=4, to=32, orient="horizontal")
length_slider.set(12)
length_slider.pack(pady=5)

check_frame = tk.Frame(app, bg="#f7f7f7")
check_frame.pack(pady=10)
var_upper = tk.BooleanVar(value=True)
var_lower = tk.BooleanVar(value=True)
var_digits = tk.BooleanVar(value=True)
var_symbols = tk.BooleanVar(value=True)

ttk.Checkbutton(check_frame, text="A-Z", variable=var_upper).grid(row=0, column=0, padx=10)
ttk.Checkbutton(check_frame, text="a-z", variable=var_lower).grid(row=0, column=1, padx=10)
ttk.Checkbutton(check_frame, text="0-9", variable=var_digits).grid(row=1, column=0, padx=10)
ttk.Checkbutton(check_frame, text="@#$%", variable=var_symbols).grid(row=1, column=1, padx=10)

btn_frame = tk.Frame(app, bg="#f7f7f7")
btn_frame.pack(pady=10)
style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 11), padding=6)

ttk.Button(btn_frame, text="Generate", command=generate_password).grid(row=0, column=0, padx=8)
ttk.Button(btn_frame, text="Copy", command=copy_to_clipboard).grid(row=0, column=1, padx=8)
ttk.Button(btn_frame, text="Reset", command=reset_all).grid(row=0, column=2, padx=8)
ttk.Button(btn_frame, text="💾 Save", command=save_password).grid(row=1, column=0, padx=8, pady=5)
ttk.Button(btn_frame, text="👁 View", command=view_passwords).grid(row=1, column=1, padx=8)
ttk.Button(btn_frame, text="🔑 Set", command=set_master).grid(row=2, column=0, padx=8, pady=5)
ttk.Button(btn_frame, text="🔁 Change", command=change_master).grid(row=2, column=1, padx=8)

result = tk.StringVar()
result_label = tk.Label(app, textvariable=result, font=("Consolas", 14), bg="#f7f7f7", fg="#111827", wraplength=420)
result_label.pack(pady=(20, 5))
strength_label = tk.Label(app, text="", font=("Segoe UI", 11, "bold"), bg="#f7f7f7")
strength_label.pack()

tk.Label(app, text="🔐 Secure & Persistent | CodSoft Task 3", font=("Segoe UI", 9), bg="#f7f7f7", fg="#6b7280").pack(pady=10)

load_master_password()
app.mainloop()