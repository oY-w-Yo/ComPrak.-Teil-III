from enum import Enum

class Position(Enum):
    root = 0
    InsidePoint = 1
    Leaf = 2

class CallingCounter(object):
    def __init__(self,func):
        self.func = func
        self.count = 0
    def __call__(self,*args,**kwargs):
        self.count += 1
        return self.func(*args,**kwargs)
