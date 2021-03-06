# DESCRIPTION: Tests the piece classes.

# 4920646f6e5c2774206361726520696620697420776f726b73206f6e20796f7572206d61636869
# 6e652120576520617265206e6f74207368697070696e6720796f7572206d616368696e6521

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# REVIEW: This testing suite needs a serious review when I can be bothered.

import unittest
from lib import pieces, core
from tests.test_core import errormessage

class BasePieceCalls(unittest.TestCase):
    """Tests the base piece and its associated methods."""
    # TODO: Finish fleshing this out.

    def setUp(self):
        self.piece = pieces.BasePiece(
            'white', 'a', [core.Vector(0, 1)], crawler=True)
        return None

    def test_nonbooloncrawler(self):
        with self.assertRaises(TypeError):
            pieces.BasePiece(
            'white', 'a', [core.Vector(0, 1)], crawler=10
            )
        return None

    def test_colournotvalid(self):
        with self.assertRaises(TypeError):
            pieces.BasePiece(
            'w', 'a', [core.Vector(0, 1)], crawler=True)
        with self.assertRaises(TypeError):
            pieces.BasePiece(
            10, 'a', [core.Vector(0, 1)], crawler=True)
        with self.assertRaises(TypeError):
            pieces.BasePiece(
            int, 'a', [core.Vector(0, 1)], crawler=True)
        return None

    def test_colourrandomcapitalised(self):
        pieces.BasePiece('WhItE', 'a', [core.Vector(0, 1)], crawler=True)
        pieces.BasePiece('blACK', 'a', [core.Vector(0, 1)], crawler=True)
        return None

    def test_notationsymbol_white(self):
        self.assertEqual(
            self.piece.notationsymbol, 'A',
            errormessage(self.piece.notationsymbol, 'A')
        )
        return None

    def test_notationsymbol_black(self):
        piece = pieces.BasePiece('black', 'a', [core.Vector(0, 1)], crawler=True)
        self.assertEqual(
            piece.notationsymbol, 'a',
            errormessage(piece.notationsymbol, 'a')
        )
        return None

    def test_colourattribute(self):
        self.assertEqual(self.piece.colour, 'white')
        return None

    def test_stringcall(self):
        self.assertEqual(
            str(self.piece), 'BasePiece'
        )
        return None

    def test_equality(self):
        piece2 = pieces.BasePiece(
            'black', '?', [core.Vector(0, 1)], crawler=True)

        self.assertEqual(
            self.piece, piece2,
            errormessage(
                "%s =/= %s" % (self.piece, "BasePiece"),
                "%s == %s" % (self.piece, "BasePiece")
            )
        )
        return None

    def test_inequality(self):
        piece2 = pieces.BishopPiece('white')

        self.assertNotEqual(
            self.piece, piece2,
            errormessage(
                "%s == %s" % (self.piece, "BishopPiece"),
                "%s =/= %s" % (self.piece, "BishopPiece")
            )
        )
        return None

    def test_type(self):
        self.assertTrue(
            self.piece.type is pieces.BasePiece,
            errormessage(
                "%s is not BasePiece" % str(self.piece),
                "%s is BasePiece" % str(self.piece)
            )
        )
        return None

    def test_assertisvector(self):
        self.piece._assertisvector(core.Vector(1, 0))  # Do nothing if vector.
        with self.assertRaises(TypeError):
            self.piece._assertisvector((1, 4))
        return None


class TestKnightPiece(unittest.TestCase):
    """Make sure that the knight is behaving correctly."""

    def setUp(self):
        self.piece = pieces.KnightPiece('white')
        return None

    def test_type(self):
        self.assertTrue(
            self.piece.type is pieces.KnightPiece,
            errormessage(
                "%s is not %s" % (self.piece.type, "KnightPiece"),
                "%s is %s" % (self.piece.type, "KnightPiece")
            )
        )
        return None

    def test_equality(self):
        piece2 = pieces.KnightPiece('black')

        self.assertEqual(
            self.piece, piece2,
            errormessage(
                "%s =/= %s" % (self.piece, "KnightPiece"),
                "%s == %s" % (self.piece, "KnightPiece")
            )
        )
        return None


class TestBishopPiece(unittest.TestCase):
    """Make sure that the bishop is behaving correctly."""

    def setUp(self):
        self.piece = pieces.BishopPiece('white')
        return None

    def tearDown(self):
        return None

    def test_type(self):
        self.assertTrue(
            self.piece.type is pieces.BishopPiece,
            errormessage(
                "%s is not %s" % (self.piece.type, "BishopPiece"),
                "%s is %s" % (self.piece.type, "BishopPiece")
            )
        )
        return None

    def test_equality(self):
        piece2 = pieces.BishopPiece('black')

        self.assertEqual(
            self.piece, piece2,
            errormessage(
                "%s =/= %s" % (self.piece, "BishopPiece"),
                "%s == %s" % (self.piece, "BishopPiece")
            )
        )
        return None


class TestQueenPiece(unittest.TestCase):
    """Make sure that the queen is behaving correctly."""

    def setUp(self):
        self.piece = pieces.QueenPiece('white')
        return None

    def tearDown(self):
        return None

    def test_type(self):
        self.assertTrue(
            self.piece.type is pieces.QueenPiece,
            errormessage(
                "%s is not %s" % (self.piece.type, "QueenPiece"),
                "%s is %s" % (self.piece.type, "QueenPiece")
            )
        )
        return None

    def test_equality(self):
        piece2 = pieces.QueenPiece('black')

        self.assertEqual(
            self.piece, piece2,
            errormessage(
                "%s =/= %s" % (self.piece, "QueenPiece"),
                "%s == %s" % (self.piece, "QueenPiece")
            )
        )
        return None


class TestKingPiece(unittest.TestCase):
    """Make sure that the king is behaving correctly."""

    def setUp(self):
        self.piece = pieces.KingPiece('white')
        return None

    def tearDown(self):
        return None

    def test_type(self):
        self.assertTrue(
            self.piece.type is pieces.KingPiece,
            errormessage(
                "%s is not %s" % (self.piece.type, "KingPiece"),
                "%s is %s" % (self.piece.type, "KingPiece")
            )
        )
        return None

    def test_equality(self):
        piece2 = pieces.KingPiece('black')

        self.assertEqual(
            self.piece, piece2,
            errormessage(
                "%s =/= %s" % (self.piece, "KingPiece"),
                "%s == %s" % (self.piece, "KingPiece")
            )
        )
        return None


class TestRookPiece(unittest.TestCase):
    """Make sure that the rook is behaving correctly."""

    def setUp(self):
        self.piece = pieces.RookPiece('white')
        return None

    def tearDown(self):
        return None

    def test_type(self):
        self.assertTrue(
            self.piece.type is pieces.RookPiece,
            errormessage(
                "%s is not %s" % (self.piece.type, "RookPiece"),
                "%s is %s" % (self.piece.type, "RookPiece")
            )
        )
        return None

    def test_equality(self):
        piece2 = pieces.RookPiece('black')

        self.assertEqual(
            self.piece, piece2,
            errormessage(
                "%s =/= %s" % (self.piece, "RookPiece"),
                "%s == %s" % (self.piece, "RookPiece")
            )
        )
        return None


class TestPawnPiece(unittest.TestCase):
    """Make sure that the pawn is behaving correctly."""

    def setUp(self):
        self.piece = pieces.PawnPiece('white')
        return None

    def tearDown(self):
        return None

    def test_type(self):
        self.assertTrue(
            self.piece.type is pieces.PawnPiece,
            errormessage(
                "%s is not %s" % (self.piece.type, "PawnPiece"),
                "%s is %s" % (self.piece.type, "PawnPiece")
            )
        )
        return None

    def test_equality(self):
        piece2 = pieces.PawnPiece('black')

        self.assertEqual(
            self.piece, piece2,
            errormessage(
                "%s =/= %s" % (self.piece, "PawnPiece"),
                "%s == %s" % (self.piece, "PawnPiece")
            )
        )
        return None


if __name__ == '__main__':
    unittest.main(verbosity=2)
