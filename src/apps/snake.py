# Multi-user Snake game
import time
from frame_buffer import FrameBuffer
from inputs.input import Button, Event, State


class SnakeApp:
    def __init__(self, frame: FrameBuffer, fps: int):
        self.running = True

        self.frame = frame
        self.fps = fps
        self.position = [0, 0]

    def handle_input(self, event: Event):
        print(f"{self.__class__.__name__} received event: {event}")
        if event.state == State.PRESSED:
            if event.button == Button.BUTTON_UP:
                self.position[1] = (self.position[1] - 1) % self.frame.height
            elif event.button == Button.BUTTON_DOWN:
                self.position[1] = (self.position[1] + 1) % self.frame.height
            elif event.button == Button.BUTTON_RIGHT:
                self.position[0] = (self.position[0] + 1) % self.frame.width
            elif event.button == Button.BUTTON_LEFT:
                self.position[0] = (self.position[0] - 1) % self.frame.width
            print(f"Pixel moved to position {self.position}")

    def run(self):
        """Simulates a moving pixel until it decides to exit."""
        while self.running:
            start = time.perf_counter()

            self.frame.pixels.fill(0)
            self.frame.pixels[self.position[0], self.position[1]] = [255, 255, 255]

            waiting = max(0, 1.0 / self.fps - (time.perf_counter() - start))
            time.sleep(waiting)