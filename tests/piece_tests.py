# DESCRIPTION: Contains all of the unit tests for the chess pieces.

# 4920646f6e5c2774206361726520696620697420776f726b73206f6e20796f7572206d61636869
# 6e652120576520617265206e6f74207368697070696e6720796f7572206d616368696e6521

# DEVELOPMENT LOG:
#    27/12/16: Initialized the testing suite. Added tests for the BasePiece and
# all of its children (the backline of the board).
#    28/12/16: Fixed wrong number of arguements raised when calling the method
# isvalidindex. Fix possible starting position for the rook such that the tests
# will always be either true or false. Before, sometimes an index was chosen on
# the edge of the board and a true test would fail in the direction the edge was
# on.
#    29/12/16: Added tests for good moves and bad moves on each piece. Did some
# refactoring to clean up testing suites.


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~IMPORTS/GLOBALS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from time import time
import unittest
from random import randint, choice
from lib import core
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.:.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~TESTING~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class TestBasePiece(unittest.TestCase):
    """Tests the behaviour of the basic piece."""

    @staticmethod
    def _flatten(l):
        """A hack used to flatten lists."""
        return [item for sublist in l for item in sublist]

    def innersquares(self):
        """Gives only the squares at least one square away from the edge."""
        possible_positions = [
            range(9, 14+1),
            range(17, 22+1),
            range(25, 30+1),
            range(33, 38+1),
            range(41, 46+1),
            range(49, 54+1)
        ]  # All squares that aren't on the edge.
        # Now turn list of lists into 1D array of possible positions:
        return self._flatten(possible_positions)

    def assertthatmoveis(self, TrueorFalse, movelist):
        """A shorthand for assertTrue(ismovevalid(..)) check for a list of
        moves."""
        originalpos = self.piece._postion
        isvalidmove = self.piece.isvalidmove

        message = lambda x: "Moving %i squares from %i should yield %s" % \
        (x, originalpos, str(TrueorFalse))

        if TrueorFalse is True:
            for move in movelist:
                self.assertTrue(isvalidmove(originalpos + move), message(move))
        elif TrueorFalse is False:
            for move in movelist:
                self.assertFalse(isvalidmove(originalpos + move), message(move))
        else:
            raise TypeError("The first arguement must be True or False.")
        return None

    def setUp(self):
        self.piece = core.BasePiece(
            startpositionindex=choice(self.innersquares()),
            validmoves=(1,)
        )
        return None

    def tearDown(self):
        self.piece = None
        return None

    def test_isvalidindex(self):
        func = self.piece.isvalidindex

        self.assertTrue(func(randint(0, 63)), "False under correct index.")
        self.assertFalse(func(-12), "True when negative value.")
        self.assertFalse(func(67), "True when index >63.")
        self.assertRaises(TypeError, func, 'string', "A string passed through.")
        self.assertRaises(TypeError, func, 23.1, "A float passed through.")

    def test_positionmethod(self):
        self.assertEqual(
            self.piece.postion(), self.piece._postion,
            "The method 'postion' does not return expected values."
        )
        self.assertNotEqual(
            self.piece.postion(), self.piece._postion + 1,
            "The method returned true when it should have been false."
        )
        return None

    def test_moveoffboard(self):
        self.assertRaises(
            IndexError,
            self.piece.move, 65
        )
        return None


class TestKingPiece(TestBasePiece):
    """Conduct basic unittests on the King."""

    def setUp(self):
        self.piece = core.KingPiece(choice(self.innersquares()))
        return None

    def test_kinggoodmove(self):
        self.assertthatmoveis(True,
            (8, -8, 1, -1,  # Move forward, backward, left, right.
             9, -9, 7, -7)  # Move NE, SW, NW, SE.
        )
        return None

    def test_kingbadmove(self):
        self.assertthatmoveis(False,
            (22, -32, -10, 19)  # Bad moves.
        )
        return None


class TestQueenPiece(TestBasePiece):
    """Conducts basic unittests on the Queen."""

    def setUp(self):
        self.piece = core.QueenPiece(choice(self.innersquares()))
        return None

    def test_queengoodmove(self):
        self.assertthatmoveis(True,
            (8, -8, 1, -1, 9, -9, 7, -7)  # Move like King.
        )
        self.piece._postion = 27  # Dump the queen in the middle of the board.
        self.assertthatmoveis(True,
            (8*2, -8*3, 1*4, -1*2, 9*3, -9*2, 7*2, -7*3)  # Move multiple squares.
        )
        return None

    def test_queenbadmove(self):
        self.assertthatmoveis(False,
            (10, -15, -22, 12)  # Check moves that should never work.
        )
        self.piece._postion = 27  # Move queen to check knight-like moves.
        self.assertthatmoveis(False,
            (6, -6)  # Knight-like moves that might be valid in certain positions.
        )
        return None


class TestBishopPiece(TestBasePiece):
    """What do these tests pertain to?"""

    def setUp(self):
        self.piece = core.BishopPiece(choice(self.innersquares()))
        return None

    def test_bishopgoodmove(self):
        self.assertthatmoveis(True,
            (7, -7, 9, -9,  # 1-square bishop moves.
             14, -14, 18, -18,  # 2-square bishop moves.
             21, -21, 27, -27)  # 3-square bishop moves.
        )
        return None

    def test_bishopbadmove(self):
        self.assertthatmoveis(False,
            (8, 1, 10, -23)  # Bad bishop moves.
        )
        return None


class TestKnightPiece(TestBasePiece):
    """What do these tests pertain to?"""

    def setUp(self):
        self.piece = core.KnightPiece(choice(self.innersquares()))
        return None

    def test_knightgoodmove(self):
        self.assertthatmoveis(True,
            (6, -6, 10, -10, 15, -15, 17, -17)
        )
        return None

    def test_knightbadmove(self):
        self.assertthatmoveis(False,
            (8, 12, -3, 9, -7)
        )
        return None


class TestRookPiece(TestBasePiece):
    """Tests the behaviour of the rook piece."""

    def setUp(self):
        self.piece = core.RookPiece(choice(self.innersquares()))
        return None

    def test_isvalidmove(self):
        # TODO: Fix this method so that it is using the same style as the others.
        originalpos = self.piece._postion
        func = self.piece.isvalidmove
        self.assertTrue(func(originalpos + 8))  # Move up.
        self.assertTrue(func(originalpos - 8))  # Move down.
        self.assertTrue(func(originalpos - 1))  # Move left.
        self.assertTrue(func(originalpos + 1))  # Move right.

        self.assertFalse(func(originalpos + 9))
        self.assertFalse(func(originalpos - 20))

        # Move out of rank but less then 8 indicies.
        self.piece._postion = 15  # Rank 2, file H.
        self.assertFalse(func(self.piece._postion + 3))  # Rank 3, file C
        return None


class TestPawnPiece(TestBasePiece):
    """These tests are for the pawn pieces. Since this is one of the hardest
    pieces to code these tests are much tougher to pass."""

    def setUp(self):
        self.piece = core.PawnPiece(randint(8, 15))  # Only on second rank.
        return None

    def test_basicmove(self):
        self.assertthatmoveis(True,
            (8,)  # Move forward one square.
        )
        return None

    def test_pawnpush(self):
        self.assertthatmoveis(True,
            (16,)  # Pawn push.
        )
        self.piece.move(self.piece._postion + choice((8, 16)))
        self.assertthatmoveis(False,
            (16,)  # Make sure pawn can't push again.
        )
        return None

    def test_promotion(self):

        return None

    def test_capture(self):

        return None
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.:.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~FINAL EXECUTION~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':
    unittest.main(verbosity=2)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.:.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
