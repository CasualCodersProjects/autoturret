# this is the websocket server to control
# the turret remotely
import asyncio
import logging
import os
import signal
import sys

import websockets

logger = logging.getLogger('websockets')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

try:
    from stepper_control_thread import StepperThread
except ModuleNotFoundError:
    from dummy_stepper_control_thread import StepperThread
except RuntimeError:
    from dummy_stepper_control_thread import StepperThread
# from video_get import VideoGet

SLEEP_TIME = 0.001
STEP_X_PIN = 12
DIR_X_PIN = 16
DIR_Y_PIN = 40
STEP_Y_PIN = 38
ENABLE_PIN = 8

# recv format
# x1
# y1
# s1
# x2
x_stepper = StepperThread(
    step_pin=STEP_X_PIN, direction_pin=DIR_X_PIN, enable_pin=ENABLE_PIN, sleep_time=SLEEP_TIME).start()
y_stepper = StepperThread(step_pin=STEP_Y_PIN,
                          direction_pin=DIR_Y_PIN, enable_pin=ENABLE_PIN, sleep_time=SLEEP_TIME).start()


def thread_cleanup(_):
    x_stepper.cleanup()
    y_stepper.cleanup()
    sys.exit(0)


async def handler(websocket):
    async for message in websocket:
        if type(message) == bytes:
            message = message.decode("utf-8")
        # message = message.split(" ")
        # if len(message) != 3:
        #     await websocket.send("Invalid message")
        #     continue
        # try:
        #     x = int(message[0])
        #     y = int(message[1])
        #     shoot = int(message[2])
        # except ValueError:
        #     await websocket.send("Invalid message")
        #     continue
        # x_stepper.set_direction(x)
        # y_stepper.set_direction(y)
        # print(x, y, shoot)
        axis = message[0]
        try:
            direction = int(message[1]) - 1
        except ValueError:
            await websocket.send("Invalid message")
            continue
        if axis == "x":
            x_stepper.set_direction(direction)
        elif axis == "y":
            y_stepper.set_direction(direction)
        elif axis == "s":
            if direction == 1 or direction == 0:
                print("shoot")
            else:
                print("no shoot")
        print(message)


async def main():
    # Set the stop condition when receiving SIGTERM.
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    # these don't seem to work
    # loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)
    # loop.add_signal_handler(signal.SIGINT, stop.set_result, None)
    # these do, so I added sys.exit to the cleanup
    loop.add_signal_handler(signal.SIGTERM, thread_cleanup, None)
    loop.add_signal_handler(signal.SIGINT, thread_cleanup, None)

    port = int(os.environ.get("PORT", "8001"))
    async with websockets.serve(handler, "", port):
        await stop

if __name__ == "__main__":
    asyncio.run(main())
