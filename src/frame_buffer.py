import numpy


class FrameBuffer:
    """
    FrameBuffer class tracks the current local state of the display.

    The display is represented as a 2D array of pixels, where each pixel is a 3-element array of RGB values.

    `self.pixels[horizontal, vertical] = [r, g, b]`

    Applications can access and modify the pixels directly.

    Consumers (DisplayUpdater) should either call get_all_pixels() to get all pixels, or get_diff_pixels()
    to get only the pixels that have changed since the last call to either method.
    """
    def __init__(self, width, height):
        """
        """
        self.pixels = numpy.zeros((width, height, 3), dtype=numpy.uint8)
        self._last_pixels = self.pixels.copy()
        self.width = width
        self.height = height

    def get_all_pixels(self) -> numpy.ndarray:
        self._last_pixels = self.pixels.copy()
        return self.pixels

    def get_diff_pixels(self) -> numpy.ndarray:
        diff = self.pixels != self._last_pixels
        self._last_pixels = self.pixels.copy()
        return self.pixels[diff]

