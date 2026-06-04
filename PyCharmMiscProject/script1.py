import json
import os
import tkinter as tk
from tkinter import messagebox

FILE_NAME = "tasks.json"

tasks = []
current_filter = "Всички"




def load_tasks():
    global tasks
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            tasks = json.load(f)


def save_tasks():
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)


def add_task(event=None):
    task_text = task_entry.get().strip()
    if task_text != "":
        tasks.append({"text": task_text, "completed": False})
        task_entry.delete(0, tk.END)
        refresh_list()
    else:
        messagebox.showwarning("Внимание", "Моля, въведете текст.")


def toggle_task(index):
    tasks[index]["completed"] = not tasks[index]["completed"]
    refresh_list()


def delete_task(index):
    del tasks[index]
    refresh_list()


def set_filter(new_filter):
    global current_filter
    current_filter = new_filter
    refresh_list()


def refresh_list():
    for widget in list_frame.winfo_children():
        widget.destroy()

    for index, task in enumerate(tasks):
        if current_filter == "Активни" and task["completed"]:
            continue
        if current_filter == "Завършени" and not task["completed"]:
            continue

        row = tk.Frame(list_frame)
        row.pack(fill="x", pady=2)

        sign = "✅" if task["completed"] else "⬜"
        check_btn = tk.Button(
            row, text=sign, command=lambda idx=index: toggle_task(idx)
        )
        check_btn.pack(side="left")

        if task["completed"]:
            lbl = tk.Label(
                row, text=task["text"], font=("Arial", 11, "overstrike")
            )
        else:
            lbl = tk.Label(row, text=task["text"], font=("Arial", 11))
        lbl.pack(side="left", padx=5)

        del_btn = tk.Button(
            row, text="❌", fg="red", command=lambda idx=index: delete_task(idx)
        )
        del_btn.pack(side="right")


def on_closing():
    save_tasks()
    root.destroy()



root = tk.Tk()
root.title("Мениджър на задачи")
root.geometry("400x450")

load_tasks()

entry_frame = tk.Frame(root)
entry_frame.pack(pady=10)

task_entry = tk.Entry(entry_frame, width=25, font=("Arial", 12))
task_entry.pack(side="left", padx=5)
task_entry.bind("<Return>", add_task)

add_button = tk.Button(entry_frame, text="Добави", command=add_task)
add_button.pack(side="left")

filter_frame = tk.Frame(root)
filter_frame.pack(pady=5)

tk.Button(
    filter_frame, text="Всички", command=lambda: set_filter("Всички")
).pack(side="left", padx=2)
tk.Button(
    filter_frame, text="Активни", command=lambda: set_filter("Активни")
).pack(side="left", padx=2)
tk.Button(
    filter_frame, text="Завършени", command=lambda: set_filter("Завършени")
).pack(side="left", padx=2)

list_frame = tk.Frame(root)
list_frame.pack(fill="both", expand=True, padx=20, pady=10)

refresh_list()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()