# Task Tracker CLI

A simple command-line task tracker built with Python.

## Requirements

- Python 3.8 or newer
- No external libraries

## Commands

### Add a task

```powershell
python task_cli.py add "Buy groceries"
```

### List all tasks

```powershell
python task_cli.py list
```

### List tasks by status

```powershell
python task_cli.py list todo
python task_cli.py list in-progress
python task_cli.py list done
```

### Update a task

```powershell
python task_cli.py update 1 "Buy groceries and cook dinner"
```

### Mark a task as in progress

```powershell
python task_cli.py mark-in-progress 1
```

### Mark a task as done

```powershell
python task_cli.py mark-done 1
```

### Delete a task

```powershell
python task_cli.py delete 1
```

Tasks are stored in `tasks.json`. This file is created automatically and excluded from Git.