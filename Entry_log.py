import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime

# Function to handle database connection and table creation
def init_db():
    conn = sqlite3.connect('entry_log.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            entry_time TEXT,
            exit_time TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function to handle login action
def login():
    username = entry_username.get()
    if username:
        entry_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = sqlite3.connect('entry_log.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO logs (username, entry_time, exit_time)
            VALUES (?, ?, ?)
        ''', (username, entry_time, None))
        conn.commit()
        conn.close()
        label_message.config(text=f"Welcome, {username}!", fg="green")
        entry_username.delete(0, tk.END)
        update_active_users()
    else:
        label_message.config(text="Please enter your name.", fg="red")

# Function to handle exit action
def exit_app():
    username = entry_username.get()
    if username:
        exit_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = sqlite3.connect('entry_log.db')
        c = conn.cursor()
        c.execute('''
            UPDATE logs
            SET exit_time = ?
            WHERE username = ? AND exit_time IS NULL
        ''', (exit_time, username))
        conn.commit()
        conn.close()
        label_message.config(text=f"Goodbye, {username}!", fg="green")
        entry_username.delete(0, tk.END)
        update_active_users()
    else:
        label_message.config(text="Please enter your name.", fg="red")

# Function to update the list of active users
def update_active_users():
    conn = sqlite3.connect('entry_log.db')
    c = conn.cursor()
    c.execute('''
        SELECT username, entry_time FROM logs
        WHERE exit_time IS NULL
    ''')
    users = c.fetchall()
    conn.close()

    for row in tree_active_users.get_children():
        tree_active_users.delete(row)

    for user in users:
        tree_active_users.insert('', tk.END, values=(user[0], user[1]))

# Function to view all entries in a new window
def view_all_entries():
    new_window = tk.Toplevel(window)
    new_window.title("All Entries")
    new_window.geometry("600x400")

    tree_all_entries = ttk.Treeview(new_window, columns=("Name", "Entry Time", "Exit Time"), show='headings')
    tree_all_entries.heading("Name", text="Entry Name")
    tree_all_entries.heading("Entry Time", text="Time of Entry")
    tree_all_entries.heading("Exit Time", text="Time of Exit")
    tree_all_entries.pack(pady=5, fill=tk.BOTH, expand=True)

    conn = sqlite3.connect('entry_log.db')
    c = conn.cursor()
    c.execute('SELECT username, entry_time, exit_time FROM logs')
    entries = c.fetchall()
    conn.close()

    for entry in entries:
        tree_all_entries.insert('', tk.END, values=(entry[0], entry[1], entry[2]))

# Initialize database
init_db()

# Create the main window
window = tk.Tk()
window.title("Entry Log Window")
window.geometry("700x500")

# Create and place the username label and entry field
label_username = tk.Label(window, text="Enter your name:")
label_username.pack(pady=10)

entry_username = tk.Entry(window, width=30)
entry_username.pack(pady=5)

# Create and place the login and exit buttons
frame_buttons = tk.Frame(window)
frame_buttons.pack(pady=10)

button_login = tk.Button(frame_buttons, text="Login", command=login)
button_login.pack(side=tk.LEFT, padx=5)

button_exit = tk.Button(frame_buttons, text="Exit", command=exit_app)
button_exit.pack(side=tk.LEFT, padx=5)

# Create a label to display messages
label_message = tk.Label(window, text="", fg="green")
label_message.pack(pady=5)

# Create and place the active users label and Treeview
label_active_users = tk.Label(window, text="Active Users:")
label_active_users.pack(pady=10)

tree_active_users = ttk.Treeview(window, columns=("Name", "Entry Time"), show='headings')
tree_active_users.heading("Name", text="Entry Name")
tree_active_users.heading("Entry Time", text="Time of Entry")
tree_active_users.pack(pady=5, fill=tk.BOTH, expand=True)

# Create a button to view all entries
button_view_all = tk.Button(window, text="View All Entries", command=view_all_entries)
button_view_all.pack(pady=10)

# Run the initial update for active users
update_active_users()

# Run the application
window.mainloop()

