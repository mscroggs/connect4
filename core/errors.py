class MoveError(BaseException):
    def __init__(self,text):
        self.text = text
    def __str__(self):
        return self.text

class ResultError(BaseException):
    def __str__(self):
        return "Invalid result"
