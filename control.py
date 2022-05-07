from stepper_control import Stepper
import RPi.GPIO as GPIO
import time

try:
    x_stepper = Stepper(step_pin=12, direction_pin=16, enable_pin=8)
    y_stepper = Stepper(step_pin=38, direction_pin=40, enable_pin=8)

    x_stepper.setup()
    y_stepper.setup()

    while True:
        x_stepper.step(direction=1, steps=500)
        time.sleep(1)
        x_stepper.step(direction=0, steps=500)
        time.sleep(1)
        y_stepper.step(direction=0, steps=200)
        time.sleep(1)
        y_stepper.step(direction=1, steps=200)
        time.sleep(1)


finally:
    GPIO.cleanup()
