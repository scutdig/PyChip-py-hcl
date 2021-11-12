from pyhcl.core._clock_manager import Clock_manager

class clockdomin:
    def __init__(self, clock, reset):
        self.clock = clock
        self.reset = reset
        pass
    def __enter__(self):
        Clock_manager.push(self.clock, self.reset)

    def __exit__(self, exc_type, exc_val, exc_tb):
        Clock_manager.pop()