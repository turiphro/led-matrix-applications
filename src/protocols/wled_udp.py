import socket
import numpy

from .protocol import Protocol


class UDPRealtimeProtocol(Protocol):
    PACKET_SIZE = 450

    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_full_frame(self, pixels: numpy.ndarray):
        """Send over UDP, using either DNRGB (all pixels) or WARLS (changed only)"""
        #print("Sending full frame inside UDPRealtimeProtocol...")
        colours = pixels.transpose(1, 0, 2).reshape(-1, 3).tolist()
        #print("Colours:", colours)
        offsets = range(0, len(colours), self.PACKET_SIZE)
        for offset in offsets:
            m = [
                4,   # protocol (1=WARLS, 2=DRGB, 3=DRGBW, 4=DNRGB), need DNRGB beyond 490 pixels
                255, # seconds to wait after last packet before returning to normal mode, 255=forever
            ]
            m += [ # starting LED index (only for DNRGB)
                (offset >> 8) & 0xFF,  # high byte
                offset & 0xFF,
            ]
            for r, g, b in colours[offset:offset+self.PACKET_SIZE]:
                m += [r, g, b]
            self.sock.sendto(bytes(m), (self.ip, self.port))
            #print("sent UDP packet for offset", offset, "with content", m)