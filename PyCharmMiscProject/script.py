from tkinter import *
import json

tasks = []

def add_task(event=None):
    task = entry.get()
    if task:
        tasks.append({"text": task, "done": False})
        entry.delete(0, END)
        update_list()

def complete_task():
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        tasks[index]["done"] = not tasks[index]["done"]
        update_list()

def delete_task():
    selected = listbox.curselection()
    if selected:
        tasks.pop(selected[0])
        update_list()

def update_list():
    listbox.delete(0, END)

    for task in tasks:
        text = task["text"]
        if task["done"]:
            text = "✔ " + text
        listbox.insert(END, text)

def save_tasks():
    with open("tasks.json", "w", encoding="utf-8") as f:
        json.dump(tasks, f)

def load_tasks():
    global tasks
    try:
        with open("tasks.json", "r", encoding="utf-8") as f:
            tasks = json.load(f)
    except:
        tasks = []
    update_list()

root = Tk()
root.title("To-Do List")

entry = Entry(root, width=30)
entry.pack()

entry.bind("<Return>", add_task)

Button(root, text="Добави", command=add_task).pack()

listbox = Listbox(root, width=40)
listbox.pack()

Button(root, text="Завършена", command=complete_task).pack()
Button(root, text="Изтрий", command=delete_task).pack()

load_tasks()

root.protocol("WM_DELETE_WINDOW", lambda: (save_tasks(), root.destroy()))

root.mainloop()