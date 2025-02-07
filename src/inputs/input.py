from dataclasses import dataclass
import enum


DEVICE_ID_COLOURS = {
    # known device IDs with their respective colours
    "E4:17:D8:2C:2D:EA": (44, 111, 187),  # 8bitdo micro - matt blue
    "E4:17:D8:35:8A:3A": (57, 173, 72),  # 8bitdo micro - matt green
}


class Button(enum.Enum):
    BUTTON_UP = enum.auto()
    BUTTON_RIGHT = enum.auto()
    BUTTON_DOWN = enum.auto()
    BUTTON_LEFT = enum.auto()
    JOY_UP = enum.auto()
    JOY_RIGHT = enum.auto()
    JOY_DOWN = enum.auto()
    JOY_LEFT = enum.auto()
    START = enum.auto()
    SELECT = enum.auto()
    TRIGGER_RIGHT = enum.auto()
    TRIGGER_RIGHT2 = enum.auto()
    TRIGGER_LEFT = enum.auto()
    TRIGGER_LEFT2 = enum.auto()
    NONE = enum.auto()


class State(enum.Enum):
    RELEASED = 0
    PRESSED = 1


@dataclass
class Event:
    device_id: str
    button: Button
    state: State


class Input:
    def __init__(self):
        self.running = True

    def handle_events(self):
        raise NotImplementedError

