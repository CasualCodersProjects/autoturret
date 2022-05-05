# tests controlling the steppers
# import keyboard
# from stepper_control import Stepper
import RPi.GPIO as GPIO

try:
    x_stepper = Stepper(step_pin=12, direction_pin=16, enable_pin=8)
    # y_stepper = Stepper(step_pin=38, direction_pin=40, enable_pin=8)

    x_stepper.setup()

    while True:
        x_stepper.step(direction=1, steps=200)
except KeyboardInterrupt:
    GPIO.cleanup()
