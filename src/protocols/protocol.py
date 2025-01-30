import numpy


class Protocol:
    def send_full_frame(self, pixels: numpy.ndarray):
        raise NotImplementedError