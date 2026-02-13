#!/usr/bin/env python

import os
import sys
import json

FILE = os.path.expanduser(os.path.join("~", ".config", "todo", "todo.json"))


def load():
    if not os.path.exists(FILE):
        return {}

    with open(FILE, "r") as f:
        return json.load(f)


def save(tasks):
    with open(FILE, "w") as f:
        json.dump(tasks, f)


def add(content):
    tasks = load()
    tasks[content] = False
    save(tasks)


def view():
    tasks = load()
    print("Your tasks are\n <id> | <completed> | <name> ")
    for i, task in enumerate(tasks, 1):
        status = " " if tasks[task] else "✗"
        print(f" {i} | {status} | {task} ")


def delete(id):
    tasks = load()
    tasks.pop(list(tasks)[int(id) - 1])
    save(tasks)


def status(id):
    tasks = load()
    key = list(tasks)[int(id) - 1]
    tasks[key] = not tasks[key]
    save(tasks)


def modify(id, task):
    tasks = load()
    delete(id)
    add(task)
    if tasks[list(tasks)[int(id) - 1]]:
        status(id)


if __name__ == "__main__":
    os.makedirs(os.path.expanduser("~/.config/todo/"),exist_ok=True)
    cmd = sys.argv[1:]
    print("\n")

    if "add" in cmd:
        add(cmd[1])
        view()

    elif "ls" in cmd:
        view()

    elif "del" in cmd:
        delete(cmd[1])
        print("Deleted successfully !")
        view()

    elif "stat" in cmd:
        status(cmd[1])
        view()

    elif "mod" in cmd:
        modify(*cmd[1:])
        view()

    else:
        print(""" Todo <cmd> <option> 

                         cmd 
        --------------------------------------------
        ls - Lists all tasks.
        add <task name> - Create a <task name> task.
        del <id> - Delete task with <id>
        mod <id> <name> - Renames a task
        stat <id> - toggle a task status
        help - Prints this message""")
