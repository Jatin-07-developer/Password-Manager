from cryptography.fernet import Fernet
import os

def load_key():
    if not os.path.exists("key.key"):
        key = Fernet.generate_key()

        with open("key.key", "wb") as file:
            file.write(key)

        return key

    with open("key.key", "rb") as file:
        key = file.read()

    return key


key = load_key()
fer = Fernet(key)

import tkinter as tk
from tkinter import ttk, messagebox
from cryptography.fernet import Fernet
import os


# ---------------- KEY MANAGEMENT ----------------

def load_key():
    if not os.path.exists("key.key"):
        key = Fernet.generate_key()
        with open("key.key", "wb") as file:
            file.write(key)
        return key

    with open("key.key", "rb") as file:
        return file.read()


key = load_key()
fer = Fernet(key)


# ---------------- FUNCTIONS ----------------

def add_password():
    account = account_entry.get().strip()
    password = password_entry.get()

    if not account or not password:
        messagebox.showwarning(
            "Missing Information",
            "Please enter both account name and password."
        )
        return

    encrypted_password = fer.encrypt(password.encode()).decode()

    with open("password.txt", "a") as file:
        file.write(account + "|" + encrypted_password + "\n")

    messagebox.showinfo(
        "Success",
        "Password saved successfully!"
    )

    account_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)


def view_passwords():
    for item in tree.get_children():
        tree.delete(item)

    if not os.path.exists("password.txt"):
        messagebox.showinfo(
            "No Passwords",
            "No passwords have been saved yet."
        )
        return

    try:
        with open("password.txt", "r") as file:
            for line in file:
                line = line.rstrip()

                if not line:
                    continue

                try:
                    account, encrypted_password = line.split("|", 1)

                    password = fer.decrypt(
                        encrypted_password.encode()
                    ).decode()

                    tree.insert(
                        "",
                        tk.END,
                        values=(account, password)
                    )

                except Exception:
                    continue

    except FileNotFoundError:
        pass


def toggle_password():
    if password_entry.cget("show") == "*":
        password_entry.config(show="")
        show_button.config(text="Hide")
    else:
        password_entry.config(show="*")
        show_button.config(text="Show")


def clear_fields():
    account_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)


# ---------------- MAIN WINDOW ----------------

root = tk.Tk()
root.title("🔐 Secure Password Manager")
root.geometry("850x600")
root.resizable(False, False)
root.configure(bg="#121212")


# ---------------- STYLE ----------------

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background="#1e1e1e",
    foreground="white",
    fieldbackground="#1e1e1e",
    rowheight=35,
    font=("Segoe UI", 11)
)

style.configure(
    "Treeview.Heading",
    background="#292929",
    foreground="#00e5ff",
    font=("Segoe UI", 11, "bold")
)

style.map(
    "Treeview",
    background=[("selected", "#005f73")]
)


# ---------------- TITLE ----------------

title = tk.Label(
    root,
    text="🔐  SECURE PASSWORD MANAGER",
    font=("Segoe UI", 24, "bold"),
    bg="#121212",
    fg="#00e5ff"
)

title.pack(pady=(25, 5))


subtitle = tk.Label(
    root,
    text="Store your passwords securely with Fernet encryption",
    font=("Segoe UI", 11),
    bg="#121212",
    fg="#aaaaaa"
)

subtitle.pack(pady=(0, 20))


# ---------------- INPUT FRAME ----------------

input_frame = tk.Frame(
    root,
    bg="#1b1b1b",
    highlightbackground="#333333",
    highlightthickness=1
)

input_frame.pack(
    padx=40,
    pady=10,
    fill="x"
)


# Account

account_label = tk.Label(
    input_frame,
    text="Account",
    font=("Segoe UI", 11, "bold"),
    bg="#1b1b1b",
    fg="white"
)

account_label.grid(
    row=0,
    column=0,
    padx=20,
    pady=(20, 5),
    sticky="w"
)


account_entry = tk.Entry(
    input_frame,
    font=("Segoe UI", 12),
    bg="#292929",
    fg="white",
    insertbackground="white",
    relief="flat"
)

account_entry.grid(
    row=1,
    column=0,
    padx=20,
    pady=(0, 20),
    ipady=8,
    sticky="ew"
)


# Password

password_label = tk.Label(
    input_frame,
    text="Password",
    font=("Segoe UI", 11, "bold"),
    bg="#1b1b1b",
    fg="white"
)

password_label.grid(
    row=0,
    column=1,
    padx=20,
    pady=(20, 5),
    sticky="w"
)


password_entry = tk.Entry(
    input_frame,
    font=("Segoe UI", 12),
    bg="#292929",
    fg="white",
    insertbackground="white",
    relief="flat",
    show="*"
)

password_entry.grid(
    row=1,
    column=1,
    padx=(20, 5),
    pady=(0, 20),
    ipady=8,
    sticky="ew"
)


show_button = tk.Button(
    input_frame,
    text="Show",
    command=toggle_password,
    bg="#333333",
    fg="white",
    activebackground="#444444",
    activeforeground="white",
    relief="flat",
    cursor="hand2"
)

show_button.grid(
    row=1,
    column=2,
    padx=(0, 20),
    pady=(0, 20),
    ipadx=10,
    ipady=5
)


input_frame.columnconfigure(0, weight=1)
input_frame.columnconfigure(1, weight=1)


# ---------------- BUTTONS ----------------

button_frame = tk.Frame(
    root,
    bg="#121212"
)

button_frame.pack(pady=15)


add_button = tk.Button(
    button_frame,
    text="➕  Add Password",
    command=add_password,
    font=("Segoe UI", 11, "bold"),
    bg="#00a896",
    fg="white",
    activebackground="#008f7a",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    padx=20,
    pady=10
)

add_button.grid(row=0, column=0, padx=8)


view_button = tk.Button(
    button_frame,
    text="👁  View Passwords",
    command=view_passwords,
    font=("Segoe UI", 11, "bold"),
    bg="#0077b6",
    fg="white",
    activebackground="#005f8f",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    padx=20,
    pady=10
)

view_button.grid(row=0, column=1, padx=8)


clear_button = tk.Button(
    button_frame,
    text="✖  Clear",
    command=clear_fields,
    font=("Segoe UI", 11, "bold"),
    bg="#444444",
    fg="white",
    activebackground="#555555",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    padx=20,
    pady=10
)

clear_button.grid(row=0, column=2, padx=8)


# ---------------- PASSWORD TABLE ----------------

table_frame = tk.Frame(
    root,
    bg="#121212"
)

table_frame.pack(
    padx=40,
    pady=10,
    fill="both",
    expand=True
)


columns = ("Account", "Password")

tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

tree.heading(
    "Account",
    text="ACCOUNT"
)

tree.heading(
    "Password",
    text="PASSWORD"
)

tree.column(
    "Account",
    width=300,
    anchor="center"
)

tree.column(
    "Password",
    width=400,
    anchor="center"
)

tree.pack(
    fill="both",
    expand=True
)


# ---------------- FOOTER ----------------

footer = tk.Label(
    root,
    text="🔒 Your passwords are encrypted using Fernet",
    font=("Segoe UI", 9),
    bg="#121212",
    fg="#777777"
)

footer.pack(pady=10)


# ---------------- START APP ----------------

root.mainloop()