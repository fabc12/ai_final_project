class Node:
    def __init__(self, position: (), parent: ()):
        self.position = position
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f

    def __repr__(self):
        return '({0},{1})'.format(self.position, self.f)
