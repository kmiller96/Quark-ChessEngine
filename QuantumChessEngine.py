# AUTHOR: Kale Miller
# DESCRIPTION: Front end execution of the chess engine.

# 416c7761797320636f646520617320696620746865206775792077686f20656e6473207570206d
# 61696e7461696e696e6720796f757220636f64652077696c6c20626520612076696f6c656e7420
# 70737963686f706174682077686f206b6e6f777320776865726520796f75206c6976652e

# DEVELOPMENT LOG:
#    30/12/16: Initalised the front-end script. Added psuedo code.

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~EXECUTION~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
DRAFT EXECUTION - DEBUGGING LEVEL OF UI:
===================
- Start up program.
- Prompt the user to set up the board. This is done by passing in the pieces (
which would be symbolised by their notation like K for king, N for knight) with
a set of coordinates.
- Otherwise let a default game be generated.

- ???
- Profit.
"""
from lib import core, exceptions

def startprogram():
    pass


def letuserpickgametype():
    pass


def initialisethisboard(boardtype):
    pass


def promptuserformove():
    pass


def makebestmove():
    pass


def whowon():
    pass


def gameover(gameresult):
    pass


def main():
    # Begin the program and create the chess board.
    startprogram()
    whichboardtype = letuserpickgametype()
    chessboard = initialisethisboard(whichboardtype)

    # Now play the game.
    while True:
        # Make a move.
        if userturn:
            promptuserformove()
        else:
            if not debug:
                makebestmove()
            else:
                promptuserformove(debug=True)

        # See if the user won the game.
        if gameover:
            result = whowon()
            gameover(result)
    return None

if __name__ == '__main__':
    main()
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.:.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
