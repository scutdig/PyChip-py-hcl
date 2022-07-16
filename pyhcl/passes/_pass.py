from typing import List

class Pass:
    ...

#Error handling
class PassException(Exception):
    def __init__(self, message: str):
        self.message = message
    
    def __str__(self):
        return self.message


class PassExceptions(Exception):
    def __init__(self, exceptions: List[PassException]):
        self.message = '\n'.join([str(exception) for exception in exceptions])
    
    def __str__(self):
        return '\n' + self.message
    

class Error:
    def __init__(self):
        self.errors: List[PassException] = []

    def append(self, pe: PassException):
        self.errors.append(pe)
    
    def trigger(self):
        if len(self.errors) == 0:
            return
        elif len(self.errors) == 1:
            raise self.errors.pop()
        else:
            self.append(f'{len(self.errors)} errors detected!')
            raise PassExceptions(self.errors)