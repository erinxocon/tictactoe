import random
from string import ascii_uppercase
import json


def create_new_state(*, grid_size=3):
    """Created a new dictionary containing information for a new game state

    Returns a dictionary, containing the new game_state:
        - "winning": True, False, or "Draw".
        - "move_count": Number of moves that have passed
        - "grid_szie": size of the board
        - "game_code": Reference code for the current game, used for other players to join.
        - "state": a two dimensional list containing the current board state
    """

    cells = [{"state": ""} for _ in range(grid_size)]
    rows = [{"cells": cells} for _ in range(grid_size)]
    empty_board = dict(rows=rows)

    game_code = "".join(random.choices(ascii_uppercase, k=5))
    return dict(
        state=empty_board,
        move_count=0,
        grid_size=grid_size,
        game_code=game_code,
        win_state=False,
        player1=None,
        player2=None,
        emblem1="🍰",
        emblem2="🌈",
    )


def make_move(*, game_state, x, y, emblem):
    """Adds move to the current state and checks if there are any winning conditions, or a draw.

    Returns a dictionary, containing the new game_state:
        - "winning": True, False, or "Draw".
        - "move_count": Number of moves that have passed
        - "grid_szie": size of the board
        - "game_code": Reference code for the current game, used for other players to join.
        - "state": a two dimensional list containing the current board state
    """
    x = int(x)
    y = int(y)
    if game_state["state"]["rows"][x]["cells"][y]["state"] == "":
        game_state["state"]["rows"][x]["cells"][y]["state"] = emblem

    # check if there are any winning conditions in the rows
    for i in range(game_state["grid_size"]):
        if game_state["state"]["rows"][i]["cells"][y]["state"] != emblem:
            break
        elif i == game_state["grid_size"] - 1:
            game_state["win_state"] = True
            return game_state

    # check if there are any winning conditions in the columns
    for i in range(game_state["grid_size"]):
        if game_state["state"]["rows"][x]["cells"][i]["state"] != emblem:
            break
        elif i == game_state["grid_size"] - 1:
            game_state["win_state"] = True
            return game_state

    # check the diagonals for winning conditions
    for i in range(game_state["grid_size"]):
        if game_state["state"]["rows"][i]["cells"][i]["state"] != emblem:
            break
        elif i == game_state["grid_size"] - 1:
            game_state["win_state"] = True
            return game_state

    # check the other diagonal
    for i in range(game_state["grid_size"]):
        if (
            game_state["state"]["rows"][i]["cells"][(game_state["grid_size"] - 1) - i][
                "state"
            ]
            != emblem
        ):
            break
        elif i == game_state["grid_size"] - 1:
            game_state["win_state"] = True
            return game_state

    if game_state["move_count"] == (game_state["grid_size"] ** 2) - 1:
        game_state["win_state"] = "Draw"
        return game_state

    # increment the move counter and set the player to the other
    game_state["move_count"] += 1

    # return flase since no winning conditions were found
    return game_state


if __name__ == "__main__":
    j = json.dumps(create_new_state(grid_size=3))
    print(j)
