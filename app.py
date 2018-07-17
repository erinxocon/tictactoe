import json

import socketio
import eventlet

from flask import Flask, render_template, request, jsonify, g, redirect, url_for
from redis import Redis

from tictactoe import create_new_state, make_move

sio = socketio.Server()
app = Flask(__name__)
REDIS = "redis"


@app.route("/", methods=["GET", "POST"])
def index():
    """Serve the client-side application."""
    if request.method == "GET":
        # if get method was used serve the beginning app page
        return render_template("index.html")
    elif request.method == "POST":
        # If the request was post then we create a new state and save it to redis
        game_state = create_new_state(grid_size=int(request.form["grid_size"]))
        # extract game code for use in redis
        game_code = game_state["game_code"]
        # Connect to redis and store the initial game state
        r = Redis(host=REDIS)
        r.set(game_code, json.dumps(game_state))
        # redirect to the game page
        return redirect(location=url_for("retrieve_game", code=game_code))


@app.route("/join_game", methods=["POST"])
def join_game():
    """Join a game in progress"""
    return redirect(location=url_for("retrieve_game", code=request.form["game_code"]))


@app.route("/<code>", methods=["GET"])
def retrieve_game(code):
    """The endpoint that serves the actual game page"""
    return render_template("game.html")


@sio.on("connect")
def connect(sid, environ):
    """Utility listener that lets you know when someone has connected"""
    print("connect ", sid)


@sio.on("disconnect")
def disconnect(sid):
    """Utility listener that lets you know when someone has disconnected"""
    print("disconnect ", sid)


@sio.on("enter_room")
def enter_room(sid, game_code):
    """This lets game be seperate so we can handle a lot of connections without
    addressing everyone at once
    """
    # Load the game state (payload) from redis.
    r = Redis(host=REDIS)
    game_state_json = r.get(game_code).decode("utf-8")
    game_state = json.loads(game_state_json)
    # First player to join is X, then Y, then spectator
    if game_state["player1"] is None:
        game_state["player1"] = sid

    elif game_state["player2"] is None:
        game_state["player2"] = sid
    new_game_state = json.dumps(game_state)
    # Persist new game state to redis.
    r.set(game_state["game_code"], new_game_state)
    sio.enter_room(sid, game_code)


@sio.on("get_game_state")
def get_game_state(sid, game_code):
    """Returns a game state from a given game_code"""
    # connect to redis
    r = Redis(host=REDIS)
    # decode the binary response redis returned
    game_state_json = r.get(game_code).decode("utf-8")
    # Trigger event for clients in the room that there is a new gamestate.
    sio.emit("init_game_state", game_state_json, room=game_code)


@sio.on("make_move")
def move(sid, game_code, move_data, emblem):
    # Load the game state (payload) from redis.
    r = Redis(host=REDIS)
    game_state_json = r.get(game_code).decode("utf-8")
    game_state = json.loads(game_state_json)
    # Check to see who's turn it's supposed to be
    if game_state["move_count"] % 2 == 0:
        turn = game_state["player1"]
    else:
        turn = game_state["player2"]
    # if the initiating sid isn't the same as the turn sid, then raise an exception
    if turn != sid:
        raise Exception(turn, sid, "It's not your turn!")
    # Create new game state based on user input.
    moved_state = make_move(
        game_state=game_state, x=move_data["x"], y=move_data["y"], emblem=emblem
    )

    moved_json = json.dumps(moved_state)
    # Persist new game state to redis.
    r.set(game_state["game_code"], moved_json)
    # Emit SocketIO event for updated game_state.
    sio.emit("game_state_change", moved_json, room=game_code)

    # If an end-game condition is found...
    if game_state["win_state"] is True:
        # A player won the game.
        winner = "X" if game_state["move_count"] % 2 == 0 else "O"
        sio.emit("win_state", winner, room=game_code)
    elif game_state["win_state"] is "Draw":
        # The game is a draw.
        sio.emit("draw", room=game_code)


if __name__ == "__main__":
    # wrap Flask application with socketio's middleware
    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(("0.0.0.0", 8000)), app)

