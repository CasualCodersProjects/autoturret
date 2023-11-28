class Stepper:
    def __init__(self, step_pin, direction_pin, enable_pin, sleep_time=0.0005):
        self.direction_pin = direction_pin
        self.step_pin = step_pin
        self.sleep_time = sleep_time
        self.enable_pin = enable_pin
        print("Dummy stepper initialized")
    
    def setup(self):
        print("DummyStepper set up")
        pass

    def step(self, direction, steps=200):
        print(f"Dummy Stepper moving in direction {direction}, {steps} steps")

    def cleanup(self):
        print("Cleaning up stepper")

