class MoveError:
    def __init__(self,text):
        self.text = text
    def __str__(self):
        return self.text

class ResultError:
    def __str__(self):
        return "Invalid result"

class Alarm:
    def __str__(self):
        return "Strategy took too long to move"
