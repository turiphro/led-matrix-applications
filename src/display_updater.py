import asyncio
import time

from display import Display
from protocols.protocol import Protocol


class DisplayUpdater:
    def __init__(self, display: Display, protocol: Protocol, fps: int):
        self.running = True

        # NOTE: DisplayUpdater should only READ from display, never write
        self.display = display
        self.protocol = protocol
        self.fps = fps

    async def loop(self):
        while self.running:
            #print("Updating display...")
            start = time.perf_counter()

            pixels = self.display.pixels
            self.protocol.send_full_frame(pixels)

            waiting = max(0, 1.0 / self.fps - (time.perf_counter() - start))
            await asyncio.sleep(waiting)

    def stop(self):
        self.running = False