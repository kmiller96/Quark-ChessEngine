# DESCRIPTION: Contains all of the code, classes and functions corresponding to
# the board.

# 50726f6772616d6d696e6720697320627265616b696e67206f66206f6e652062696720696d706f
# 737369626c65207461736b20696e746f207365766572616c207665727920736d616c6c20706f73
# 7369626c65207461736b732e

# NOTE:
# ================
# This file is currently a work in progress. The original chessboard.py file has
# become overly bloated and is detrimental to the moral of the project. This new
# script is aimed at taking only the methods that pertain to a chessboard, while
# separating the other components into their own scrips

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MAIN~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from lib import core, vectors, pieces
from copy import deepcopy

class _ChessBoardCore:
    """Contains the core methods, plus the __init__ method."""

    def __init__(self):
        """Initialises the board."""
        self._board = [None] * 64
        self.playercolour = 'white'
        self.computercolour = 'black'

        # Define initial states
        self.cancastleleft = True
        self.cancastleright = True
        self.enpassant = None

    def __getitem__(self, pos):
        """Controls calling the piece at a position on the board like a list."""

        errormsg = "The board is read either as a index from 0 to 63 or a " \
        "tuple/list that specifies the row and column index."
        try:
            position = core.convert(pos, toindex=True)
            return self._board[position]
        except IndexError:
            raise IndexError(errormsg)
        except TypeError:
            raise TypeError(errormsg)  # If the pos is wrong type, raise TypeError.

    def __setitem__(self, pos, piece):
        """Add a piece on the board at pos."""
        errormsg = ("Please pass a position on the board and a piece that "
                    "derives from BasePiece")
        try:
            assert isinstance(piece, pieces.BasePiece), errormsg
            position = core.convert(pos, toindex=True)
            self._board[position] = piece
        except AssertionError:
            raise TypeError(errormsg)
        except IndexError:
            raise IndexError(errormsg)
        except TypeError:
            raise TypeError(errormsg)
        else:
            return None

    def __iter__(self):
        """Iterate over each square on the board."""
        for square in self._board:
            yield square

    def duplicateboard(self):
        """Creates an instance of the chess board exactly as it is now."""
        return deepcopy(self)

    def setplayercolour(self, colour):
        """Assigns a colour to the player."""
        errormsg = "Colour of the piece must be 'white' or 'black'"
        try:
            assert colour.lower() in ('white', 'black')
            if colour.lower() == 'white':
                self.playercolour = 'white'
                self.computercolour = 'black'
            elif colour.lower() == 'black':
                self.playercolour = 'black'
                self.computercolour = 'white'
            else:
                raise RuntimeError("!!!UNKNOWN ERROR!!!")
        except AssertionError:
            raise NameError(errormsg)
        except AttributeError:
            raise TypeError(errormsg)
        return None

    def isplayercolour(self, colour):
        """Determines if the colour passed is the player's colour or not."""
        errormsg = "The colour of the piece must be 'white' or 'black'"
        try:
            assert colour.lower() in ('white', 'black')
        except AssertionError:
            raise NameError(errormsg)
        except AttributeError:
            raise TypeError(errormsg)
        else:
            return (colour.lower() == self.playercolour)

    def positiononboard(self, position):
        """Returns boolean depending on if the position is on the board."""
        pos = core.convert(position, tocoordinate=True)
        if 0 <= pos[0] <= 7 and 0 <= pos[1] <= 7:
            return True
        else:
            return False

    def assertPositionOnBoard(self, position):
        """Asserts that the position is valid."""
        try:
            index = convert(position, toindex=True)
            self._board[index]
        except IndexError:  # If off board.
            raise IndexError("The position %r is off the board." % position)
        return None

    def assertIsUnoccupied(self, position):
        """Asserts that the square is free and unoccupied."""
        try:
            index = convert(position, toindex=True)
            assert self._board[index] == None, "The target square is occupied."
        except IndexError:
            raise IndexError("The index used is off the board!")
        return None

    def assertIsOccupied(self, position):
        """Asserts that the square is occupied."""
        try:
            index = convert(position, toindex=True)
            assert self._board[index] != None, "The target square is unoccupied."
        except IndexError:
            raise IndexError("The index used is off the board!")
        return None

class ChessBoard(_ChessBoardCore):
    """The public class that is the chessboard.

    This class creates a chessboard, much like you have a physical board when
    you play chess. It is a pretty dumb class however; it doesn't have many
    checks in place for moves and it can't do anything special like make moves.
    """

    def findpiece(self, piecetype, colour):
        """Finds all instances of piece on the board that belong to one side."""
        piecepositions = list()
        for ii, square in enumerate(self._board):
            if square is None:
                continue
            elif ((piecetype is square.piecetype())
                    and square.colour == colour):
                piecepositions.append(ii)
        return piecepositions

    def move(self, startpos, endpos, force=False):
        """A clean way of moving pieces around on the board."""
        # Sanity checks and assertions.
        assert startpos != endpos, \
            "To move the piece, the start and end points must be different."
        startindex = core.convert(startpos, toindex=True)
        endindex = core.convert(endpos, toindex=True)
        self.assertPositionOnBoard(startindex)
        self.assertPositionOnBoard(endindex)
        self.assertIsOccupied(startindex)
        if not force: self.assertIsUnoccupied(endindex)

        # Movement code.
        if startindex == endindex:
            return None  # HACK: Prevents deleting the piece from the board.
        self._board[endindex] = self._board[startindex]
        self._board[startindex] = None
        return None

    def promotepawn(self, position, promoteto):
        """Promotes a pawn at position specified."""
        position = core.convert(position, toindex=True)
        pawnpiece = self._board[position]
        colour = pawnpiece.colour
        self._board[position] = promoteto(colour)
        return None
