# DESCRIPTION: Contains all of the code, classes and functions corresponding to
# the board.

# 50726f6772616d6d696e6720697320627265616b696e67206f66206f6e652062696720696d706f
# 737369626c65207461736b20696e746f207365766572616c207665727920736d616c6c20706f73
# 7369626c65207461736b732e

# IDEA: Make a method that iterates over occupied squares only.

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MAIN~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from lib import core, vectors, pieces
from copy import deepcopy


class _ChessBoardCore:
    """Contains the core methods, plus the __init__ method."""

    def __init__(self):
        """Initialises the board."""
        self._board = [None] * 64
        self._colours = core.COLOURS
        self.playercolour, self.computercolour = self._colours

        # Define initial states
        self.cancastleleft = True
        self.cancastleright = True
        self.enpassantforplayer = None
        self.enpassantforcomputer = None

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
            if piece != None:
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

    def __eq__(self, other):
        # REVIEW: Why do I need this method?
        try:
            return self._board == other._board
        except AttributeError:
            if other == None: return False
            else: raise TypeError("Other must be chessboard.")

    def __ne__(self, other):
        # REVIEW: Why do I need this method?
        try:
            return self._board != other._board
        except AttributeError:
            if other == None: return True
            else: raise TypeError("Other must be chessboard.")

    def duplicateboard(self):
        """Creates an instance of the chess board exactly as it is now."""
        return deepcopy(self)

    def findpiece(self, piecetype, colour):
        """Finds all instances of piece on the board that belong to one side."""
        piecepositions = list()
        for ii, square in enumerate(self._board):
            if square is None:
                continue
            elif ((piecetype is square.type)
                    and square.colour == colour):
                piecepositions.append(ii)
        return piecepositions

    def setplayercolour(self, colour):
        """Assigns a colour to the player."""
        try:
            if colour.lower() == self._colours[0]:  # If player = white.
                self.playercolour, self.computercolour = self._colours
            elif colour.lower() == self._colours[1]:  # If player = black.
                self.playercolour, self.computercolour = self._colours[::-1]
            else:  # Not a valid colour specified.
                raise core.ColourError()
        except AttributeError:
            raise TypeError("To set player colour you must pass a string.")
        return self

    def positiononboard(self, position):
        """Returns boolean depending on if the position is on the board."""
        pos = core.Position(position)
        return 0 <= pos.index <= 63


class ChessBoard(_ChessBoardCore):
    """The public class that is the chessboard.

    This class creates a chessboard, much like you have a physical board when
    you play chess. It is a pretty dumb class however; it doesn't have many
    checks in place for moves and it can't do anything special like make moves.
    """

    def setupnormalboard(self):
        """Set up the chess board by placing the pieces at the correct spots."""
        backline = [
            pieces.RookPiece, pieces.KnightPiece, pieces.BishopPiece,
            pieces.QueenPiece, pieces.KingPiece, pieces.BishopPiece,
            pieces.KnightPiece, pieces.RookPiece
        ]

        # Add the white pieces.
        for index in range(0, 7+1):
            self._board[index] = backline[index](colour='white')
        for index in range(8, 15+1):
            self._board[index] = pieces.PawnPiece(colour='white')

        # Add the black pieces.
        for index in range(48,55+1):
            self._board[index] = pieces.PawnPiece(colour='black')
        for index in range(56, 63+1):
            self._board[index] = backline[index-56](colour='black')
        return None

    def setenpassantfor(self, colour, whichfile):
        """Sets enpassant for a colour"""
        if colour not in core.COLOURS:
            raise core.ColourError()

        if core.xnor(colour == 'white', self.playercolour == 'white'):
            self.enpassantforplayer = whichfile
        else:
            self.enpassantforcomputer = whichfile
        return None

    def move(self, startpos, endpos, force=True):
        """A clean way of moving pieces around on the board."""
        # Get start and end positions.
        start, end = core.Position(startpos), core.Position(endpos)
        if start == end:
            raise IndexError("The start and end points must be different.")

        # Check that start position has a piece on it.
        if self._board[start.index] == None:
            raise core.IllegalMoveError("There is no piece at %s" % start.coordinate)

        # See if en passant is in play.
        # REVIEW: Should the board handle this or the 'brain'?
        if (
            (self._board[start.index].type == pieces.PawnPiece)  # Is pawn and...
            and (start.coordinate[0] == 1 or start.coordinate[0] == 6)
            and (abs(start.coordinate[0] - end.coordinate[0]) == 2)  # ..is pushing
            ):
            self.setenpassantfor(
                core.oppositecolour(self._board[start.index].colour),
                start.coordinate[1])

        # Finally alter the board state.
        self._board[end.index] = self._board[start.index]
        self._board[start.index] = None
        return None

    def promotepawn(self, pos, promoteto):
        """Promotes a pawn at position specified."""
        position = core.Position(pos)
        pawnpiece = self._board[position.index]
        if pawnpiece == None:
            raise IndexError("There is no piece at %i" % pos.index)
        else:
            colour = pawnpiece.colour
            self._board[position] = promoteto(colour)
        return None
