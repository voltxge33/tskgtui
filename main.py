import json
from pathlib import Path
from textual import on, __version__
from textual.app import App, ComposeResult
from textual.widgets import Button, Input, Label, ListView, ListItem
from textual.containers import Horizontal, Vertical
DATA_DIR = Path.home() / "tskg"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DATA_FILE = DATA_DIR / "tasks.json"
print(__version__)

completed = " | Completed!"
incomplete = " | Not Completed"
def load_tasks():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []
def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)
def appendlist(app) -> None:
    tasks = load_tasks()
    list_view = app.query_one(ListView)
    list_view.clear()  # remove all existing items
    for t in tasks:
        list_view.append(ListItem(Label(t["name"])))
class tskg(App):
    CSS = """
    Vertical {
        align: center top;
    }
    Horizontal {
        align: left bottom;
    }
    """
    def compose(self) -> ComposeResult:
        yield Vertical(
            Horizontal(    
                Button("Add", id="add"),
                Button("Remove", id="remove"),
                id="Buttons"
                ),
            Input(placeholder="Enter Task Name", id="taskinput"),
            Label("Tasks"),
            ListView(
            ),
        )
    async def on_mount(self) -> None:
        appendlist(self)
    @on(Button.Pressed, "#add")
    def pressed_add(self) -> None:
        self.query_one("#add", Button).disabled = True
        task_name = self.query_one("#taskinput").value
        tasks = load_tasks()
        new_task = {
            "name": task_name
        }
        if any(t["name"].lower() == task_name.lower() for t in tasks):
            return
        tasks.append(new_task)
        save_tasks(tasks)
        appendlist(self)
        self.query_one('#add', Button).disabled = False
    @on(Button.Pressed, "#remove")


    def pressed_remove(self) -> None:
        tasks = load_tasks()
        task = self.query_one(ListView).index
        try:
            for t in tasks:
                if t["name"] == tasks[task]["name"]:
                    tasks.remove(t)
        except:
            return
        save_tasks(tasks)
        appendlist(self)
if __name__ == "__main__":
    app = tskg()
    app.run()