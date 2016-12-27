# DESCRIPTION: Contains all of the unit tests for the chess pieces.

# 4920646f6e5c2774206361726520696620697420776f726b73206f6e20796f7572206d61636869
# 6e652120576520617265206e6f74207368697070696e6720796f7572206d616368696e6521

# DEVELOPMENT LOG:
#    27/12/16: Initialized the testing suite. Added tests for the BasePiece and
# all of its children (the backline of the board).

# TESTING REQUIREMENTS:
# This is the description of what needs to be tested in order to deem the
# program robust.


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~IMPORTS/GLOBALS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from time import time
import unittest
from random import randint
from lib import core
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.:.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~TESTING~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class TestBasePiece(unittest.TestCase):
    """Tests the behaviour of the basic piece."""

    def setUp(self):
        self.piece = core.BasePiece(randint(0, 63))
        return None

    def tearDown(self):
        self.piece = None
        return None

    def test_isvalidindex(self, ii):
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
        self.piece = core.KingPiece(randint(0, 63))
        return None

    def test_kinggoodmove(self):
        # TODO: This method.
        return None

    def test_kingbadmove(self):
        # TODO: This method.
        return None


class TestQueenPiece(TestBasePiece):
    """Conducts basic unittests on the Queen."""

    def setUp(self):
        self.piece = core.QueenPiece(randint(0, 63))
        return None

    def test_queengoodmove(self):
        # TODO: This method.
        return None

    def test_queenbadmove(self):
        # TODO: This method.
        return None


class TestBishopPiece(TestBasePiece):
    """What do these tests pertain to?"""

    def setUp(self):
        self.piece = core.BishopPiece(randint(0, 63))
        return None

    def test_bishopgoodmove(self):
        # TODO: This method.
        return None

    def test_bishopbadmove(self):
        # TODO: This method.
        return None


class TestKnightPiece(TestBasePiece):
    """What do these tests pertain to?"""

    def setUp(self):
        self.piece = core.KnightPiece(randint(0, 63))
        return None

    def test_knightgoodmove(self):
        # TODO: This method.
        return None

    def test_knightbadmove(self):
        # TODO: This method.
        return None


class TestRookPiece(TestBasePiece):
    """Tests the behaviour of the rook piece."""

    def setUp(self):
        self.piece = core.RookPiece(randint(9, 54))
        return None

    def test_isvalidmove(self):
        # TODO: Make all of these tests not hardcoded in.
        originalpos = self.piece._postion
        self.assertTrue(self.piece.isvalidmove(originalpos + 8))  # Move up.
        self.assertTrue(self.piece.isvalidmove(originalpos - 8))  # Move down.
        self.assertTrue(self.piece.isvalidmove(originalpos - 1))  # Move left.
        self.assertTrue(self.piece.isvalidmove(originalpos + 1))  # Move right.

        self.assertFalse(self.piece.isvalidmove(originalpos + 9))
        self.assertFalse(self.piece.isvalidmove(originalpos + 6))
        self.assertFalse(self.piece.isvalidmove(originalpos - 20))
        return None
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.:.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~FINAL EXECUTION~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':
    unittest.main(verbosity=2)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.:.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
