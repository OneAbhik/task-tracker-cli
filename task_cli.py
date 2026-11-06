import argparse
import json
from datetime import datetime
from pathlib import Path


TASKS_FILE = Path("tasks.json")

VALID_STATUSES = {
    "todo",
    "in-progress",
    "done",
}


def load_tasks():
    if not TASKS_FILE.exists():
        return []

    try:
        with TASKS_FILE.open("r", encoding="utf-8") as file:
            tasks = json.load(file)

        if not isinstance(tasks, list):
            print("Error: tasks.json must contain a list of tasks.")
            return []

        return tasks

    except json.JSONDecodeError:
        print("Error: tasks.json contains invalid JSON.")
        return []

    except OSError as error:
        print(f"Error: Could not read tasks.json: {error}")
        return []


def save_tasks(tasks):
    try:
        with TASKS_FILE.open("w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=2)
    except OSError as error:
        print(f"Error: Could not save tasks.json: {error}")

def get_current_time():
    return datetime.now().astimezone().isoformat(timespec="seconds")

def add_task(description):
    description = description.strip()
    if not description:
        print("Error: Task description cannot be empty.")
        return

    tasks = load_tasks()

    next_id = 1

    if tasks:
        next_id = max(task["id"] for task in tasks) + 1

    timestamp = get_current_time()

    task = {
        "id": next_id,
        "description": description,
        "status": "todo",
        "createdAt": timestamp,
        "updatedAt": timestamp,
    }

    tasks.append(task)
    save_tasks(tasks)

    print(f"Task added successfully (ID: {task['id']})")

def list_tasks(status=None):
    tasks = load_tasks()

    if status is not None:
        tasks = [
            task for task in tasks
            if task["status"] == status
        ]

    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        print(
            f"[{task['id']}] "
            f"{task['description']} "
            f"(status: {task['status']})"
        )

def update_task(task_id, description):
    description = description.strip()
    if not description:
        print("Error: Task description cannot be empty.")
        return

    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["description"] = description
            task["updatedAt"] = get_current_time()
            save_tasks(tasks)
            print(f"Task {task_id} updated successfully.")
            return

    print(f"Task with ID {task_id} not found.")

def delete_task(task_id):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            save_tasks(tasks)
            print(f"Task {task_id} deleted successfully.")
            return

    print(f"Task with ID {task_id} not found.")

def mark_in_progress(task_id):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "in-progress"
            task["updatedAt"] = get_current_time()
            save_tasks(tasks)
            print(f"Task {task_id} marked as in-progress.")
            return

    print(f"Task with ID {task_id} not found.")

def mark_done(task_id):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "done"
            task["updatedAt"] = get_current_time()
            save_tasks(tasks)
            print(f"Task {task_id} marked as done.")
            return

    print(f"Task with ID {task_id} not found.")

def main():
    parser = argparse.ArgumentParser(
        description="A simple command-line task tracker."
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    add_parser = subparsers.add_parser(
        "add",
        help="Add a new task",
    )

    add_parser.add_argument(
        "description",
        help="Description of the task",
    )

    update_parser = subparsers.add_parser(
        "update",
        help="Update a task description",
    )

    update_parser.add_argument(
        "id",
        type=int,
        help="ID of the task to update",
    )

    update_parser.add_argument(
        "description",
        help="New task description",
    )

    delete_parser = subparsers.add_parser(
        "delete",
        help="Delete a task",
    )

    delete_parser.add_argument(
        "id",
        type=int,
        help="ID of the task to delete",
    )

    mark_progress_parser = subparsers.   add_parser(
        "mark-in-progress",
        help="Mark a task as in progress",
    )

    mark_progress_parser.add_argument(
        "id",
        type=int,
        help="ID of the task",
    )

    mark_done_parser = subparsers.add_parser(
        "mark-done",
        help="Mark a task as done",
    )

    mark_done_parser.add_argument(
        "id",
        type=int,
        help="ID of the task",
    )

    list_parser = subparsers.add_parser(
        "list",
        help="List tasks",
    )

    list_parser.add_argument(
        "status",
        nargs="?",
        choices=["todo", "in-progress", "done"],
        help="Optional task status filter",
    )

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.description)
    elif args.command == "update":
        update_task(args.id, args.description)
    elif args.command == "delete":
        delete_task(args.id)
    elif args.command == "mark-in-progress":
        mark_in_progress(args.id)
    elif args.command == "mark-done":
        mark_done(args.id)
    elif args.command == "list":
        list_tasks(args.status) 

if __name__ == "__main__":
    main()