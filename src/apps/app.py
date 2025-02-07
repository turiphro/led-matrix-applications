from ..frame_buffer import FrameBuffer
from ..inputs import Event


class App:
    def __init__(self, frame: FrameBuffer, fps: int):
        self.frame = frame
        self.fps = fps

    def handle_input(self, event: Event):
        raise NotImplementedError
