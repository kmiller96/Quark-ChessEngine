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
#    03/01/17: Wrote more tests/made broken tests work. This file is a major
# item on the list of things to do. There are lots of unfinished methods to
# complete.
#    !!NOTE!! This development log has been made redundant now that it is on
# GitHub.

# TODO:
# Rewrite these tests from scratch :(


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~IMPORTS/GLOBALS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from time import time
import unittest
from random import randint, choice
from lib import core
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.:.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~TESTING~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class TestBasePiece(unittest.TestCase):
    """Tests the behaviour of the basic piece."""

    def setUp(self):
        self.piece = core.BasePiece(
            playerpiece=True,
            startpositionindex=choice(self.innersquares()),
            notationsymbol='?',
            validmovevectors=(core.Vector(1, 0),),
            onlyunitvectors=True
        )
        return None

    def tearDown(self):
        self.piece = None
        return None

    def innersquares(self):
        """Gives only the squares at least one square away from the edge.

        The tests for movement all check one square away in every direction.
        So to still randomly pick positions on the board while maintaining that
        certain tests will always pass/fail this method is used."""
        flatten = lambda l: [item for sublist in l for item in sublist]

        possible_positions = [
            range(9, 14+1),
            range(17, 22+1),
            range(25, 30+1),
            range(33, 38+1),
            range(41, 46+1),
            range(49, 54+1)
        ]  # All squares that aren't on the edge.
        return flatten(possible_positions)

    def test_checkAllAreVectors_goodinput(self):
        vectorlist = [core.Vector(1,3), core.Vector(5,1), core.Vector(0,6)]
        try:
            self.piece._checkAllAreVectors(vectorlist)
        except Exception as error:
            self.fail("%s" % error)
        return

    def test_checkAllAreVectors_badinput(self):
        badlist1 = [(2,5), (6, 0), (7, 7)]  # Coordinates instead of vectors.
        badlist2 = ['strings', 'are', 'not', 'good']  # Strings instead of.
        badlist3 = ['some are strings', core.Vector(1, 2), (6, 5)]  # Mixed.
        badlist4 = core.Vector(7, 1)  # Not a list.

        self.assertRaises(AssertionError,
            self.piece._checkAllAreVectors, badlist1)
        self.assertRaises(AssertionError,
            self.piece._checkAllAreVectors, badlist2)
        self.assertRaises(AssertionError,
            self.piece._checkAllAreVectors, badlist3)
        self.assertRaises(TypeError,
            self.piece._checkAllAreVectors, badlist4)
        return

    def test_tovector_goodinput(self):
        index = 44  # Magic number to be certain the output is right.
        expectedvector = core.Vector(5, 4)
        self.assertEqual(expectedvector, self.piece._tovector(index),
            "The vector calculated doesn't match that as expected.")
        return

    def test_tovector_badinput(self):
        badinput1 = 'string'
        badinput2 = 14.09
        badinput3 = [1, 6, 12, 34]  # No lists.
        badinput4 = (2, 5)  # Doesn't accept coordinates.

        self.assertRaises(TypeError,
            self.piece._tovector, badinput1)
        self.assertRaises(TypeError,
            self.piece._tovector, badinput2)
        self.assertRaises(TypeError,
            self.piece._tovector, badinput3)
        self.assertRaises(TypeError,
            self.piece._tovector, badinput3)
        return

    def test_toindex_goodinput(self):
        vector = core.Vector(2, 2)
        expectedindex = 18  # Magic numbers to be certain of correct answer.

        self.assertEqual(expectedindex, self.piece._toindex(vector),
            "The output of _toindex didn't match expected result.")
        return

    def test_toindex_badinput(self):
        badinput1 = 'string'
        badinput2 = 14.09
        badinput3 = [core.Vector(1,3), core.Vector(5, 3)]  # No lists.
        badinput4 = (2, 5)  # Doesn't accept coordinates.

        self.assertRaises(TypeError,
            self.piece._toindex, badinput1)
        self.assertRaises(TypeError,
            self.piece._toindex, badinput2)
        self.assertRaises(TypeError,
            self.piece._toindex, badinput3)
        self.assertRaises(TypeError,
            self.piece._toindex, badinput3)
        return

    def test_piecetype(self):
        self.assertTrue(core.BasePiece, self.piece.piecetype)

    def test_distancefromselfto(self):
        self.piece.movetovector(core.Vector(3, 3))  # I have to call this method :(
        vec1 = core.Vector(4, 4); relvec1 = core.Vector(1, 1)
        vec2 = core.Vector(1, 4); relvec2 = core.Vector(-2, 1)
        vec3 = core.Vector(7, 1); relvec3 = core.Vector(4, -2)

        try:
            self.assertEqual(relvec1, self.piece.distancefromselfto(vec1))
            self.assertEqual(relvec2, self.piece.distancefromselfto(vec2))
            self.assertEqual(relvec3, self.piece.distancefromselfto(vec3))
        except AssertionError as error:
            self.fail("The relative vector calculated didn't match that expected.")
        return

    def test_position(self):
        # TODO: Goood and bad input checks.
        self.piece.movetoindex(33)
        self.assertEqual(33, self.piece.position(indexform=True))

        self.piece.movetovector(core.Vector(4,5))
        self.assertEqual(core.Vector(4,5), self.piece.position(vectorform=True))
        return

    def test_movetoindex(self):
        # TODO: This method.
        return

    def test_movetovector(self):
        # TODO: This method.
        return


class TestKingPiece(TestBasePiece):
    """Conduct basic unittests on the King."""

    def setUp(self):
        self.piece = core.KingPiece(
            playerpiece=True, startpositionindex=choice(self.innersquares())
        )
        return None

    def test_piecetype(self):
        self.assertTrue(core.KingPiece, self.piece.piecetype)
        return


class TestQueenPiece(TestBasePiece):
    """Conducts basic unittests on the Queen."""

    def setUp(self):
        self.piece = core.QueenPiece(
            playerpiece=True, startpositionindex=choice(self.innersquares())
        )
        return

    def test_piecetype(self):
        self.assertTrue(core.QueenPiece, self.piece.piecetype)
        return


class TestBishopPiece(TestBasePiece):
    """What do these tests pertain to?"""

    def setUp(self):
        self.piece = core.BishopPiece(
            playerpiece=True, startpositionindex=choice(self.innersquares())
        )
        return

    def test_piecetype(self):
        self.assertTrue(core.BishopPiece, self.piece.piecetype)
        return


class TestKnightPiece(TestBasePiece):
    """What do these tests pertain to?"""

    def setUp(self):
        self.piece = core.KnightPiece(
            playerpiece=True, startpositionindex=choice(self.innersquares())
        )
        return

    def test_piecetype(self):
        self.assertTrue(core.KnightPiece, self.piece.piecetype)
        return


class TestRookPiece(TestBasePiece):
    """Tests the behaviour of the rook piece."""

    def setUp(self):
        self.piece = core.RookPiece(
            playerpiece=True, startpositionindex=choice(self.innersquares())
        )
        return

    def test_piecetype(self):
        self.assertTrue(core.RookPiece, self.piece.piecetype)
        return


class TestPawnPiece(TestBasePiece):
    """These tests are for the pawn pieces. Since this is one of the hardest
    pieces to code these tests are much tougher to pass."""

    def setUp(self):
        self.piece = core.PawnPiece(
            playerpiece=True, startpositionindex=choice(range(8, 15+1))
        )
        return

    def test_piecetype(self):
        self.assertTrue(core.PawnPiece, self.piece.piecetype)
        return
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.:.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~FINAL EXECUTION~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':
    unittest.main(verbosity=2)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.:.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
