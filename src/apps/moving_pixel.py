# simple app for testing purposes, moves a pixel across the display
import time

from display import Display
from inputs.input import Event


class MovingPixelApp:
    def __init__(self, display: Display):
        self.display = display
        self.running = True
        self.position = [0, 0]

    def handle_input(self, event: Event):
        raise NotImplementedError

    def run(self):
        """Simulates a moving pixel until it decides to exit."""
        while self.running:
            # TODO change to abstraction methods instead of accessing display.pixels directly
            self.display.pixels.fill(0)
            self.display.pixels[self.position[0], self.position[1]] = [255, 255, 255]

            self.position[0] += 1
            if self.position[0] == self.display.width:
                self.position[0] = 0
                self.position[1] = (self.position[1] + 1) % self.display.height
            print(f"Pixel moved to position {self.position}")

            time.sleep(0.1)

            # to end:
            #self.running = False