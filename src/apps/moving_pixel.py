# simple app for testing purposes, moves a pixel across the frame
import time

from frame_buffer import FrameBuffer
from inputs.input import Event


class MovingPixelApp:
    def __init__(self, frame: FrameBuffer):
        self.frame = frame
        self.running = True
        self.position = [0, 0]

    def handle_input(self, event: Event):
        raise NotImplementedError

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