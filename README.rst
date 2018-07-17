Example can be found at:

http://erincodes.com:8000

To Build
========

.. code-block:: shell

    $ git clone https://github.com/erinxocon/tictactoe.git
    $ cd tictactoe/
    $ docker-compose up --build


Description
===========

This is a real time tic tac toe game that utilizes, Python3, Flask, SocketIO, Redis, and Javascript.  To play, open up a browser to http://hostname:8000 and choose a game board size.  Once done select "Create Game" and you will be presented with a game board and a code in the upper left hand corner.  That is the game code you share with someone else so you can play against them.  They can go to the same main page and enter the code in under the "Join Game" section.  Once in a game, updates to the game state will be pused to clients and stored in the redis database.  Upon receiving a new game stae the page will rerender a new board with the updated moves.  If a winning condition is found, a message is displayed under the game board telling you who won or if it was a draw.  Note: Currently the game works on the honor system, as there is no checking to see who is player 1 or 2, the "x" and "o" emblems are determnined by what the current move number is.  This is an improvement I'd like to make.  Speaking of which..

Improvements
===========

* Store session ID's in the gamestate to determine who is player 1, who is player 2, and who is a spectator
* Use react, or vue to render the game state into a table instead of rerendering it myself.
* CSS
* Redis database is currently unsecured, however you have to be on the docker network docker-compose sets up to access it so this was lower on my list of priorities.
* Games aren't currently private, however you do have to know the game code to access it.



