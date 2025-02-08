import asyncio
import evdev

from inputs.input import Button, Input, Event, State


MAPPING_BUTTONS = {
    ("BTN_NORTH", "BTN_X"): Button.BUTTON_UP,
    ("BTN_B", "BTN_EAST"): Button.BUTTON_RIGHT,
    ("BTN_A", "BTN_GAMEPAD", "BTN_SOUTH"): Button.BUTTON_DOWN,
    ("BTN_WEST", "BTN_Y"): Button.BUTTON_LEFT,
    "BTN_START": Button.START,
    "BTN_SELECT": Button.SELECT,
    "BTN_TR": Button.TRIGGER_RIGHT,
    "BTN_TR2": Button.TRIGGER_RIGHT2,
    "BTN_TL": Button.TRIGGER_LEFT,
    "BTN_TL2": Button.TRIGGER_LEFT2,
}
MAPPING_JOYSTICKS = {
    ("ABS_X", True): Button.JOY_RIGHT,
    ("ABS_X", False): Button.JOY_LEFT,
    ("ABS_Y", True): Button.JOY_DOWN,
    ("ABS_Y", False): Button.JOY_UP,
}


def map_joystick(axis):
    return Button.NONE


class BTController(Input):
    def __init__(self, event_handler):
        self.running = True
        self.event_handler = event_handler
        self.controllers = {}
        self.tasks = {}

    def find_controllers(self):
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        controllers = {device.uniq: device for device in devices if "Pro Controller" in device.name}
        return controllers

    async def handle_events(self, controller: evdev.InputDevice):
        async for bt_event in controller.async_read_loop():
            if not self.running:
                break  # abort loop

            # Key press/release events
            if bt_event.type == evdev.ecodes.EV_KEY:
                key_event = evdev.categorize(bt_event)
                button = MAPPING_BUTTONS.get(key_event.keycode, Button.NONE)
                event = Event(controller.uniq, button, State(bt_event.value))
                self.event_handler(event)

            # Analog input (joystick or trigger) -> convert to binary button presses
            elif bt_event.type == evdev.ecodes.EV_ABS:
                axis = evdev.ecodes.ABS[bt_event.code] if bt_event.code in evdev.ecodes.ABS else bt_event.code
                state = State(0 if abs(bt_event.value) < 1000 else 1)
                if state == State.PRESSED:
                    button = MAPPING_JOYSTICKS.get((axis, bt_event.value > 0), Button.NONE)
                    self.event_handler(Event(controller.uniq, button, state))
                else:
                    # for 'neutral' positions, we don't know the button (no memory),
                    # so we send a RELEASED event for all directions
                    for button in [Button.JOY_UP, Button.JOY_RIGHT, Button.JOY_DOWN, Button.JOY_LEFT]:
                        self.event_handler(Event(controller.uniq, button, state))

    async def loop(self):
        while self.running:
            controllers = self.find_controllers()

            # add new controllers
            for controller_id, controller in controllers.items():
                if controller_id not in self.controllers:
                    print(f"New controller found: {controller.uniq}")
                    self.controllers[controller_id] = controller
                    task = asyncio.create_task(self.handle_events(controller))
                    self.tasks[controller_id] = task

            # remove disconnected controllers
            disconnected_ids = set(self.controllers.keys()) - set(controllers.keys())
            for controller_id in disconnected_ids:
                print(f"Controller disconnected: {controller_id}")
                del self.controllers[controller_id]
                self.tasks[controller_id].cancel()
                del self.tasks[controller_id]

            await asyncio.sleep(5)

    def stop(self):
        self.running = False
        for task in self.tasks:
            task.cancel()