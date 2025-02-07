import asyncio
from protocols.wled_udp import UDPRealtimeProtocol
from frame_buffer import FrameBuffer
from display_updater import DisplayUpdater
from apps.moving_pixel import MovingPixelApp


WIDTH = 18
HEIGHT = 60
FPS = 20
IP = "192.168.1.186"
PORT_UDP = 21324
PORT_TX = 0
PORT_RX = 1


async def main():
    """
    Main entry point for the application.
    """

    """
    ----thread-           ---------------------------thread-
    | app ----|--> frame -|-> display_updater -> protocol -|-> [screen]
    -----------           ----------------------------------
    """

    frame = FrameBuffer(width=WIDTH, height=HEIGHT)

    protocol = UDPRealtimeProtocol(IP, PORT_UDP)
    display_updater = DisplayUpdater(frame, protocol, FPS)

    app = MovingPixelApp(frame)

    display_task = asyncio.create_task(display_updater.loop())
    loop = asyncio.get_running_loop()
    app_task = loop.run_in_executor(None, app.run)

    await app_task
    display_updater.stop()
    await display_task


if __name__ == '__main__':
    asyncio.run(main())