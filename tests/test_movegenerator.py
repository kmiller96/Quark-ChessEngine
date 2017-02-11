# DESCRIPTION: Tests the move generator.

# 4920646f6e5c2774206361726520696620697420776f726b73206f6e20796f7572206d61636869
# 6e652120576520617265206e6f74207368697070696e6720796f7572206d616368696e6521

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import unittest
from lib import core, chessboard, pieces, movegenerator
from tests.test_core import errormessage

class TestCoreMoveGenerator(unittest.TestCase):
    """Goes about testing the core methods of the move generator."""

    def setUp(self):
        self.board = chessboard.ChessBoard()
        self.board[18] = pieces.QueenPiece('white')
        self.board[19] = pieces.PawnPiece('white')
        self.board[23] = pieces.RookPiece('black')
        self.board[42] = pieces.KnightPiece('black')

        self.generator = movegenerator._CoreMoveGenerator(self.board)

    def test_piecesareonsameside_white(self):
        self.assertTrue(
            self.generator._piecesareonsameside(self.board[18], self.board[19]),
            errormessage(False, True)
        )
        return None

    def test_piecesareonsameside_black(self):
        self.assertTrue(
            self.generator._piecesareonsameside(self.board[23], self.board[42]),
            errormessage(False, True)
        )
        return None

    def test_piecesareonsameside_bothcolours(self):
        self.assertFalse(
            self.generator._piecesareonsameside(self.board[18], self.board[23]),
            errormessage(True, False)
        )
        return None

    def test_piecesareonsameside_nonpieces(self):
        with self.assertRaises(TypeError):
            self.generator._piecesareonsameside(12, 15)
        return None

    def test_piecesbetween_onepiece(self):
        self.assertEqual(
            len(self.generator._piecesbetween(18, 23)), 1,
            errormessage(
            '%s pieces' % len(self.generator._piecesbetween(18, 23)),
            '1 piece'
            )
        )
        return None

    def test_piecesbetween_twopieces(self):
        self.assertEqual(
            len(self.generator._piecesbetween(16, 23)), 2,
            errormessage(
            '%s piece(s)' % len(self.generator._piecesbetween(16, 23)),
            '2 pieces'
            )
        )
        return None

    def test_piecesbetween_inclusive(self):
        self.assertEqual(
            len(self.generator._piecesbetween(18, 19, inclusive=True)), 2,
            errormessage(
            '%s piece(s)' % len(self.generator._piecesbetween(18, 19, inclusive=True)),
            '2 pieces'
            )
        )
        return None

    def test_piecesbetween_nonpositions(self):
        with self.assertRaises(TypeError):
            self.generator._piecesbetween('string', 'pie')
        return None

    def test_piecesbetween_offboard(self):
        with self.assertRaises(IndexError):
            self.generator._piecesbetween((10, 10), (1, 1))
        return None

    def test_piecesbetween_weirdvector(self):
        with self.assertRaises(core.BadVectorError):
            self.generator._piecesbetween(28, 45)

    def test_kingincheck_true(self):
        self.generator.board[34] = pieces.KingPiece('black')  # Add black king.
        self.assertTrue(
            self.generator.kingincheck('black'))
        return None

    def test_kingincheck_false(self):
        self.generator.board[1] = pieces.KingPiece('black')
        self.assertFalse(
            self.generator.kingincheck('black'))


class BasicMoveTests(unittest.TestCase):
    """A testing suite for only basic moves."""

    def setUp(self):
        self.board = chessboard.ChessBoard()
        self.board[18] = pieces.QueenPiece('white')
        self.board[19] = pieces.PawnPiece('white')
        self.board[23] = pieces.RookPiece('black')
        self.board[42] = pieces.KnightPiece('black')

        self.generator = movegenerator.MoveGenerator(self.board)

    def test_basicmoves_white(self):
        movelist = self.generator._basicmoves('white')

        # Make sure queen can't jump over white pawn.
        self.assertNotIn(
            (18, 19), movelist,
            errormessage('Can capture white pawn', "Can't capture white pawn"))
        self.assertNotIn(
            (18, 20), movelist,
            errormessage('Can move over pawn', 'Blocked by white pawn'))

        # Make sure queen can't move past knight at 42.
        self.assertIn(
            (18, 42), movelist,
            errormessage("Can't capture knight", 'Can capture black knight'))
        self.assertNotIn(
            (18, 50), movelist,
            errormessage('Can move past black knight', 'Blocked by knight'))

    def test_basicmoves_white(self):
        movelist = self.generator._basicmoves('white')

        # Make sure queen can't jump over white pawn.
        self.assertNotIn(
            (18, 19), movelist,
            errormessage('Can capture white pawn', "Can't capture white pawn"))
        self.assertNotIn(
            (18, 20), movelist,
            errormessage('Can move over pawn', 'Blocked by white pawn'))

        # Make sure queen can't move past knight at 42.
        self.assertIn(
            (18, 42), movelist,
            errormessage("Can't capture knight", 'Can capture black knight'))
        self.assertNotIn(
            (18, 50), movelist,
            errormessage('Can move past black knight', 'Blocked by knight'))

    def test_basicmoves_wrongcolour(self):
        with self.assertRaises(core.ColourError):
            self.generator._basicmoves(10)
        with self.assertRaises(core.ColourError):
            self.generator._basicmoves('while')
        return None


class AdvancedMoveTests(unittest.TestCase):
    """These tests are for the more advanced situations, like castling and check."""

    def setUp(self):
        self.board = chessboard.ChessBoard()
        self.board[0] = pieces.RookPiece('white')
        self.board[4] = pieces.KingPiece('white')
        self.board[13] = pieces.PawnPiece('white')
        self.board[31] = pieces.BishopPiece('black')
        self.board[58] = pieces.RookPiece('black')

        self.generator = movegenerator.MoveGenerator(self.board)
        return None

    def test_allpossiblemoves_white(self):
        movelist = self.generator.generatemovelist('white')
        self.assertIn(
            ((4, 2), (0, 3)), movelist
        )
        return None


if __name__ == '__main__':
    unittest.main(verbosity=2)
