# DESCRIPTION: Contains all of the code, classes and functions corresponding to the board and pieces.

# 50726f6772616d6d696e6720697320627265616b696e67206f66206f6e652062696720696d706f737369626c65207461736b20696e746f20736576
# 6572616c207665727920736d616c6c20706f737369626c65207461736b732e

# EXPLAINATION:
# The board works by allocating an index to each square, starting at the bottom left and moving right. Thus the white
# left rook is at index 0, the white king is at index 4 and the black queen at index 59.

# DEVELOPMENT LOG:
#    19/11/16: Initialized core file.

# NOTES:
# The board should have its internal structure (i.e. the locations) completely unaccessable from outside observers.

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MAIN~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import sys

class ChessBoard:
    """Creates the chess board."""

    def __init__(self):
        """Initialises the board."""
        self.__board = [None] * 64
        self.playerturn = True

    @staticmethod
    def assertIndexOnBoard(indices, message):
        """Assert that the indices called are on the board. Used as a sanity check."""
        if message is None:
            message = "Index is out the the board range."
        for ii in indices:
            assert 0 <= ii <= 63, message
        return None

    def isoccupied(self, index):
        """Checks to see if the square is occupied."""
        self.assertIndexOnBoard(index)
        if self.__board[index] != None:
            return True
        else:
            return False

    def assertIsUnoccupied(self, index, message=None):
        """Asserts that the square is unoccupied. Acts differently then isoccupied."""
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
    """The parent class for the chess pieces."""

    def __init__(self):
        return None
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.:.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

