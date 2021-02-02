import random
import copy
import math
from chess_board import ChessBoard


def create_chess_board(dimension):
    board = [['0' for i in range(0, dimension)] for j in range(0, dimension)]
    for i in range(0, dimension):
        queen_index = random.randint(0, dimension - 1)
        board[i][queen_index] = 'Q' + str(i)
    return ChessBoard(evaluation_function(copy.deepcopy(board)), board)


def evaluation_function(current_board):
    value = 0
    queen_x_index = 0
    while queen_x_index < len(current_board):
        queen_y_index = 0
        # find y_index of queen
        while True:
            if current_board[queen_x_index][queen_y_index] == 'Q' + str(queen_x_index):
                break
            queen_y_index += 1
        # check intersects
        value += count_intersects(current_board, queen_x_index, queen_y_index)
        # make that queen go away for not repeating in next calculations
        current_board[queen_x_index][queen_y_index] = '0'
        queen_x_index += 1
    return value


def print_board(start_board):
    for i in range(len(start_board)):
        for j in range(len(start_board)):
            print(start_board[i][j][0], end=" ")
        print("\n", end="")


def count_intersects(board, queen_x, queen_y):
    intersect_counter = 0
    # row and column
    for i in range(len(board)):
        if i != queen_y and board[queen_x][i] != '0':
            intersect_counter += 1
        if i != queen_x and board[i][queen_y] != '0':
            intersect_counter += 1
    # diagonal
    for i in range(len(board)):
        first_diagonal = queen_x + queen_y - i
        second_diagonal = i - (queen_x - queen_y)
        if 0 <= first_diagonal < len(board) and i != queen_x and board[i][first_diagonal] != '0':
            intersect_counter += 1
        if 0 <= second_diagonal < len(board) and i != queen_x and board[i][second_diagonal] != '0':
            intersect_counter += 1
    return intersect_counter


def get_neighbor(current_chess_board):
    b = current_chess_board.board
    queen_x = random.randint(0, len(b) - 1)
    queen_y = 0
    # find y_index of queen
    while True:
        if b[queen_x][queen_y] == 'Q' + str(queen_x):
            break
        queen_y += 1
    # loop for different position
    while True:
        new_y_index = random.randint(0, len(b) - 1)
        if new_y_index != queen_y:
            break
    b[queen_x][queen_y] = '0'
    b[queen_x][new_y_index] = 'Q' + str(queen_x)
    return ChessBoard(evaluation_function(copy.deepcopy(b)), b)


def simulated_annealing(start_chess_board, initial_temp, final_temp, alpha):
    current_temp = initial_temp
    current_state = start_chess_board
    solution = current_state
    while current_temp > final_temp:
        neighbor = get_neighbor(copy.deepcopy(current_state))
        if neighbor.evaluation_value == 0:
            return neighbor
        cost_diff = current_state.evaluation_value - neighbor.evaluation_value
        print(math.exp(cost_diff / current_temp))
        if cost_diff > 0:
            current_state = neighbor
        else:
            if random.uniform(0, 1) < math.exp(cost_diff / current_temp):
                current_state = neighbor
        if current_state.evaluation_value < solution.evaluation_value:
            solution, current_state = current_state, solution
        current_temp -= alpha
    return solution


# m = [['0', '0', '0', '0', '0', '0', 'Q0', '0'], ['0', '0', '0', 'Q1', '0', '0', '0', '0'],
#      ['0', '0', '0', '0', '0', '0', '0', 'Q2'], ['0', '0', '0', '0', 'Q3', '0', '0', '0'],
#      ['0', 'Q4', '0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', 'Q5', '0', '0'],
#      ['0', '0', 'Q6', '0', '0', '0', '0', '0'], ['Q7', '0', '0', '0', '0', '0', '0', '0']]
# print(evaluation_function(m))

chess_board = create_chess_board(8)
print(chess_board.board)
print_board(chess_board.board)
print(chess_board.evaluation_value)

result = simulated_annealing(chess_board, 20, 0, 1)

print(result.board)
print_board(result.board)
print(result.evaluation_value)
