from ..display import Display
from ..inputs import Event


class App:
    def __init__(self, display: Display):
        self.display = display

    def handle_input(self, event: Event):
        raise NotImplementedError
