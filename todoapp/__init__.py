from .apps import TodoApp


def create_list(name: str):
    app = TodoApp(user=name)
    app.run()
