from enum import Enum

class Position(Enum):
    root = 0
    InsidePoint = 1
    Leaf = 2

class Stack():
    def __init__(self):
        self.items = []
    def is_empty(self):
        return self.items == []

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)

    def push(self, item):
        self.items.append(item)

    def pop(self, item):
        return self.items.pop()