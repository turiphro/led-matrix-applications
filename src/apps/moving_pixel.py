# simple app for testing purposes, moves a pixel across the frame
import time

from frame_buffer import FrameBuffer
from inputs.input import Event


class MovingPixelApp:
    def __init__(self, frame: FrameBuffer, fps: int):
        self.running = True

        self.frame = frame
        self.fps = fps
        self.position = [0, 0]

    def handle_input(self, event: Event):
        print(f"{self.__class__.__name__} received event: {event}")

    def run(self):
        """Simulates a moving pixel until it decides to exit."""
        while self.running:
            self.frame.pixels.fill(0)
            self.frame.pixels[self.position[0], self.position[1]] = [255, 255, 255]

            self.position[0] += 1
            if self.position[0] == self.frame.width:
                self.position[0] = 0
                self.position[1] = (self.position[1] + 1) % self.frame.height
            print(f"Pixel moved to position {self.position}")

            time.sleep(0.1)

            # to end:
            #self.running = False