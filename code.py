from datetime import datetime
import os
import time

tasks = []


def get_current_time():
    return datetime.now()

def get_task_status(task):
    now = get_current_time()

    if task["done"]:
        return "Done"
    elif task["time"] < now:
        return "Expired"
    else:
        return "Not Done"


def show_header():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n")
    print("===================================================")
    print("   CURRENT DATE & TIME:", get_current_time().strftime("%B %d %Y , %I:%M %p"))
    print("===================================================\n")


def parse_datetime(date, time_str):
    formats = [
        "%Y-%m-%d %H:%M",
        "%d/%m/%Y %H:%M",
        "%Y-%m-%d %I:%M %p",
        "%d/%m/%Y %I:%M %p"
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(f"{date} {time_str}", fmt)
        except ValueError:
            continue
    return None


def add_task():
    show_header()

    name = input("Enter task: ")
    date = input("Enter date (YYYY-MM-DD or DD/MM/YYYY): ")
    time_str = input("Enter time (HH:MM or HH:MM AM/PM): ")

    task_datetime = parse_datetime(date, time_str)

    if not task_datetime:
        print("Invalid date/time format!")
        input("Press Enter...")
        return

    now = get_current_time()
    if task_datetime < now:
        print("Date/Time has already been passed!")
        input("Press Enter...")
        return

    tasks.append({
        "task": name,
        "time": task_datetime,
        "done": False
    })

    print("Task added successfully!")
    input("Press Enter...")


def view_tasks():
    show_header()

    if not tasks:
        print("No tasks available.\n")
        input("Press Enter...")
        return

    print("TASK LIST:\n")
    for i, task in enumerate(tasks):
        status = get_task_status(task)
        time_str = task["time"].strftime("%Y-%m-%d %I:%M %p")
        print(f"{i+1}. {task['task']} | {time_str} | {status}")

    input("\nPress Enter...")


def mark_done():
    view_tasks()
    try:
        num = int(input("Enter task number to mark done: "))
        if 0 < num <= len(tasks):
            tasks[num-1]["done"] = True
            print("Task marked as done!")
        else:
            print("Invalid task number!")
    except ValueError:
        print("Invalid input!")
    input("Press Enter...")


def delete_task():
    view_tasks()
    try:
        num = int(input("Enter task number to delete: "))
        if 0 < num <= len(tasks):
            tasks.pop(num-1)
            print("Task deleted!")
        else:
            print("Invalid task number!")
    except ValueError:
        print("Invalid input!")
    input("Press Enter...")


try:
    while True:
        show_header()

        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Done")
        print("4. Delete Task")
        print("5. Exit")

        choice = input("\nChoose option: ")

        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            mark_done()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            print("Closing...")
            break
        else:
            print("Invalid choice!")
            time.sleep(1)

except KeyboardInterrupt:
    print("\nProgram closed safely.")
