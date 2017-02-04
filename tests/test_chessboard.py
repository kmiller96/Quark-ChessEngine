# DESCRIPTION: Tests the chessboard.

# 4920646f6e5c2774206361726520696620697420776f726b73206f6e20796f7572206d61636869
# 6e652120576520617265206e6f74207368697070696e6720796f7572206d616368696e6521

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import unittest
from tests.test_core import errormessage
from lib import chessboard, core

class CoreMethods(unittest.TestCase):
    """This testing suite looks at the core methods."""

    def setUp(self):
        self.board = chessboard._ChessBoardCore()
        return None

    def test__getitem__index(self):
        self.board._board[19] = 'X'  # Inject a piece at 19
        self.board._board[23] = 'Y'  # Inject a piece at (2, 7)

        self.assertEqual(
            self.board[19], 'X',
            errormessage(self.board[19], 'X'))
        return None

    def test__getitem__coordinate(self):
        self.board._board[23] = 'Y'  # Inject a piece at (2, 7)
        self.assertEqual(
            self.board[(2, 7)], 'Y',
            errormessage(self.board[(2, 7)], 'Y'))
        return None

    def test__getitem__vector(self):
        self.board._board[0] = 'Z'  # Inject a piece at (0, 0)

        self.assertEqual(
            self.board[core.Vector(0, 0)], 'Z',
            errormessage(self.board[core.Vector(0, 0)], 'Z'))
        return None

if __name__ == '__main__':
    unittest.main(verbosity=2)
