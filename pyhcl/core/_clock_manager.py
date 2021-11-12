class Clock_manager:
    _clocks = []
    _resets = []
    _map = {}

    @staticmethod
    def push(clock, reset):
        Clock_manager._clocks.append(clock)
        Clock_manager._resets.append(reset)

    @staticmethod
    def pop():
        Clock_manager._clocks.pop()
        Clock_manager._resets.pop()

    @staticmethod
    def empty():
        return len(Clock_manager._map) == 0

    @staticmethod
    def clockempty():
        return len(Clock_manager._clocks) == 0

    @staticmethod
    def resetempty():
        return len(Clock_manager._resets) == 0

    @staticmethod
    def getClock():
        if(Clock_manager.clockempty()):
            raise Exception("No Clock")
        return Clock_manager._clocks[-1]

    @staticmethod
    def getReset():
        if(Clock_manager.resetempty()):
            raise Exception("No Reset")
        return Clock_manager._resets[-1]

    @staticmethod
    def getClockByID(id):
        if id in Clock_manager._map:
            return Clock_manager._map[id][0]
        raise Exception("Can not find a clock by ID")  # default

    @staticmethod
    def getResetByID(id):
        if id in Clock_manager._map:
            return Clock_manager._map[id][1]
        raise Exception("Can not find a reset by ID") # default

    @staticmethod
    def register(id):
        Clock_manager._map[id] = (Clock_manager.getClock(), Clock_manager.getReset())

    @staticmethod
    def defaultclock():
        Clock_manager.push("clock", "reset")
