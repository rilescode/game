from collections import deque

DEPTH = 2


def next_move_minimax(board, current_x, current_y):
    bestMove = None
    best_score = -float("inf")

    for next_x, next_y in legal_moves(board, current_x, current_y):
        new_board = [row[:] for row in board]
        new_board[next_x][next_y] = "me"
        score = min_value(new_board, next_x, next_y, DEPTH)
        if score > best_score:
            best_score = score
            bestMove = (next_x, next_y)

    return bestMove


def min_value(board, x, y, depth):
    if depth == 0:
        return value(board, x, y)
    v = float("inf")

    for next_x, next_y in legal_moves(board, x, y):
        new_board = [row[:] for row in board]
        new_board[next_x][next_y] = "opponent"
        v = min(v, max_value(new_board, next_x, next_y, depth - 1))
    return v


def max_value(board, x, y, depth):
    if depth == 0:
        return value(board, x, y)
    v = -float("inf")

    for next_x, next_y in legal_moves(board, x, y):
        new_board = [row[:] for row in board]
        new_board[next_x][next_y] = "me"
        v = max(v, min_value(new_board, next_x, next_y, depth - 1))
    return v


def legal_moves(board, x, y):
    rows, cols = len(board), len(board[0])
    possible_moves = [
        (x, y + 1),  # right
        (x, y - 1),  # left
        (x + 1, y),  # down
        (x - 1, y),  # up
    ]
    return [
        (x, y)
        for x, y in possible_moves
        if 0 <= x < rows and 0 <= y < cols and board[x][y] is None
    ]


def value(board, x, y):
    score = evaluate_current_position(board, x, y)
    return score


def evaluate_current_position(board, x, y):
    return (
        calculate_available_space(board, x, y) * 0.7
        + calculate_center_distance(board, x, y) * 0.3
    )


def calculate_center_distance(board, x, y):
    center_x, center_y = len(board) // 2, len(board[0]) // 2
    return abs(x - center_x) + abs(y - center_y)


# Flood fill algo!
def calculate_available_space(board, start_x, start_y):
    rows, cols = len(board), len(board[0])
    visited = set()
    queue = deque([(start_x, start_y)])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while queue:
        x, y = queue.popleft()
        if (x, y) not in visited:
            visited.add((x, y))
            for dx, dy in directions:
                newx, newy = x + dx, y + dy
                if 0 <= newx < rows and 0 <= newy < cols and board[newx][newy] is None:
                    queue.append((newx, newy))
    return len(visited)
