class DynamicContext:
    _lst = []
    _scopeId = [object()]
    _delScope = []

    @staticmethod
    def push(stuff):
        DynamicContext._lst.append(stuff)

    @staticmethod
    def pop():
        res = DynamicContext._lst.pop()
        return res

    @staticmethod
    def get():
        res = DynamicContext._lst
        DynamicContext._lst = []
        return res

    @staticmethod
    def currentScope():
        return id(DynamicContext._scopeId[-1])

    @staticmethod
    def createScope():
        obj = object()
        DynamicContext._scopeId.append(obj)
        return id(obj)

    @staticmethod
    def deleteScope():
        DynamicContext._delScope.append(DynamicContext._scopeId[-1])
        DynamicContext._scopeId.pop()

    @staticmethod
    def clearScope():
        DynamicContext._scopeId.clear()
        DynamicContext._delScope.clear()
        DynamicContext._scopeId.append(object())
