# Multi-user Snake game
from dataclasses import dataclass
import enum
import random
import time
from frame_buffer import FrameBuffer
from inputs.input import DEVICE_ID_COLOURS, Button, Event, State


FRAMES_PER_STEP = 5


class Direction(enum.Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


@dataclass
class Snake:
    head: tuple[int, int]
    tail: list[tuple[int, int]]
    direction: Direction


class SnakeApp:
    def __init__(self, frame: FrameBuffer, fps: int):
        self.running = True

        self.frame = frame
        self.fps = fps
        self.snakes = {}
        self.food = self.random_position()

    def handle_input(self, event: Event):
        print(f"{self.__class__.__name__} received event: {event}")

        if event.device_id not in self.snakes:
            self.snakes[event.device_id] = Snake(
                self.random_position(), [], Direction.RIGHT
            )

        if event.state == State.PRESSED:
            snake = self.snakes[event.device_id]
            if event.button == Button.BUTTON_UP:
                snake.direction = Direction.UP
            elif event.button == Button.BUTTON_DOWN:
                snake.direction = Direction.DOWN
            elif event.button == Button.BUTTON_RIGHT:
                snake.direction = Direction.RIGHT
            elif event.button == Button.BUTTON_LEFT:
                snake.direction = Direction.LEFT

    def run(self):
        """Simulates a moving pixel until it decides to exit."""
        step = 0
        while self.running:
            start = time.perf_counter()

            if step == 0:
                # take a step
                for snake in self.snakes.values():
                    if snake.direction == Direction.UP:
                        new_head = (snake.head[0], (snake.head[1] - 1) % self.frame.height)
                    elif snake.direction == Direction.RIGHT:
                        new_head = ((snake.head[0] + 1) % self.frame.width, snake.head[1])
                    elif snake.direction == Direction.DOWN:
                        new_head = (snake.head[0], (snake.head[1] + 1) % self.frame.height)
                    elif snake.direction == Direction.LEFT:
                        new_head = ((snake.head[0] - 1) % self.frame.width, snake.head[1])

                    if new_head == self.food:
                        self.food = self.random_position()
                        snake.tail = [snake.head] + snake.tail
                    else:  # not eating
                        snake.tail = [snake.head] + snake.tail[:-1]
                    snake.head = new_head
                    # TODO if eating food, don't remove last pixel

                # check for collisions (self and others)
                # TODO

                # draw
                self.frame.pixels.fill(0)
                self.frame.pixels[*self.food] = [200, 10, 10]
                for device_id, snake in self.snakes.items():
                    colour = DEVICE_ID_COLOURS.get(device_id, (200, 200, 200))
                    for x, y in snake.tail:
                        self.frame.pixels[x, y] = colour

            step = (step + 1) % FRAMES_PER_STEP
            waiting = max(0, 1.0 / self.fps - (time.perf_counter() - start))
            time.sleep(waiting)


    def random_position(self):
        return (
            random.randint(0, self.frame.width - 1),
            random.randint(0, self.frame.height - 1)
        )