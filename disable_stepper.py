import RPi.GPIO as GPIO

pins = [8, 36, 37]

GPIO.setmode(GPIO.BOARD)

for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
