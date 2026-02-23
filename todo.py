#!/usr/bin/env python

import os
import argparse, argcomplete
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
    print("Your tasks are\n\n <id> | <completed> | <name> ")
    for i, task in enumerate(tasks, 1):
        status = " " if tasks[task] else "✗"
        print(f"    {i} | {status.center(11," ")} | {task} ")


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
    os.makedirs(os.path.expanduser("~/.config/todo/"), exist_ok=True)

    parser = argparse.ArgumentParser(
        prog="todo",
        description="A File based quick CLI Tool",
        epilog="Thanks for using :)",
    )

    # Create subparsers for commands
    subparsers = parser.add_subparsers(dest="command")

    # add command
    add_parser = subparsers.add_parser("add", help="Create a new task")
    add_parser.add_argument("task", help="Task name")

    # ls command
    subparsers.add_parser("ls", help="List all tasks")

    # del command
    del_parser = subparsers.add_parser("del", help="Delete a task")
    del_parser.add_argument("id", help="Task ID")

    # stat command
    stat_parser = subparsers.add_parser("stat", help="Toggle task status")
    stat_parser.add_argument("id", help="Task ID")

    # mod command
    mod_parser = subparsers.add_parser("mod", help="Rename a task")
    mod_parser.add_argument("id", help="Task ID")
    mod_parser.add_argument("name", help="New task name")

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    # Handle commands
    if args.command == "add":
        add(args.task)
        view()

    elif args.command == "ls":
        view()

    elif args.command == "del":
        delete(args.id)
        print("Deleted successfully!")
        view()

    elif args.command == "stat":
        status(args.id)
        view()

    elif args.command == "mod":
        modify(args.id, args.name)
        view()

    else:
        parser.print_help()
