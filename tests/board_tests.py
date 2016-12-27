# DESCRIPTION: Contains all of the unit tests for the chess board.

# 4920646f6e5c2774206361726520696620697420776f726b73206f6e20796f7572206d61636869
# 6e652120576520617265206e6f74207368697070696e6720796f7572206d616368696e6521

# DEVELOPMENT LOG:
#    20/11/16: Initialized testing script. Added core unittests for the chess
# board. Initialised a semi-integrated testing suite for a short game.
#    26/12/16: Fixed script to obey 80 character limit. Abstracted the tests
# in order to randomly certain squares.

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
class TestBoard(unittest.TestCase):
    """A basic testing suite the pertains to only the most basic of calls."""

    def setUp(self):
        """Initialise the board."""
        self.board = core.ChessBoard()
        self.startpos = randint(0, 63)  # Pick a position on the board to test.
        self.startcoord = (self.startpos / 8, self.startpos % 8)
        self.piece = 'X'
        self.board._ChessBoard__board[self.startpos] = self.piece  # Insert piece manually.

        self.errormessage = " PIECE INDEX: %i" % self.startpos
        return None

    def tearDown(self):
        """Destroy the tainted board. An extra procaution."""
        self.board = None
        return None

    def test_read_position_singleindex(self):
        self.assertEqual(
            self.board[self.startpos], self.piece,
            "Couldn't read the board using a single index." + self.errormessage
        )
        return None

    def test_read_position_coordinate(self):
        self.assertEqual(
            self.board[self.startcoord], self.piece,
            "Couldn't read the board using matrix notation." + self.errormessage
        )

        self.assertEqual(
            self.board[self.startcoord[0], self.startcoord[1]], self.piece,
            "Couldn't read the board using 2 integers separated by a comma." + \
            self.errormessage
        )
        return None

    def test_checkoccupacy(self):
        self.assertTrue(
            self.board.isoccupied(self.startpos),
            'The square should be occupied.' + self.errormessage
        )
        return None

    def test_addpiece(self):
        pos2 = randint(0, 63)
        if pos2 == self.startpos:  # Fix the ineviatble clash of indicies.
            pos2 = (pos2 + 1) % 63
        self.board.addpiece('Y', pos2)

        self.assertEqual(
            self.board._ChessBoard__board[pos2], 'Y',  # Don't use __getitem__ method.
            "The piece wasn't added correctly."
        )
        return None

    def test_removepiece(self):
        pos2 = 22
        if pos2 == self.startpos:  # Fix the ineviatble clash of indicies.
            pos2 += 1

        self.board._ChessBoard__board[pos2] = 'Z'  # Manually insert.
        self.board.removepiece(pos2)  # Remove using method under test.
        self.assertIs(
            self.board._ChessBoard__board[pos2], None,
            'The piece was not removed correctly.' + self.errormessage
        )

    def test_movepiece(self):
        self.board.move(
            self.startpos, (self.startpos + 1) % 63  # Avoid index>63
        )
        # Check piece isn't in old positon.
        self.assertEqual(
            self.board._ChessBoard__board[self.startpos], None,
            "The piece remains in its old spot." + self.errormessage
        )
        # Check piece is in new postion.
        self.assertEqual(
            self.board._ChessBoard__board[(self.startpos+1) % 63], self.piece,
            "The piece should have moved, but it didn't."
        )


class TestBasicGame(unittest.TestCase):
    """A slightly more involved test, involving some dependancy on the already
    tested methods. Plays through a simple, short game and checks to see if all
    the results are completed."""
    # TODO: This test suite.

    def setUp(self):
        """Initialise the board."""
        self.board = core.ChessBoard()
        return None

    def tearDown(self):
        """Destroy the tainted board."""
        self.board = None
        return None
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.:.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~FINAL EXECUTION~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':
    unittest.main(verbosity=2)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.:.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
