from pyhcl.core._clock_manager import Clock_manager

class DslChecker:

    @classmethod
    def do_check(cls, vic):
        DslChecker.clock_check(vic)

    @classmethod
    def clock_check(cls, vic):
        pass

    @classmethod
    def loop_check(cls, vic):
        pass