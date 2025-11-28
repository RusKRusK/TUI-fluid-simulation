from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Header, Footer, Static, Label
from simulation import FluidSimulation

class SimulationDisplay(Static):
    pass

class FluidApp(App):
    CSS = """
    Screen {
        layout: horizontal;
    }

    #sidebar {
        width: 30;
        background: $panel;
        dock: left;
        height: 100%;
        padding: 1;
    }

    #display-container {
        width: 100%;
        height: 100%;
        align: center middle;
        border: solid green;
    }

    SimulationDisplay {
        width: auto;
        height: auto;
        border: solid white;
    }

    Button {
        width: 100%;
        margin-bottom: 1;
    }
    """

    BINDINGS = [("q", "quit", "Quit")]

    def __init__(self):
        super().__init__()
        self.simulation = FluidSimulation()
        self.timer = None
        self.sim_running = False

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="sidebar"):
            yield Label("Controls")
            yield Button("ファイルをロード", id="load_btn", variant="primary")
            yield Button("リセット", id="reset_btn", variant="warning")
        
        with Container(id="display-container"):
            yield SimulationDisplay(id="sim_display")
        
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "load_btn":
            self.load_simulation()
        elif event.button.id == "reset_btn":
            self.reset_simulation()

    def load_simulation(self):
        if self.simulation.load_from_file("level.txt"):
            self.query_one("#sim_display").update(self.simulation.get_render_text())
            self.start_simulation()
            self.notify("Loaded level.txt")
        else:
            self.notify("Failed to load level.txt", severity="error")

    def reset_simulation(self):
        self.simulation.reset()
        self.query_one("#sim_display").update(self.simulation.get_render_text())
        self.start_simulation()
        self.notify("Simulation Reset")

    def start_simulation(self):
        if not self.sim_running:
            self.sim_running = True
            self.timer = self.set_interval(0.1, self.update_simulation)

    def update_simulation(self):
        self.simulation.update()
        self.query_one("#sim_display").update(self.simulation.get_render_text())

if __name__ == "__main__":
    app = FluidApp()
    app.run()
