import requests
import sys
import threading

from minimax import next_move_minimax
from naive import naive_evaluate_position

root_url = "http://light-bikes.inseng.net"


def create_test_game(
    add_server_bot=True, board_size=25, num_players=2, server_bot_difficulty=3
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
    print("move sent")
    endpoint = f"{root_url}/games/{game_id}/move"
    params = {"playerId": player_id, "x": x, "y": y}

    response = requests.post(endpoint, params=params)
    if response.status_code == 200:
        return response.json()[0]
    else:
        print(f"Unexpected status code: {response.status_code}")
        print(response.json())
        return None


# determine the next move
def next_move_simple(board, current_x, current_y):
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
            score = naive_evaluate_position(board, x, y)  # This is the line to change
            if score > best_score:
                bestMove = (x, y)
                best_score = score

    if bestMove == None:
        print("board", board)
        print("current_x", current_x)
        print("current_y", current_y)
    return bestMove


def play_game(game_id=None, player_name="Riley!", difficulty=3):
    if game_id is None:
        game = create_test_game(server_bot_difficulty=difficulty)
        game_id = game["id"]
    else:
        print(f"Joining existing game with ID: {game_id}")

    res = join_game(game_id, player_name)

    # Get initial game state
    game_response = show_game(game_id)
    my_id = game_response["current_player"]["id"]
    print(f"My player ID: {my_id}")

    while True:
        # Check if the game is over
        if game_response["winner"] is not None:
            break

        # Check if it's my turn
        if game_response["current_player"]["id"] != my_id:
            game_response = show_game(game_id)
            continue

        current_board_state = game_response["board"]
        my_x = game_response["current_player"]["x"]
        my_y = game_response["current_player"]["y"]

        next_move = next_move_minimax(current_board_state, my_x, my_y)
        if next_move is None:
            next_move = next_move_simple(current_board_state, my_x, my_y)

        new_x, new_y = next_move
        game_response = move(game_id, my_id, new_x, new_y)

    print("Game over. Winner:", game_response["winner"])


def run_multiple_games(num_games):
    threads = []
    for i in range(num_games):
        thread = threading.Thread(
            target=play_game, args=(None, f"bot_difficulty_{i+1}", i + 1)
        )
        threads.append(thread)
        thread.start()

    # Wait for all games to complete
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        game_id = sys.argv[1]
        play_game(game_id)
    else:
        run_multiple_games(1)
