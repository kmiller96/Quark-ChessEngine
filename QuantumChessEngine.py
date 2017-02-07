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
import time
from lib import core, chessboard, engine, movegenerator, pieces, usercontrol

# Define globals.
VERSION = 'alpha 1.00.00'
SLEEP_TIME = 0.1
USER_OPTIONS = ['hist', 'move', 'quit']
HELPMESSAGE_NOTATION = "Uhhh... Sorry I can't help you at the moment."

# Initialise the components of the board.
UI = usercontrol.EngineUI()
GUI = usercontrol.EngineGUI()

def rest():
    """Pauses a program for the designated time."""
    time.sleep(SLEEP_TIME)
    return None

def startprogram():
    print "Welcome, to Quark Chess Engine!"
    print "You are playing the version %r of the engine.\n\n" % VERSION
    rest()
    print "Let me introduce you to the rules."
    rest()
    print " - The board is rendered as an ASCII picture. Each piece has its "
    print "   own symbol (K, Q, B, N, R and P) which is either capitalised if "
    print "   white or lowercase if black. If the square is blank then a period "
    print "   (the '.' symbol) is used to denote the square."""
    rest(); rest(); rest()
    print " - To make a move you are required to pass a notation string to\n" \
          "   designate where you wish to move to. This notation string however\n" \
          "   is special as it helps to clearly define what move you wish to\n" \
          "   make.\n"
    rest(); rest(); rest()
    print "PRESS ENTER TO CONTINUE."
    raw_input()
    return None


def letuserpickgametype():
    """Lets the user pick what board/gametype they want to play on."""
    print "While we are debugging, you can only play on a normal chess board."
    rest()
    print "Initalising the chessboard..."
    board = chessboard.ChessBoard
    print "Done!"
    return board


def initialisethisboard(boardtype):
    """Creates the board to play on. Just calls the class to initalise it."""
    board = boardtype()
    board.setupnormalboard()
    return board


def whogoesfirst():
    """Determines if the player or computer goes first."""
    return True  # HACK: Until I write proper code.


def promptuser(commandlist):
    """Get the user's command."""
    # commanddict = {
    #     'hist': printmovehistory,
    #     'move': processmove,
    #     'quit': resign
    # }
    print "What would you like to do? Please pass what is in the parenthesis."
    print "  - Get the move history (%s)" % commandlist[0]
    print "  - Make a move (%s)" % commandlist [1]
    print "  - Resign (%s)" % commandlist[2]

    while True:
        usercommand = raw_input('> ')
        if usercommand in commandlist:
            return usercommand
        else:
            print "Not a valid option. Please pass one of %s" % commandlist
    return None


def promptuserformove():
    """Get the move that the user wants to make."""
    print "\nPlease type in the move string you wish to make. If you want to see"
    print "the rules for making these special strings type 'help'."
    while True:
        movestring = raw_input('> ')
        try:
            if movestring.lower() == 'help':
                print HELPMESSAGE_NOTATION
            else:
                piecetomove, movetuple = UI.processusermove(movestring)
        except (NameError, core.UnknownPieceError) as e:
            print "%r is not a valid string." % movestring
            print "Type 'help' if you need assistance with the naming rules."
        else:
            break
    return piecetomove, movetuple, movestring


def islegalmove(piece, movetuple):
    """Determine if the move is legal."""
    return True


def makemove(movetuple, board):
    """Make the move passed on board."""
    board.move(movetuple[0], movetuple[1], force=True)
    return None


def printhistory(historylist):
    """Prints the history of the game."""
    if historylist == []:
        print "\nYou have to make a move to see the history of the game!"
    else:
        print "\nHere is the history of the game so far:"
        print historylist
    return None


def makebestmove(board):
    """Makes the best move on board."""
    pass


def switchcolours(board):
    """A debugging method that allows for the player to change sides."""
    colours = (board.playercolour, board.computercolour)
    (board.playercolour, board.computercolour) = colours[::-1]
    return None


def whowon():
    pass


def gameover(gameresult):
    pass


def resign():
    """The function that handles resignations."""
    print "You lose!"
    return None


def goodbye():
    """The final goodbye message."""
    print "Thanks for playing, I hope to see you again!"
    return None


def main():
    # Begin the program and create the chess board.
    startprogram()

    rest(); rest()

    whichboardtype = letuserpickgametype()  # Force while developing.
    chessboard = initialisethisboard(whichboardtype)

    rest(); rest()

    print "\nDuring debugging, you will be playing as both white and black."
    debug = True
    print "PRESS ENTER TO START THE GAME."
    raw_input()
    print ""

    # Now play the game.
    userturn = whogoesfirst(); firstloop = True
    while True:
        # See if the user won the game.
        if gameover:
            result = whowon()
            gameover(result)

        # Otherwise play normally.
        if userturn:
            if firstloop:
                print GUI.generateasciiboard(chessboard, side=chessboard.playercolour)

            command = promptuser(USER_OPTIONS)  # Get the user command.

            if command == 'hist':  # Look at the game history.
                printhistory(UI.history)
                print ""

            elif command == 'move':  # Make a move.
                piece, movetuple, movestr = promptuserformove()
                if islegalmove(piece, movetuple):
                    # Make move and add it to the history.
                    makemove(movetuple, board=chessboard)
                    UI.addmovetohistory(
                        piece('white').notationsymbol,
                        movetuple[0], movetuple[1])
                    # Cleanup.
                    userturn = False; firstloop = True
                    continue
                else:
                    print "\nThat move is not valid."

            elif command == 'exit':  # Quit out of the game.
                resign()
                break

        else:
            if not debug:
                makebestmove(board=chessboard); firstloop = True
                continue
            else:
                switchcolours(chessboard)
                userturn = True; firstloop = True  # Force the player to play again.
                continue
        firstloop = False
    goodbye()
    return None

if __name__ == '__main__':
    main()
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.:.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
