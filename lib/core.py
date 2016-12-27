# DESCRIPTION: Contains all of the code, classes and functions corresponding to
# the board and pieces.

# 50726f6772616d6d696e6720697320627265616b696e67206f66206f6e652062696720696d706f
# 737369626c65207461736b20696e746f207365766572616c207665727920736d616c6c20706f73
# 7369626c65207461736b732e

# EXPLAINATION:
# The board works by allocating an index to each square, starting at the bottom
# left and moving right. Thus the white left rook is at index 0, the white king
# is at index 4 and the black queen at index 59.

# DEVELOPMENT LOG:
#    19/11/16: Initialized core file. Added core functionallity such as sanity
# checks, add/remove/move methods.
#    20/11/16: Added a getitem method.
#    26/12/16: Fixed line length so that it corresponded to PEP8 guidlines.
# Revisited the project, conducting some cleaning while I was in.
#    27/12/16: Added some framework for the backline pieces.

# NOTES:
# The board should have its internal structure (i.e. the locations) completely
# unaccessable from outside observers.

# TODO:
# - Check to see if pieces between start and final destination when moving.

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MAIN~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ChessBoard:
    """Creates a chess board."""

    def __init__(self):
        """Initialises the board."""
        self.__board = [None] * 64
        self.playerturn = True

    def __getitem__(self, pos):
        """Controls calling the piece at a position on the board.

        The structure in doing this is two fold. One way is to simply call an
        index of 0 to 63 corresponding to that square. The second way is to call
        a row then a column with the bottom right positon being 0 and increasing
        as you go right. E.g. a call of (1,3) will give the second row (b rank)
        and the fourth column (4th file) and as a result if effectively the same
        as calling 11.
        """
        # TO-DO: It is better to beg for forgiveness then to ask for permission;
        # Add a try-exception statement here.

        self.assertIndexOnBoard(pos)
        if isinstance(pos, int):
            return self.__board[pos]
        elif isinstance(pos, (list, tuple)) and len(pos) == 2:
            return self.__board[8*pos[0] + pos[1]]
        else:
            raise TypeError, "The board is read either as a index from 0 to " \
            "63 or a tuple that specifies the row and column index."

    @staticmethod
    def assertIndexOnBoard(indices):
        """Assert that the indices called are on the board as a sanity check."""
        if isinstance(indices, (list, tuple)):
            for ii in indices:
                assert isinstance(ii, int), "The value(s) passed are not integers"
                assert 0 <= ii <= 63, "Index is out the the board range."
        elif isinstance(indices, int):
            assert 0 <= indices <= 63, "The value(s) passed are not integers"
        return None

    def isoccupied(self, index):
        """Checks to see if the square is occupied."""
        self.assertIndexOnBoard(index)
        if self.__board[index] != None:
            return True
        else:
            return False

    def assertIsUnoccupied(self, index, message=None):
        """Asserts that the square is free and unoccupied.

        Note that this is different to the method 'isoccupied' since it is
        purely an assertion and doesn't return a True or False.
        """
        self.assertIndexOnBoard(index)
        if message is None:
            message = "The target square is occupied."
        assert self.__board[index] == None, message
        return None


    def move(self, startindex, endindex):
        """Move a piece around on the board."""
        self.assertIndexOnBoard((startindex, endindex))
        self.assertIsUnoccupied(endindex, 'The end square is occupied.')
        self.__board[endindex] = self.__board[startindex]
        self.__board[startindex] = None
        return None

    def addpiece(self, piece, index):
        """Add a new piece to the board."""
        self.assertIndexOnBoard(index)
        self.assertIsUnoccupied(index)
        self.__board[index] = piece
        return None

    def removepiece(self, index):
        """Removes a piece from the board."""
        self.assertIndexOnBoard(index)
        self.__board[index] = None


class BasePiece:
    """The class all chess pieces inherit from."""

    def __init__(self):
        self._postion = None
        return None

    def isvalidmove(self):
        """Placeholder method used to check if the move is valid for a specific
        piece."""
        pass

    def postion(self):
        """Returns the position of the piece."""
        return self._postion

    def move(self, index):
        """Moves the piece to new index."""
        self._postion = index
        return None


class RookPiece(BasePiece):
    """The class for the Rook."""

    def __init__(self):
        BasePiece.__init__(self)
        return None

    def isvalidmove(self, movetopos):
        """Checks that the move specified is valid."""
        movediff = abs(movetopos - self._postion)
        if movediff % 8 == 0:  # If moving up or down:
            return True  # This is always true.
        elif movediff % 8 != 0:  # If moving side-to-side:
            if movediff/8 == 0: # Make sure not moving up or down.
                return True
        else:
            return False


class KnightPiece(BasePiece):
    """The class for the knight."""

    def __init__(self):
        BasePiece.__init__(self)
        return None

    def isvalidmove(self, movetopos):
        """Checks that the move specified is valid."""
        movediff = abs(movetopos - self._postion)
        if movediff in (6, 10, 15, 17):  # Valid move differences.
            return True
        else:
            return False


class BishopPiece(BasePiece):
    """The class for the bishop."""

    def __init__(self):
        BasePiece.__init__(self)
        return None

    def isvalidmove(self, movetopos):
        """Checks that the move specified is valid."""
        movediff = abs(movetopos - self._postion)
        if movediff in (7, 9):  # Valid move differences.
            return True
        else:
            return False
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.:.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
