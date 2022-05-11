import time
from multiprocessing import Process, Queue

import RPi.GPIO as GPIO


class StepperThread:
    '''
    Thread that controls a stepper motor. The movement is continuous rather than stepping.
    '''

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
        '''
        Sets up the GPIO pins and starts the thread.
        '''
        self.setup()
        self.queue = Queue()
        self.process = Process(target=self.run, args=(self.queue,))
        self.process.start()
        return self

    def setup(self):
        '''
        Sets up the GPIO pins.
        '''
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.direction_pin, GPIO.OUT)
        GPIO.setup(self.enable_pin, GPIO.OUT)
        GPIO.output(self.enable_pin, GPIO.LOW)

    # direction is 0 for forward, 1 for backwards, -1 for stopped
    def set_direction(self, direction):
        '''
        Sets the direction of the stepper motor.
        '''
        if self.direction != direction:
            self.direction = direction
            self.queue.put(direction)

    def stop(self):
        '''
        Stops the stepper motor.
        '''
        self.set_direction(-1)

    def cleanup(self):
        '''
        Stops the thread gracefully.
        '''
        self.kill = True
        self.process.join()

    def close(self):
        '''
        Stops the thread gracefully.
        '''
        self.cleanup()

    def run(self, queue):
        '''
        The main loop of the thread.
        '''
        last_direction = -1
        while not self.kill:
            if queue.empty():
                direction = last_direction
            else:
                direction = queue.get()

            if direction != -1 and direction != last_direction:
                GPIO.output(self.direction_pin, direction)

            last_direction = direction

            if direction != -1:
                GPIO.output(self.step_pin, GPIO.HIGH)
                time.sleep(self.sleep_time)
                GPIO.output(self.step_pin, GPIO.LOW)
                time.sleep(self.sleep_time)
        try:
            GPIO.cleanup()
        except:
            pass
