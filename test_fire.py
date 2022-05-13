import RPi.GPIO as GPIO

import time

AIR_PIN = 37

GPIO.setmode(GPIO.BOARD)

GPIO.setup(AIR_PIN, GPIO.OUT)

try:
    while True:
        for i in range(5):
            GPIO.output(AIR_PIN, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(AIR_PIN, GPIO.LOW)
            time.sleep(1)

        for i in range(5):
            GPIO.output(AIR_PIN, GPIO.LOW)
            time.sleep(0.5)
            GPIO.output(AIR_PIN, GPIO.HIGH)
            time.sleep(0.5)
finally:
    GPIO.output(AIR_PIN, GPIO.LOW)
    GPIO.cleanup()
