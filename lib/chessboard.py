# DESCRIPTION: Contains all of the code, classes and functions corresponding to
# the board.

# 50726f6772616d6d696e6720697320627265616b696e67206f66206f6e652062696720696d706f
# 737369626c65207461736b20696e746f207365766572616c207665727920736d616c6c20706f73
# 7369626c65207461736b732e

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

    def _equality(self, other):
        """Handles the equality of two chessboards."""
        return self._board == other._board

    def __eq__(self, other):
        try:
            return self._equality(other)
        except AttributeError:
            if other == None: return False
            else: raise TypeError("Other must be chessboard.")

    def __ne__(self, other):
        try:
            return not self._equality(other)
        except AttributeError:
            if other == None: return True
            else: raise TypeError("Other must be chessboard.")

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
        try:
            pos = core.convert(position, tocoordinate=True)
        except TypeError:
            raise TypeError("Position must be an index, coordinate or vector.")
        else:
            return (0 <= pos[0] <= 7 and 0 <= pos[1] <= 7)

    def assertPositionOnBoard(self, position):
        """Asserts that the position is valid."""
        try:
            index = core.convert(position, toindex=True)
            self._board[index]
        except IndexError:  # If off board.
            raise AssertionError("The position %r is off the board." % position)
        return None

    def assertIsUnoccupied(self, position):
        """Asserts that the square is free and unoccupied."""
        try:
            index = core.convert(position, toindex=True)
            assert self._board[index] == None, "The target square is occupied."
        except IndexError:
            raise IndexError("The index used is off the board!")
        return None

    def assertIsOccupied(self, position):
        """Asserts that the square is occupied."""
        try:
            index = core.convert(position, toindex=True)
            assert self._board[index] != None
        except IndexError:
            raise IndexError("The index used is off the board!")
        except AssertionError:
            raise core.EmptySquareError(position)
        return None

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

    def setenpassantfor(self, colour, whichfile):
        """Sets enpassant for a colour"""
        if colour not in ('white', 'black'):
            raise core.ColourError()

        if core.xnor(colour == 'white', self.playercolour == 'white'):
            self.enpassantforplayer = whichfile
        else:
            self.enpassantforcomputer = whichfile
        return None

    def move(self, startpos, endpos, force=True):
        """A clean way of moving pieces around on the board."""
        # Sanity checks and assertions.
        assert startpos != endpos, \
            "To move the piece, the start and end points must be different."
        start = core.Position(startpos)
        end = core.Position(endpos)
        self.assertPositionOnBoard(start.index)
        self.assertPositionOnBoard(end.index)
        self.assertIsOccupied(start.index)
        if not force: self.assertIsUnoccupied(end.index)

        # See if en passant is in play.
        if (
            (self._board[start.index].type == pieces.PawnPiece)  # Is pawn and...
            and (start.coordinate[0] == 1 or start.coordinate[0] == 6)
            and (abs(start.coordinate[0] - end.coordinate[0]) == 2)  # ..is pushing
            ):
            self.setenpassantfor(
                core.oppositecolour(self._board[start.index].colour),
                start.coordinate[1])

        # Movement code.
        if start.index == end.index:
            return None  # HACK: Prevents deleting the piece from the board.
        self._board[end.index] = self._board[start.index]
        self._board[start.index] = None
        return None

    def promotepawn(self, position, promoteto):
        """Promotes a pawn at position specified."""
        position = core.convert(position, toindex=True)
        pawnpiece = self._board[position]
        colour = pawnpiece.colour
        self._board[position] = promoteto(colour)
        return None
