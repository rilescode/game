import requests

root_url = "http://light-bikes.inseng.net"


def create_test_game(
    add_server_bot=True, board_size=25, num_players=2, server_bot_difficulty=2
):
    endpoint = f"{root_url}/games"

    params = {
        "addServerBot": str(add_server_bot).lower(),
        "boardSize": board_size,
        "numPlayers": num_players,
        "serverBotDifficulty": server_bot_difficulty,
    }

    response = requests.post(endpoint, params=params)
    if response.status_code == 201:
        return response.json()
    else:
        print(f"Unexpected status code: {response.status_code}")
        return None


def show_game(game_id):
    endpoint = f"{root_url}/games/{game_id}"
    response = requests.get(endpoint)
    if response.status_code == 200:
        return response.json()["games"][0]
    else:
        print(f"Unexpected status code: {response.status_code}")
        return None


def join_game(game_id, player_name):
    endpoint = f"{root_url}/games/{game_id}/join"
    params = {"name": player_name}

    response = requests.post(endpoint, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Unexpected status code: {response.status_code}")
        return None


def move(game_id, player_id, x, y):
    endpoint = f"{root_url}/games/{game_id}/move"
    params = {"playerId": player_id, "x": x, "y": y}

    response = requests.post(endpoint, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Unexpected status code: {response.status_code}")
        print(response.json())
        return None


# determine the next move
def next_move(board, current_x, current_y):
    bestMove = None
    best_score = -float("inf")
    rows, cols = len(board), len(board[0])

    possible_moves = [
        (current_x, current_y + 1),  # right
        (current_x, current_y - 1),  # left
        (current_x + 1, current_y),  # down
        (current_x - 1, current_y),  # up
    ]

    for x, y in possible_moves:
        if 0 <= x < rows and 0 <= y < cols and board[x][y] is None:
            score = evaluate_move(board, x, y)
            if score > best_score:
                bestMove = (x, y)
                best_score = score
    print("best score", best_score)
    return bestMove


# 'objective' function
#  evaluate the move based on the distance to the nearest wall and the number of free cells
def evaluate_move(board, x, y):
    min_distance = min_wall_distance(board, x, y)
    free_cells = sum(
        [
            count_free_cells(board, x, y, 0, 1),  # right
            count_free_cells(board, x, y, 0, -1),  # left
            count_free_cells(board, x, y, 1, 0),  # down
            count_free_cells(board, x, y, -1, 0),  # up
        ]
    )

    return min_distance + free_cells


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


# create a test game
game = create_test_game()
game_id = game["id"]

# join the game
res = join_game(game_id, "test")
print(res)

game_response = show_game(game_id)


current_board_state = game_response["board"]
players = game_response["players"]
my_id = game_response["current_player"]["id"]

while game_response["winner"] is None:
    # get the current game state
    game_response = show_game(game_id)
    current_board_state = game_response["board"]
    players = game_response["players"]

    # check if it's my turn
    if game_response["current_player"]["id"] != my_id:
        continue

    # check if the game is over
    if game_response["winner"] is not None:
        break

    # now it's my turn
    my_x = game_response["current_player"]["x"]
    my_y = game_response["current_player"]["y"]

    # get the next move
    new_x, new_y = next_move(current_board_state, my_x, my_y)

    # make the move
    move_response = move(game_id, my_id, new_x, new_y)
    game_response = show_game(game_id)

print("winner: ", game_response["winner"])
