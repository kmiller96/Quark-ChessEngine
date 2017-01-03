# DESCRIPTION: Contains all of the unit tests for the chess board.

# 4920646f6e5c2774206361726520696620697420776f726b73206f6e20796f7572206d61636869
# 6e652120576520617265206e6f74207368697070696e6720796f7572206d616368696e6521

# DEVELOPMENT LOG:
#    20/11/16: Initialized testing script. Added core unittests for the chess
# board. Initialised a semi-integrated testing suite for a short game.
#    26/12/16: Fixed script to obey 80 character limit. Abstracted the tests
# in order to randomly certain squares.
#    30/12/16: Removed the short game testing suite and moved it to the testing
# suite tests_chessboardadvanced.py.
#    01/01/17: Fixed the file to work with the refactored code. Separated some
# of the tests into good input or bad input methods to increase readabilty and
# help identify bugs.
#    03/01/17: Fixed errors/fails raised when calling tests, some of which were
# in this script and some of which were an actual bug. Added tests for new
# methods created in UI and GUI classes.

# TESTING REQUIREMENTS:
# The chess board, for basic tests, should be very strict on what inputs it can
# accept. It should instantly fail if there is a bad input by a string, for
# example.

# TODO:
# - Change testing suite so that each component of the engine (i.e the parent
#   classes) is tested in its own suite.

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~IMPORTS/GLOBALS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from time import time
import unittest
from random import randint
from lib import exceptions, core
from lib import chessboard
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.:.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~TESTING~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class TestBoard(unittest.TestCase):
    """A basic testing suite the pertains to only the most basic of calls."""

    def setUp(self):
        """Initialise the board."""
        self.board = chessboard.ChessBoard()

        # Pick a position on the board to test.
        self.startpos = randint(0, 63)
        self.startcoord = (self.startpos / 8, self.startpos % 8)
        self.startvector = core.Vector(*self.startcoord)

        # Put a piece on the board.
        self.piece = 'X'
        self.realpiece = core.QueenPiece(playerpiece=True, startpositionindex=27)  # NOTE: Move into tests that care about the piece being real.
        self.board._board[self.startpos] = self.piece  # Insert piece manually.

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

    def test_convert_goodinput(self):
        def testequalityfor(totestagainst, toconvert, **kwargs):
            """Simplified testing call."""
            self.assertEqual(totestagainst,
                self.board.convert(toconvert,**kwargs))
            return None

        # First test index conversion.
        testequalityfor(self.startpos, self.startpos, toindex=True)
        testequalityfor(self.startcoord, self.startpos, tocoordinate=True)
        testequalityfor(self.startvector, self.startpos, tovector=True)
        # Next test coordinate conversion.
        testequalityfor(self.startpos, self.startcoord, toindex=True)
        testequalityfor(self.startcoord, self.startcoord, tocoordinate=True)
        testequalityfor(self.startvector, self.startcoord, tovector=True)
        # Finally test vector conversion.
        testequalityfor(self.startpos, self.startvector, toindex=True)
        testequalityfor(self.startcoord, self.startvector, tocoordinate=True)
        testequalityfor(self.startvector, self.startvector, tovector=True)
        return None

    def test_convert_badinput(self):
        # Dont specify what to convert to.
        self.assertRaises(AssertionError,
            self.board.convert, self.startpos)
        # Want two conversions at once.
        self.assertRaises(AssertionError,
            self.board.convert, self.startcoord, toindex=True, tocoordinate=True)
        # Pass in something other then index/coordinate/vector.
        self.assertRaises(TypeError,
            self.board.convert, 'bad string', toindex=True)
        return None

    def test_assertPositionOnBoard_goodinput(self):
        testfunc = self.board._assertPositionOnBoard
        try:
            testfunc(core.Vector(3, 4))  # Vector.
            testfunc((2, 6))  # Tuple.
            testfunc([5, 1])  # List.
            testfunc(16)  # Index
        except AssertionError:
            self.fail("AssertionError was raised when it should have passed.")
        return None

    def test_assertPositionOnBoard_badinput(self):
        testfunc = self.board._assertPositionOnBoard
        self.assertRaises(
            TypeError, testfunc, 'string')  # String
        self.assertRaises(
            TypeError, testfunc, 13.11)  # Float.
        self.assertRaises(
            AssertionError, testfunc, (8, 4))  # Tuple off board.
        self.assertRaises(
            AssertionError, testfunc, core.Vector(-3, 5))  # Vector off board.
        return None

    def test_isoccupied_goodinput(self):
        self.assertTrue(
            self.board._isoccupied(self.startpos),
            'The square should be occupied.' + self.errormessage
        )
        self.assertFalse(
            self.board._isoccupied((self.startpos+1) % 63),
            'The square should be unoccupied.' + self.errormessage
        )
        return None

    def test_assertIsUnoccupied_goodinput(self):
        try:
            self.board._assertIsUnoccupied((self.startpos+1) % 63)
        except AssertionError:
            self.fail("An AssertionError was raised when the input was good!")

    def test_assertIsUnoccupied_badinput(self):
        self.assertRaises(
            AssertionError, self.board._assertIsUnoccupied, self.startpos)

    def test_assertIsOccupied_goodinput(self):
        try:
            self.board._assertIsOccupied(self.startpos)
        except AssertionError:
            self.fail("An AssertionError was raised when the input was good!")

    def test_assertIsOccupied_badinput(self):
        self.assertRaises(AssertionError,
            self.board._assertIsOccupied, (self.startpos+1) % 63)

    def test_piecesbetween(self):
        self.board._board[self.startpos] = None  # Get a clean board.
        self.board._board[27] = self.piece  # Move to center for testing.

        piecesbetween = self.board.piecesbetween
        errormsg = "The method coudn't find the piece."
        self.assertTrue(len(piecesbetween(26, 28)) == 1, errormsg)  # Left to right
        self.assertTrue(len(piecesbetween(31, 24)) == 1, errormsg)  # Right to left
        self.assertTrue(len(piecesbetween(19, 35)) == 1, errormsg)  # Below to above
        self.assertTrue(len(piecesbetween(18, 36)) == 1, errormsg)  # SW to NE
        self.assertTrue(len(piecesbetween(20, 34)) == 1, errormsg)  # SE to NW
        return None

    def test_addpiece_badinput(self):
        self.assertRaises(AssertionError,
            self.board.addpiece, self.piece, self.startpos
        )

    def test_addpiece_goodinput(self):
        pos2 = (self.startpos + 1) % 63
        try:
            piecetype = core.KnightPiece
            self.board.addpiece(piecetype, pos2)
            self.board.addpiece(piecetype, self.startpos, force=True)
            self.assertTrue(
                isinstance(self.board._board[pos2], piecetype),
                "The piece wasn't added correctly.")
        except Exception as error:
            self.fail("%s" % error)
        return None

    def test_emptysquare(self):
        try:
            self.board.emptysquare((self.startpos+1) % 63)  # Empty already empty square.
            self.board.emptysquare(self.startpos)  # Empty full square.
        except:
            self.fail("An unexpected error was raised!")

    def test_move(self):
        # Bad move.
        self.assertRaises(AssertionError,
            self.board.move, self.startpos, self.startpos
        )
        self.assertRaises(AssertionError,
            self.board.move, self.startpos, 99
        )
        # Good inputs.
        try:
            self.board.move(self.startpos, (self.startpos+1) % 63)
            self.assertEqual(  # Check piece isn't in old positon.
                self.board._board[self.startpos], None,
                "The piece remains in its old spot." + self.errormessage)
            self.assertEqual(  # Check piece is in new position.
                self.board._board[(self.startpos+1) % 63], self.piece,
                "The piece should have moved, but it didn't.")
        except AssertionError:
            raise
        except:
            self.fail("An error was raised for some reason.")

    def test_capture(self):
        self.board._board[(self.startpos+1) % 63] = self.realpiece
        # Bad inputs
        self.assertRaises(AssertionError,  # Index off board.
            self.board.capture, self.startpos, 99)
        self.assertRaises(AssertionError,  # No piece at end index.
            self.board.capture, self.startpos, (self.startpos+2) % 63)
        # Good input.
        try:
            self.board.capture(self.startpos, (self.startpos+1) % 63)
        except Exception as error:
            self.fail("%s" % error)

    def test_positiontonotation(self):
        func = self.board._positiontonotation
        # First position.
        self.assertEqual('e1', func(4))
        self.assertEqual('e1', func((0, 4)))
        self.assertEqual('e1', func(core.Vector(*(0, 4))))

        # Second position.
        self.assertEqual('f7', func(53))
        self.assertEqual('f7', func((6, 5)))
        self.assertEqual('f7', func(core.Vector(*(6, 5))))

    def test_notationtoposition(self):
        notation1 = 'e7'; notation2 = 'h5'; notation3 = 'c1'; notation4 = 'a2'
        self.assertEqual(52,
            self.board._notationtoposition(notation1, indexform=True))
        self.assertEqual(core.Vector(4, 7),
            self.board._notationtoposition(notation2, vectorform=True))
        self.assertEqual(2,
            self.board._notationtoposition(notation3, indexform=True))
        self.assertEqual(core.Vector(1, 0),
            self.board._notationtoposition(notation4, vectorform=True))
        return None

    def test_addmovetohistory(self):
        piece = self.realpiece
        endpos = 19

        # A simple move.
        self.board.addmovetohistory(piece, endpos)
        self.assertEqual(self.board.movehistory()[-1], 'Qd3')

        # A move with capture.
        self.board.addmovetohistory(piece, endpos, movewascapture=True)
        self.assertEqual(self.board.movehistory()[-1], 'Qxd3')

    def test_addmovetohistory_pawnpiece(self):
        piece = core.PawnPiece(playerpiece=True, startpositionindex=10)
        print piece.position(vectorform=True)
        movepos = 18  # Move forward once.
        capturepos = 19  # Capture to your right.

        # A simple move.
        self.board.addmovetohistory(piece, movepos)
        self.assertEqual(self.board.movehistory()[-1], 'c3')

        # A move with capture.
        self.board.addmovetohistory(piece, capturepos, movewascapture=True)
        self.assertEqual(self.board.movehistory()[-1], 'cxd3')


class TestDefaultChessBoard(unittest.TestCase):
    """Tests on a regular chess board."""

    def setUp(self):
        self.board = chessboard.DefaultChessBoard()
        return None

    def tearDown(self):
        self.board = None
        return None

    def test_boardSetUpCorrectly(self):
        backline = [core.RookPiece, core.KnightPiece, core.BishopPiece,
                    core.QueenPiece, core.KingPiece, core.BishopPiece,
                    core.KnightPiece, core.RookPiece]  # Backline order.

        for ii in range(0, 7+1):  # Test white backline.
            self.assertTrue(isinstance(self.board._board[ii], backline[ii]))
        for ii in range(8, 15+1):  # Test white frontline.
            self.assertTrue(isinstance(self.board._board[ii], core.PawnPiece))
        for ii in range(48, 55+1):  # Test black frontline.
            self.assertTrue(isinstance(self.board._board[ii], core.PawnPiece))
        for ii in range(56, 63+1):  # Test black backline.
            self.assertTrue(isinstance(self.board._board[ii], backline[ii-56]))
        return None
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.:.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~FINAL EXECUTION~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':
    unittest.main(verbosity=2)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.:.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
