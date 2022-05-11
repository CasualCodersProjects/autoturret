import time
# from threading import Thread
from multiprocessing import Process, Queue


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
        self.process = None

    def start(self):
        self.setup()
        self.queue = Queue()
        self.process = Process(target=self.run, args=(self.queue,))
        self.process.start()
        return self

    def setup(self):
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.direction_pin, GPIO.OUT)
        GPIO.setup(self.enable_pin, GPIO.OUT)
        GPIO.output(self.enable_pin, GPIO.LOW)

    # direction is 0 for forward, 1 for backwards, -1 for stopped
    def set_direction(self, direction):
        if self.direction != direction:
            self.direction = direction
            self.queue.put(direction)

    def stop(self):
        self.set_direction(-1)

    def cleanup(self):
        self.kill = True
        self.process.join()

    def close(self):
        self.cleanup()

    def run(self, queue):
        last_direction = -1
        while not self.kill:
            try:
                direction = queue.get(block=False)
            except:
                direction = last_direction

            if direction != -1:
                GPIO.output(self.direction_pin, direction)

            last_direction = direction

            # print(f"direction:{direction}")

            if direction != -1:
                # print("step")
                GPIO.output(self.step_pin, GPIO.HIGH)
                time.sleep(self.sleep_time)
                GPIO.output(self.step_pin, GPIO.LOW)
                time.sleep(self.sleep_time)
        try:
            GPIO.cleanup()
        except:
            pass
