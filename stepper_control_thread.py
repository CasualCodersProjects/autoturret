import time
from threading import Thread

import RPi.GPIO as GPIO


class StepperThread:
    def __init__(self, step_pin, direction_pin, enable_pin, sleep_time=0.0005):
        GPIO.setmode(GPIO.BOARD)
        self.direction_pin = direction_pin
        self.step_pin = step_pin
        self.sleep_time = sleep_time
        self.enable_pin = enable_pin
        self.kill = False
        self.direction = -1  # this means the steppers are stopped
        self.last_step = 0

    def start(self):
        self.setup()
        Thread(target=self.run, args=()).start()
        return self

    def setup(self):
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.direction_pin, GPIO.OUT)
        GPIO.setup(self.enable_pin, GPIO.OUT)
        GPIO.output(self.enable_pin, GPIO.LOW)

    def set_direction(self, direction):
        if self.direction != direction:
            self.direction = direction
            GPIO.output(self.direction_pin, direction)

    def stop(self):
        self.set_direction(-1)

    def cleanup(self):
        self.kill = True

    def run(self):
        while not self.kill:
            if self.direction != -1:
                GPIO.output(self.step_pin, GPIO.HIGH)
                time.sleep(self.sleep_time)
                GPIO.output(self.step_pin, GPIO.LOW)
                time.sleep(self.sleep_time)
        try:
            GPIO.cleanup()
        except:
            pass
