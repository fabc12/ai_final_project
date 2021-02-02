import random

from node import Node


def create_maze(n):
    maze = [[get_val(i, j, n) for i in range((2 * n) + 1)] for j in range((2 * n) + 1)]
    return maze


def get_val(i, j, n):
    if j % 2 != 0:
        if i == 0 or i == 2 * n:
            return 'w'
        elif i % 2 == 0:
            return 'w' if random.randint(0, 1) else 'o'
        else:
            return '.'
    else:
        if j == 0 or j == 2 * n:
            return 'w'
        elif i == 0 or i == 2 * n:
            return 'w'
        else:
            return 'w' if random.randint(0, 1) else 'o'


def print_maze(maze, n):
    print("  ", end="")
    for i in range(2 * n + 1):
        print(i, end="")
    print("\n", end="")
    for i in range(2 * n + 1):
        print(i, end=" ")
        for j in range(2 * n + 1):
            print(maze[i][j], end="")
        print("\n", end="")


def manhattan_distance(source_x, source_y, destination_x, destination_y):
    return abs(destination_x - source_x) + abs(destination_y - source_y)


def add_to_open(open, neighbor):
    for node in open:
        if neighbor == node and neighbor.f >= node.f:
            return False
    return True


def a_star_search(map, start, end):
    open = []
    closed = []
    start_node = Node(start, None)
    goal_node = Node(end, None)
    open.append(start_node)
    while len(open) > 0:
        open.sort()
        current_node = open.pop(0)
        current_value = map[current_node.position[0]][current_node.position[1]]
        closed.append(current_node)
        if current_node == goal_node:
            path = []
            while current_node != start_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]
        (x, y) = current_node.position
        # print(current_node.position)
        neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        for next in neighbors:
            map_value = map[next[0]][next[1]]
            if map_value == 'w':
                continue
            elif map_value == 'o' and current_value == 'o':
                continue
            neighbor = Node(next, current_node)
            if neighbor in closed:
                continue
            neighbor.g = manhattan_distance(neighbor.position[0], start_node.position[0], neighbor.position[1],
                                            start_node.position[1])
            neighbor.h = manhattan_distance(neighbor.position[0], goal_node.position[0], neighbor.position[1],
                                            goal_node.position[1])
            neighbor.f = neighbor.g + neighbor.h
            if add_to_open(open, neighbor):
                open.append(neighbor)
    return None


def print_path(path, maze, start):
    print(start, end=" ")
    for item in path:
        if maze[item[0]][item[1]] != 'o':
            print(item, end=" ")


# m = [['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'], ['w', '.', 'o', '.', 'w', '.', 'o', '.', 'w', '.', 'w'],
#      ['w', 'o', 'w', 'o', 'w', 'w', 'w', 'w', 'w', 'w', 'w'], ['w', '.', 'w', '.', 'o', '.', 'w', '.', 'o', '.', 'w'],
#      ['w', 'w', 'w', 'o', 'w', 'o', 'w', 'w', 'w', 'o', 'w'], ['w', '.', 'o', '.', 'o', '.', 'o', '.', 'o', '.', 'w'],
#      ['w', 'w', 'w', 'o', 'w', 'o', 'w', 'w', 'w', 'w', 'w'], ['w', '.', 'w', '.', 'w', '.', 'o', '.', 'o', '.', 'w'],
#      ['w', 'o', 'o', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'], ['w', '.', 'w', '.', 'w', '.', 'w', '.', 'w', '.', 'w'],
#      ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w']]

# while True:
#     maze = create_maze(5)
#     start = (1, 1)
#     end = (7, 7)
#     width = 0
#     height = 0
#     path = a_star_search(maze, start, end)
#     if path != None:
#         break
maze = create_maze(5)
start = (1, 1)
end = (7, 5)
path = a_star_search(maze, start, end)
print(maze)
print_maze(maze, 5)
if path is None:
    print("No path found")
else:
    print_path(path, maze, start)
    print()
