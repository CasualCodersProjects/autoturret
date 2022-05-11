import RPi.GPIO as GPIO


class Pin:
    def __init__(self, pin):
        self.pin = pin

    def setup(self):
        GPIO.setmode(GPIO.BOARD)

    def set_value(self, value):
        GPIO.output(self.pin, value)

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)
