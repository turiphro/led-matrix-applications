import numpy


class Display:
    def __init__(self, width, height):
        """
        self.pixels[horizontal, vertical]
        """
        self.width = width
        self.height = height
        self.pixels = numpy.zeros((width, height, 3), dtype=numpy.uint8)

    # TODO do we need an abstraction from self.pixels to keep track
    # of what changed (for the UDP protocol)?

    def send_full_frame(self, frame: numpy.ndarray):
        raise NotImplementedError


