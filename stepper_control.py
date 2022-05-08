import RPi.GPIO as GPIO
import time


class Stepper():
    def __init__(self, step_pin, direction_pin, enable_pin, sleep_time=0.0005):
        GPIO.setmode(GPIO.BOARD)
        self.direction_pin = direction_pin
        self.step_pin = step_pin
        self.sleep_time = sleep_time
        self.enable_pin = enable_pin

    def setup(self):
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.direction_pin, GPIO.OUT)
        GPIO.setup(self.enable_pin, GPIO.OUT)
        GPIO.output(self.enable_pin, GPIO.LOW)

    def step(self, direction, steps=200):
        GPIO.output(self.direction_pin, direction)
        for _ in range(steps):
            GPIO.output(self.step_pin, GPIO.HIGH)
            time.sleep(self.sleep_time)
            GPIO.output(self.step_pin, GPIO.LOW)
            time.sleep(self.sleep_time)

    def cleanup(self):
        GPIO.cleanup()


if __name__ == "__main__":
    stepper = Stepper(step_pin=12, direction_pin=16, enable_pin=8)
    stepper.setup()
    stepper.step(direction=1, steps=200)
