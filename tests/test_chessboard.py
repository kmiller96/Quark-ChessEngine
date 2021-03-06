# DESCRIPTION: Tests the chessboard.

# 4920646f6e5c2774206361726520696620697420776f726b73206f6e20796f7572206d61636869
# 6e652120576520617265206e6f74207368697070696e6720796f7572206d616368696e6521

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import unittest
from tests.test_core import errormessage
from lib import chessboard, core, pieces

class CoreMethods(unittest.TestCase):
    """This testing suite looks at the core methods."""

    def setUp(self):
        self.board = chessboard._ChessBoardCore()
        return None

    def test__getitem__index(self):
        self.board._board[19] = 'X'  # Inject a piece at 19

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

    def test__getitem__badinput(self):
        with self.assertRaises(TypeError):  # String input
            self.board['string']
        with self.assertRaises(TypeError):  # Float input
            self.board[10.5]
        with self.assertRaises(TypeError):  # Too many elements
            self.board[[1, 4, 5]]
        with self.assertRaises(TypeError):  # Too few elements
            self.board[(1,)]
        with self.assertRaises(IndexError):  # Off the board.
            self.board[91]
        return None

    def test__setitem__index(self):
        piece = pieces.KingPiece('white')
        self.board[36] = piece

        self.assertEqual(
            self.board._board[36], piece,
            errormessage(self.board._board[36], piece))
        return None

    def test__setitem__coordinate(self):
        piece = pieces.BishopPiece('white')
        self.board[(2, 1)] = piece

        self.assertEqual(
            self.board._board[17], piece,
            errormessage(self.board._board[17], piece))
        return None

    def test__setitem__vector(self):
        piece = pieces.QueenPiece('white')
        self.board[core.Vector(6, 6)] = piece

        self.assertEqual(
            self.board._board[54], piece,
            errormessage(self.board._board[54], piece))
        return None

    def test__setitem__nonpiece(self):
        piece = 'X'  # Not a pieces.py piece.
        with self.assertRaises(TypeError):
            self.board[19] = piece
        return None

    def test__setitem__badposition(self):
        piece = pieces.KnightPiece('black')
        with self.assertRaises(TypeError):  # String input
            self.board['string'] = piece
        with self.assertRaises(TypeError):  # Float input
            self.board[10.5] = piece
        with self.assertRaises(TypeError):  # Too many elements
            self.board[[1, 4, 5]] = piece
        with self.assertRaises(TypeError):  # Too few elements
            self.board[(1,)] = piece
        with self.assertRaises(IndexError):  # Off the board.
            self.board[91] = piece
        return None

    @unittest.skip("Test not written yet.")
    def test_iter(self):
        # TODO: How do I test this?
        return None

    def test_duplicateboard(self):
        piece = pieces.QueenPiece('black')
        self.board[11] = piece

        newboard = self.board.duplicateboard()
        self.board[12] = piece

        self.assertNotEqual(
            newboard[12], self.board[12],
            errormessage(
                '%s == %s' % (newboard[12], self.board[12]),
                '%s =/= %s' % (newboard[12], self.board[12])))
        self.assertEqual(
            newboard[11], self.board[11],
            errormessage(
                '%s =/= %s' % (newboard[11], self.board[11]),
                '%s == %s' % (newboard[11], self.board[11])))
        return None

    def test_setplayercolour_white(self):
        self.board.setplayercolour('white')
        self.assertEqual(
            self.board.playercolour, 'white',
            errormessage(self.board.playercolour, 'white'))
        self.assertEqual(
            self.board.computercolour, 'black',
            errormessage(self.board.computercolour, 'black'))
        return None

    def test_setplayercolour_black(self):
        self.board.setplayercolour('black')
        self.assertEqual(
            self.board.playercolour, 'black',
            errormessage(self.board.playercolour, 'black'))
        self.assertEqual(
            self.board.computercolour, 'white',
            errormessage(self.board.computercolour, 'white'))
        return None

    def test_setplayercolour_badinput(self):
        with self.assertRaises(NameError):
            self.board.setplayercolour('blue')
        with self.assertRaises(TypeError):
            self.board.setplayercolour([22, 14])
        return None

    def test_playercolour(self):
        self.board.setplayercolour('white')
        self.assertEqual(self.board.playercolour, 'white')
        self.assertEqual(self.board.computercolour, 'black')

        self.board.setplayercolour('black')
        self.assertEqual(self.board.playercolour, 'black')
        self.assertEqual(self.board.computercolour, 'white')

    def test_positiononboard(self):
        pos = core.Position(11)
        index = pos.index
        coordinate = pos.coordinate
        vector = pos.vector

        self.assertTrue(self.board.positiononboard(index))
        self.assertTrue(self.board.positiononboard(coordinate))
        self.assertTrue(self.board.positiononboard(vector))
        return None

    def test_positiononboard_string(self):
        with self.assertRaises(TypeError):
            self.board.positiononboard('hello there')
        return None

    def test_positiononboard_float(self):
        with self.assertRaises(TypeError):
            self.board.positiononboard(12.1)
        return None

class TestChessBoard(unittest.TestCase):
    """These tests are for the more exciting calls."""

    def setUp(self):
        self.board = chessboard.ChessBoard()
        return None

    def test_findpiece_white(self):
        self.board[25] = pieces.KingPiece('white')

        whitekingpos = self.board.findpiece(pieces.KingPiece, 'white')[0]
        self.assertEqual(
            whitekingpos, 25,
            errormessage(
                "The king is at %i" % whitekingpos, "The king is at %i" % 25))
        return None

    def test_findpiece_black(self):
        self.board[22] = pieces.KingPiece('black')

        blackkingpos = self.board.findpiece(pieces.KingPiece, 'black')[0]
        self.assertEqual(
            blackkingpos, 22,
            errormessage(
                "The king is at %i" % blackkingpos, "The king is at %i" % 22))
        return None

    def test_findpiece_nopieces(self):
        self.assertFalse(self.board.findpiece(pieces.KnightPiece, 'white'))
        return None

    @unittest.skip("Currently under refactoring.")
    def test_enpassant(self):
        self.board[51] = pieces.PawnPiece('black')
        self.board.move(51, 35)
        self.assertTrue(self.board.enpassantforplayer != None)

if __name__ == '__main__':
    unittest.main(verbosity=2)
