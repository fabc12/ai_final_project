class Node:
    def __init__(self, board, value: int, is_leaf: bool, is_computer: bool):
        self.board = board
        self.value = value
        self.is_leaf = is_leaf
        self.is_computer = is_computer
        self.children = []

    def add_child(self, node):
        self.children.append(node)
