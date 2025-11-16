from textual import App, ComposeResult
from textual.widgets import Button

class tskg(App):
    def compose(self) -> ComposeResult:
        yield Button("Hello World!")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        pass


if __name__ == "__main__":
    app = tskg()
    app.run()
