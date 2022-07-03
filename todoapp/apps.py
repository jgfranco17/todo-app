import logging as lg
import datetime as dt
from tabulate import tabulate
from sqlalchemy.orm import sessionmaker
from .models import create_database, Task


class TodoApp(object):
    def __init__(self, user: str):
        # Basic properties
        self._user = user.title()

        # Database storage setup
        self._db_location, self._engine = create_database()
        Session = sessionmaker()
        self._db = Session(bind=self._engine)
        loaded_data = self._db.query(Task).filter(Task.user == self._user)
        self._task_count = len([d.task for d in loaded_data])

        # Configure logging
        log_fmt = "[%(levelname)s] %(asctime)s %(message)s"
        lg.basicConfig(level=lg.DEBUG, format=log_fmt)

    def __repr__(self):
        return f'<TodoApp user={self._user})>'

    def update(func):
        def update_wrapper(self, *args, **kwargs):
            loaded_data = self._db.query(Task).filter(Task.user == self._user)
            self._task_count = len([d.task for d in loaded_data])
            return func(*args, **kwargs)
        return update_wrapper

    @update
    def __load(self):
        if self._task_count:
            try:
                info = []
                data = self._db.query(Task).filter(Task.user == self._user)
                tasks = [{
                    "id": d.id,
                    "date": d.date.strftime("%d %b %Y, %I:%M %p %Z"),
                    "task": d.task
                } for d in data]
                print(f'Compiled {len(info)} data points.')

                headers = ["TASK ID", "DATE ADDED", "TASK DETAILS"]
                for t in tasks:
                    row = [t['id'], t['date'], t['task']]
                    info.append(row)

                print(tabulate(info, headers=headers, tablefmt="orgtbl"))

            except Exception as e:
                print(f'Error during loading: {e}')

        else:
            print("No tasks available right now. Maybe you would like to add one?")

    def __add(self, task_details: str):
        new_task = Task(
            user=self._user,
            date=dt.datetime.now(),
            task=task_details,
            completed=False
        )
        self._db.add(new_task)
        self._db.commit()
        self._task_count += 1

    def __delete(self, task_id: int):
        try:
            self._db.query(Task).filter(Task.id == task_id).delete()

        except Exception as e:
            lg.error(f'Error during task deletion: {e}')

    def __get_nearest(self) -> str:
        nearest_task = self._db.query(Task).filter(Task.user == self._user).first()
        return nearest_task.task

    @staticmethod
    def __options():
        print("[1] Show all tasks")
        print("[2] Add new task")
        print("[3] Mark task as completed")
        print("[4] Show nearest due task")
        print("[5] Delete task")
        print("[6] Exit program\n")

    def run(self):
        print(f'WELCOME TO {self._user.upper()}\'S TASK LIST!')
        print("---------------------------")
        while True:
            self.__options()
            choice = int(input("Action: "))
            match choice:
                case 1:
                    self.__load()
                case 2:
                    task_input = input("Please input task details: ")
                    self.__add(task_input)
                case 3:
                    task_number = input("Input task ID, or C to cancel: ")
                    if task_number == 'C' or task_number == 'c':
                        pass
                    else:
                        self.__delete(int(task_number))
                        print(f'Marked task {task_number} as completed!')
                case 4:
                    print(f'Here is your next upcoming task: {self.__get_nearest()}')
                case 5:
                    task_number = input("Input task ID, or \'C\' to cancel: ")
                    if task_number == 'C' or task_number == 'c':
                        pass
                    else:
                        self.__delete(int(task_number))
                case 6:
                    print("Exiting...")
                    break
                case _:
                    print("Please choose a valid option only!")

        lg.info("Closed task app.")
