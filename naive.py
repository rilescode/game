# 'objective' function
#  evaluate the position of the player at (x, y)
def naive_evaluate_position(board, x, y):
    # min_distance = min_wall_distance(board, x, y)
    wall_hugging_score = wall_hug_score(board, x, y)

    free_cells = sum(
        [
            count_free_cells(board, x, y, 0, 1),  # right
            count_free_cells(board, x, y, 0, -1),  # left
            count_free_cells(board, x, y, 1, 0),  # down
            count_free_cells(board, x, y, -1, 0),  # up
        ]
    )

    # return min_distance + free_cells
    return wall_hugging_score + free_cells


# Weight scores based on the distance to the nearest wall
def wall_hug_score(board, x, y):
    rows, cols = len(board), len(board[0])
    dist_to_left = x
    dist_to_right = cols - 1 - x
    dist_to_top = y
    dist_to_bottom = rows - 1 - y

    # invert the distance to the nearest wall
    score = rows - min(dist_to_left, dist_to_right, dist_to_top, dist_to_bottom)
    return score


# count the number of free cells in a given direction
def count_free_cells(board, x, y, dx, dy):
    rows, cols = len(board), len(board[0])
    max_depth = 5
    count = 0
    for i in range(1, max_depth + 1):
        newx, newy = x + i * dx, y + i * dy
        if 0 <= newx < rows and 0 <= newy < cols and board[newx][newy] is None:
            count += 1
        else:
            break
    return count


# calculate the distance to the nearest wall or color
def min_wall_distance(board, x, y):
    rows, cols = len(board), len(board[0])
    min_distance = float("inf")
    for i in range(rows):
        for j in range(cols):
            if board[i][j] is not None:
                distance = abs(x - i) + abs(y - j)
                min_distance = min(min_distance, distance)
    return min_distance
