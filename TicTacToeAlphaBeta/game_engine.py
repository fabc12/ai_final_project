from node import Node
import copy
import math
import numpy as np


class GameEngine:

    def __init__(self, x, y):
        self.game_board = [['0' for i in range(0, 3)] for j in range(0, 3)]
        self.game_board[x][y] = 'o'
        init_node = Node(list(map(list, self.game_board)), 0, False, True)
        self.game_tree = self.create_game_tree(init_node)
        self.mini_max_alpha_beta(self.game_tree, -math.inf, math.inf)

    def create_game_tree(self, current_node: Node):
        char_to_write = 'x' if current_node.is_computer else 'o'
        temp = self.calculate_value(current_node.board)
        if temp != -2:
            current_node.value = temp
            current_node.is_leaf = True
            return current_node
        for i in range(0, 3):
            for j in range(0, 3):
                if current_node.board[i][j] == '0':
                    if current_node.board[0][0] == 'x' and current_node.board[0][1] == 'o':
                        print('')
                    child_board = copy.deepcopy(current_node.board)
                    child_board[i][j] = char_to_write
                    child_node = Node(child_board, 0, False, not current_node.is_computer)
                    current_node.add_child(child_node)
                    self.create_game_tree(child_node)
        if len(current_node.children) == 0:
            current_node.is_leaf = True
        return current_node

    def calculate_value(self, board):
        winner_char = self.calculate_winner_char(board)
        if winner_char == 'x':
            return 1
        elif winner_char == 'o':
            return -1
        elif winner_char == 'd':
            return 0
        else:
            return -2

    def calculate_winner_char(self, board):
        empty_count = 0
        for i in range(0, 3):
            for j in range(0, 3):
                if board[i][j] == '0':
                    empty_count += 1
        for i in range(0, 3):
            if board[i][0] == board[i][1] == board[i][2] != '0':
                return board[i][0]
            elif board[0][i] == board[1][i] == board[2][i] != '0':
                return board[0][i]
        if board[0][0] == board[1][1] == board[2][2] != '0':
            return board[0][0]
        elif board[0][2] == board[1][1] == board[2][0] != '0':
            return board[0][2]
        elif empty_count == 0:
            return 'd'
        else:
            return ''

    def mini_max_alpha_beta(self, node, alpha, beta):
        print(node.is_computer)
        if node.is_leaf:
            return node.value
        if node.is_computer:
            best = -math.inf
            for child_node in node.children:
                child_node.value = self.mini_max_alpha_beta(child_node, alpha, beta)
                best = max(child_node.value, best)
                alpha = max(best, alpha)
                if alpha >= beta:
                    break
            return best
        else:
            best = math.inf
            for child_node in node.children:
                child_node.value = self.mini_max_alpha_beta(child_node, alpha, beta)
                best = min(child_node.value, best)
                beta = min(best, beta)
                if alpha >= beta:
                    break
            return best

    def next_move(self):
        current_node = self.find_node(self.game_board, self.game_tree)
        max_child = None
        for child in current_node.children:
            if max_child is None:
                max_child = child
            if max_child.value < child.value:
                max_child = child
        # self.game_tree = max_child
        for i in range(0, 3):
            for j in range(0, 3):
                if max_child.board[i][j] != self.game_board[i][j]:
                    return i, j

    def find_node(self, board, node_to_find):
        if board == node_to_find.board:
            return node_to_find
        else:
            for child in node_to_find.children:
                result = self.find_node(board, child)
                if result is not None:
                    return result

    def make_human_move(self, x, y):
        self.game_board[x][y] = 'o'

    def make_computer_move(self, x, y):
        self.game_board[x][y] = 'x'

    def debug_print_tree(self, start_node):
        self.debug_print_node(start_node)
        print()
        for child in start_node.children:
            self.debug_print_node(child)

    def debug_print_node(self, node):
        for i in range(0, 3):
            for j in range(0, 3):
                print(node.board[i][j], end=" ")
            print()
        print()
