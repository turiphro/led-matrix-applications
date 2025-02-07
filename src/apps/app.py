from ..frame_buffer import FrameBuffer
from ..inputs import Event


class App:
    def __init__(self, frame: FrameBuffer):
        self.frame = frame

    def handle_input(self, event: Event):
        raise NotImplementedError
