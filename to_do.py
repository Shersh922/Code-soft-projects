import tkinter as tk
from tkinter import ttk
import json
import os

# File Setup
TODO_FILE = 'todo_data.json'

# Load Tasks Safely
def load_tasks():
    if os.path.exists(TODO_FILE):
        try:
            with open(TODO_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []  # Return empty list if JSON is corrupted
    return []

# Save Tasks
def save_tasks(tasks):
    with open(TODO_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

# Refresh Task List
def update_task_list():
    task_listbox.delete(0, tk.END)
    for task in tasks:
        status = "✅ " if task['done'] else "⬜ "
        task_listbox.insert(tk.END, status + task['task'])

# Add Task
def add_task(event=None):
    task = task_entry.get().strip()
    if task:
        tasks.append({'task': task, 'done': False})
        save_tasks(tasks)
        update_task_list()
        task_entry.delete(0, tk.END)

# Delete Task
def delete_task():
    selected = task_listbox.curselection()
    if selected:
        del tasks[selected[0]]
        save_tasks(tasks)
        update_task_list()

# Toggle Task Status
def toggle_task():
    selected = task_listbox.curselection()
    if selected:
        index = selected[0]
        tasks[index]['done'] = not tasks[index]['done']
        save_tasks(tasks)
        update_task_list()

# GUI Setup
app = tk.Tk()
app.title("📝 Shersh's Task List")
app.geometry("500x640")
app.configure(bg="#f2f4f8")

# Header
title_label = tk.Label(app, text="✨ Stay Organized, Stay Ahead!", font=("Helvetica Neue", 20, "bold"), bg="#f2f4f8", fg="#1f2937")
title_label.pack(pady=(25, 10))

# Frame
frame = tk.Frame(app, bg="#ffffff", bd=2, relief=tk.GROOVE)
frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=False)

# Entry Field
task_entry = ttk.Entry(frame, font=("Segoe UI", 13))
task_entry.pack(padx=12, pady=15, fill=tk.X)
task_entry.bind("<Return>", add_task)  # Enter key adds task

# Buttons Frame
btn_frame = tk.Frame(frame, bg="#ffffff")
btn_frame.pack(padx=12, pady=8, fill=tk.X)

# Buttons Style
style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 11), padding=6)

add_btn = ttk.Button(btn_frame, text="➕ Add Task", command=add_task)
add_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=4)

done_btn = ttk.Button(btn_frame, text="✅ Mark Done", command=toggle_task)
done_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=4)

del_btn = ttk.Button(btn_frame, text="🗑 Delete", command=delete_task)
del_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=4)

# Task Listbox
task_listbox = tk.Listbox(app, font=("Segoe UI", 14), selectbackground="#dbeafe", activestyle='none',
                          bg="#ffffff", fg="#111827", bd=1, highlightthickness=0, relief=tk.FLAT)
task_listbox.pack(padx=20, pady=15, fill=tk.BOTH, expand=True)

# Footer
footer = tk.Label(app, text="📅 Build one good habit daily — Prakhar", font=("Segoe UI", 10), bg="#f2f4f8", fg="#6b7280")
footer.pack(pady=8)

# Load and Display Tasks
tasks = load_tasks()
update_task_list()

# Run App
app.mainloop()
