import datetime
from colorama import Fore
from pyfiglet import figlet_format
from yaspin import yaspin
import time
import os


class Task:
    def __init__(self, name, due_date):
        self.name = name
        self.due_date = due_date
        self.completed = False

    def change_name(self, new_name):
        self.name = new_name

    def change_due_date(self, new_date):
        self.due_date = new_date

    def complete(self):
        self.completed = True


tasks = []

menu = {
    1: "Add new tasks",
    2: "View all tasks",
    3: "Mark task as complete",
    4: "Delete tasks",
    5: "Save tasks",
    6: "Load tasks",
    7: "Quit",
}


def clear():
    os.system("clear")


def add_task():
    name = input(Fore.CYAN + "Enter task name: ")
    due_date_str = input(Fore.CYAN + "Enter due date (YYYY-MM-DD): ")
    try:
        due_date = datetime.datetime.strptime(due_date_str, "%y-%m-%d").date()
    except ValueError:
        print(Fore.RED + "Invalid date format! Please use YYYY-MM-DD.")
        return

    new_task = Task(name, due_date)
    tasks.append(new_task)
    print(Fore.GREEN + "Task added.")


def view_tasks():
    if not tasks:
        print(Fore.RED + "No tasks available.")
        return
    print(Fore.CYAN + "All tasks:")
    for i, task in enumerate(tasks, start=1):
        status = (
            (Fore.GREEN + "Completed") if task.completed else (Fore.YELLOW + "Pending")
        )
        print(f"{i}. Name: {task.name}")
        print(f"   Due date: {task.due_date}")
        print(f"   Status: {status}{Fore.RESET}")
        print()


def complete_task():
    view_tasks()
    try:
        index = int(input(Fore.CYAN + "Enter the task number to mark as completed: "))
        if 1 <= index <= len(tasks):
            tasks[index - 1].complete()
            print(Fore.GREEN + "Task marked as completed.")
        else:
            print(Fore.RED + "Invalid task number.")
    except ValueError:
        print(Fore.RED + "Please enter a valid number.")


def delete_task():
    view_tasks()
    try:
        index = int(input(Fore.CYAN + "Enter the task number to delete: "))
        if 1 <= index <= len(tasks):
            removed = tasks.pop(index - 1)
            with yaspin(text="", color="red"):
                time.sleep(1.5)  # simulate loading
                print(Fore.RED + f'Task "{removed.name}" deleted.')
        else:
            print(Fore.RED + "Invalid task number.")
    except ValueError:
        print(Fore.RED + "Please enter a valid number.")


def save_tasks():
    with open("tasks.txt", "w") as file:
        for task in tasks:
            with yaspin(text="", color="green"):
                time.sleep(1.5)  # simulate loading
            line = f"{task.name}|{task.due_date}|{task.completed}\n"
            file.write(line)
    print(Fore.GREEN + "Tasks saved.")


def load_tasks():
    global tasks
    tasks.clear()
    try:
        with open("tasks.txt", "r") as file:
            with yaspin(text="", color="cyan"):
                time.sleep(1.5)  # simulate loading
            for line in file:
                name, due_date_str, completed_str = line.split("|")
                due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d").date()
                completed = completed_str == "True"
                task = Task(name, due_date)
                task.completed = completed
                tasks.append(task)
        print(Fore.GREEN + "Tasks loaded.")
    except FileNotFoundError:
        print(Fore.YELLOW + "No saved tasks found.")


def display_menu():
    while True:
        clear()
        print(Fore.CYAN + figlet_format("TODO LIST", font="slant"))
        print("\nTodo List menu:")
        for key, value in menu.items():
            print(f"{key} -- {value}")

        choice = input("Please enter your selection: ")

        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            complete_task()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            save_tasks()
        elif choice == "6":
            load_tasks()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print(Fore.RED + "Invalid choice, please try again.")

        input(Fore.CYAN + "Press Enter to return to the menu.")


# Start the program
if __name__ == "__main__":
    display_menu()
