import asyncio

from apps.moving_pixel import MovingPixelApp
from apps.snake import SnakeApp
from display_updater import DisplayUpdater
from frame_buffer import FrameBuffer
from inputs.btcontroller import BTController
from protocols.wled_udp import UDPRealtimeProtocol


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
    -----thread-           ---------------------------thread-
    | app -----|--> frame -|-> display_updater -> protocol -|-> [screen]
    |  ^       |           |                                |
    ---|--------           ----------------------------------
       |
    ---|-thread-
    | input    |
    ------------
    """

    frame = FrameBuffer(width=WIDTH, height=HEIGHT)

    protocol = UDPRealtimeProtocol(IP, PORT_UDP)
    display_updater = DisplayUpdater(frame, protocol, FPS)

    app = SnakeApp(frame, FPS)
    input_device = BTController(app.handle_input)

    display_task = asyncio.create_task(display_updater.loop())
    input_task = asyncio.create_task(input_device.loop())
    loop = asyncio.get_running_loop()
    app_task = loop.run_in_executor(None, app.run)

    await app_task
    display_updater.stop()
    input_device.stop()
    await display_task
    await input_task


if __name__ == '__main__':
    asyncio.run(main())