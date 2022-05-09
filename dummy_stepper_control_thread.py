class StepperThread:
    def __init__(self, step_pin, direction_pin, enable_pin, sleep_time=0.0005):
        self.step_pin = step_pin
        self.direction_pin = direction_pin
        self.enable_pin = enable_pin
        self.sleep_time = sleep_time
        print("Dummy Stepper Thread created")

    def start(self):
        self.setup()
        print("Dummy Stepper Thread started")
        return self

    def setup(self):
        print("Dummy Stepper Thread setup")

    def set_direction(self, direction):
        print(f'Dummy Stepper Thread set_direction: {direction}')

    def stop(self):
        print("Dummy Stepper Thread stopped")

    def cleanup(self):
        print("Dummy Stepper Thread cleaned up")

    def close(self):
        self.cleanup()
