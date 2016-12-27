# DESCRIPTION: Contains all of the unit tests for the chess pieces.

# 4920646f6e5c2774206361726520696620697420776f726b73206f6e20796f7572206d61636869
# 6e652120576520617265206e6f74207368697070696e6720796f7572206d616368696e6521

# DEVELOPMENT LOG:
#    27/12/16:Initialized the testing suite.

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
        self.piece = core.BasePiece()
        self.piece._postion = randint(0, 63)
        return None

    def tearDown(self):
        self.piece = None
        return None

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

    def test_move(self):
        self.piece.move(10)  # WARNING: Magic number.
        self.assertEqual(
            self.piece._postion, 10,
            "The piece didn't move to where it was asked."
        )
        return None


class TestRookPiece(unittest.TestCase):
    """Tests the behaviour of the rook piece."""

    def setUp(self):
        self.piece = core.RookPiece()
        self.piece._postion = 28  # WARNING: Magic number.
        return None

    def tearDown(self):
        self.piece = None
        return None

    def test_isvalidmove(self):
        # TODO: Make all of these tests not hardcoded in.
        self.assertTrue(self.piece.isvalidmove(36))
        self.assertTrue(self.piece.isvalidmove(20))
        self.assertTrue(self.piece.isvalidmove(29))
        self.assertTrue(self.piece.isvalidmove(24))

        self.assertFalse(self.piece.isvalidmove(37))
        self.assertFalse(self.piece.isvalidmove(56))
        self.assertFalse(self.piece.isvalidmove(11))
        return None
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.:.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~FINAL EXECUTION~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':
    unittest.main(verbosity=2)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.:.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
