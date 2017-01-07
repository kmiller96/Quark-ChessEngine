# DESCRIPTION: Contains more advanced tests for the chess board.

# 4920646f6e5c2774206361726520696620697420776f726b73206f6e20796f7572206d61636869
# 6e652120576520617265206e6f74207368697070696e6720796f7572206d616368696e6521

# DEVELOPMENT LOG:
#    30/12/16: Initialised testing suite. Added some framework.
#    05/01/17: Added tests for the movement of single pieces on the board. Added
# tests for the movement of two pieces together on the board.


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~IMPORTS/GLOBALS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from time import time
import unittest
from random import randint, choice
from lib import chessboard, core
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.:.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~TESTING~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class CoreTestingSuite(unittest.TestCase):
    """Contains the core methods for the testing suites in this script."""
    # TODO: Remove duplicate code.
    # TODO: Refactor code to make it more readable.

    def setUp(self):
        """Initialise the board."""
        # Make a plain, clear board.
        self.board = chessboard.ChessBoard()

        # Make special error messages to print if all hell breaks loose.
        self.errormessage = "ERROR"
        return None

    def tearDown(self):
        """Destroy the tainted board. An extra procaution."""
        self.board = None
        return None

    def convert(self, x, **kwargs):
        """Shortcut for self.board.convert call."""
        return self.board.convert(x, **kwargs)

    def readablelistof(self, lst):
        """Shortcut for self.board._readablelistof call."""
        return self.board._readablelistof(lst)

    @staticmethod
    def innersquares():
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

    def runmovementtestfor(self, piece, atstartindex):
        """Runs the movement test for the piece passed."""
        print ""
        self.board.addpiece(piece, position=atstartindex, playerpiece=True)
        print "Here is the board with the %r on it:\n" % str(piece)
        self.board.displayboard()

        print "\nTEST: WHERE CAN THE PIECE MOVE."
        print "================================"
        for piece, moves in self.board.allpossiblemoves().iteritems():
            piecepos = piece.position(indexform=True)
            moves = self.readablelistof(
                map(lambda x: self.convert(x, toindex=True), moves))
        print "The piece, at index %i, can move to these positions:" % piecepos
        print moves + '\n'
        check = raw_input("Does all of the above seem right? [y/n]: ")
        while check.lower() not in ('y', 'n'):
            check = raw_input("Type either 'y' or 'n' to proceed.")
        if check.lower() == 'n':
            self.fail("Incorrect moves for the piece %s." % str(piece))
        else:
            print "Test passed!"
            print "--------------------------------------------------------\n"
        return None

    def runmovementtestforpieces(self, listoftuples, sameside=True):
        """Runs the movement test for the pieces passed.

        The parameter listoftuples is of the format:
            (piece, atstartindex)
        Which is basically a list of the parameters runmovementtestfor in the
        core. If sameside is false then the pieces alternate sides when added.
        """
        print ""
        piecelist = list(); whichside = 0
        for tup in listoftuples:
            if sameside:
                side = True
            else:
                whichside += 1
                if whichside % 2:
                    side = True
                else:
                    side = False
            piecelist.append(tup[0])
            self.board.addpiece(tup[0], position=tup[1], playerpiece=side)
        print "Here is the board with the pieces %r on it:\n" % self.readablelistof(piecelist)
        self.board.displayboard()

        print "\nTEST: WHERE CAN THE PIECES MOVE."
        print "================================="
        for piece, moves in self.board.allpossiblemoves(playerpieces=True).iteritems():
            piecepos = piece.position(indexform=True)
            moves = self.readablelistof(
                map(lambda x: self.convert(x, toindex=True), moves))
            print "The piece, at index %i, can move to these positions:" % piecepos
            print moves + '\n'
        for piece, moves in self.board.allpossiblemoves(playerpieces=False).iteritems():
            piecepos = piece.position(indexform=True)
            moves = self.readablelistof(
                map(lambda x: self.convert(x, toindex=True), moves))
            print "The piece, at index %i, can move to these positions:" % piecepos
            print moves + '\n'
        check = raw_input("Does all of the above seem right? [y/n]: ")
        while check.lower() not in ('y', 'n'):
            check = raw_input("Type either 'y' or 'n' to proceed.")
        if check.lower() == 'n':
            self.fail("Incorrect moves for the piece %s." % str(piece))
        else:
            print "Test passed!"
            print "--------------------------------------------------------\n"
        return None

    def runpinnedtestfor(self, pinpiece, atstartindex):
        """Runs the pinned test for the piece passed."""
        print ""
        self.board.addpiece(pinpiece, position=atstartindex, playerpiece=True)
        print "Here is the board with the %r pinned on it:\n" % str(pinpiece)
        self.board.displayboard()

        print "\nTEST: CAN THE PIECE MOVE?"
        print "================================"
        pinpieceinstance = self.board[atstartindex]
        for piece, moves in self.board.allpossiblemoves().iteritems():
            if piece is not pinpieceinstance:
                continue
            else:
                piecepos = piece.position(indexform=True)
                mymovelist = map(lambda x: self.convert(x, toindex=True), moves)
        print "The piece, at index %i, can move to these positions:" % piecepos
        print str(self.readablelistof(mymovelist)) + '\n'
        check = raw_input("Does all of the above seem right? [y/n]: ")
        while check.lower() not in ('y', 'n'):
            check = raw_input("Type either 'y' or 'n' to proceed.")
        if check.lower() == 'n':
            self.fail("Incorrect moves for the piece %s." % str(piece))
        else:
            print "Test passed!"
            print "--------------------------------------------------------\n"
        return None


class TestSinglePieceMovement(CoreTestingSuite):
    """These tests involve moving a single piece around the board and making
    sure that it behaves correctly.

    This suite assumes that each "core" method behaves correctly in order to
    simplify the tests and to conduct more integrated tests. So, as an example,
    it will call addpiece instead of manually inserting it."""

    def test_KingMovement(self):
        self.runmovementtestfor(core.KingPiece, randint(0, 63))
        return None

    def test_QueenMovement(self):
        self.runmovementtestfor(core.QueenPiece, randint(0, 63))
        return None

    def test_BishopMovement(self):
        self.runmovementtestfor(core.BishopPiece, randint(0, 63))
        return None

    def test_KnightMovement(self):
        self.runmovementtestfor(core.KnightPiece, randint(0, 63))
        return None

    def test_RookMovement(self):
        self.runmovementtestfor(core.RookPiece, randint(0, 63))
        return None

    def test_PawnMovement(self):
        self.runmovementtestfor(core.PawnPiece, randint(0, 63))
        return None


class TestTwoPiecesMovement_SameSide(CoreTestingSuite):
    """Now the tests are a little harder. This suite tests where the legal moves
    are if there are only two pieces on the board, both of which are on the same
    team."""

    def test_AdjancentPieces(self):
        startpos = choice(self.innersquares())
        startvec = self.convert(startpos, tovector=True)
        adjacentvector = core.Vector(randint(-1, 1), randint(-1, 1))
        startpos2 = self.convert(startvec + adjacentvector, toindex=True)

        self.runmovementtestforpieces(
            ((core.KingPiece, startpos), (core.KingPiece, startpos2))
        )
        return None

    def test_PiecesOnSameRank(self):
        rank = randint(0, 7)  # Pick a rank randomly.
        file1 = randint(0, 7)
        file2 = randint(0, 7)
        while file1 == file2:  # Don't let the pieces be on the same square.
            file2 = randint(0, 7)

        startpos1 = self.convert(core.Vector(rank, file1), toindex=True)
        startpos2 = self.convert(core.Vector(rank, file2), toindex=True)

        self.runmovementtestforpieces(
            ((core.RookPiece, startpos1), (core.RookPiece, startpos2))
        )
        return None

    def test_PiecesOnSameFile(self):
        file_ = randint(0, 7)  # Pick a file randomly.
        rank1 = randint(0, 7)
        rank2 = randint(0, 7)
        while rank1 == rank2:  # Don't let the pieces be on the same square.
            rank2 = randint(0, 7)

        startpos1 = self.convert(core.Vector(rank1, file_), toindex=True)
        startpos2 = self.convert(core.Vector(rank2, file_), toindex=True)

        self.runmovementtestforpieces(
            ((core.RookPiece, startpos1), (core.RookPiece, startpos2))
        )
        return None

    def test_PiecesOnSameDiagonal(self):
        startpos1 = 18
        startpos2 = 45  # Magic numbers because cbf making randomised.

        self.runmovementtestforpieces(
            ((core.BishopPiece, startpos1), (core.BishopPiece, startpos2))
        )


class TestTwoPiecesMovement_OpposingSides(CoreTestingSuite):
    """The same as TestTwoPiecesMovement_SameSide except now the pieces are
    on opposing teams."""

    def test_AdjancentPieces(self):
        startpos = choice(self.innersquares())
        startvec = self.convert(startpos, tovector=True)
        adjacentvector = core.Vector(randint(-1, 1), randint(-1, 1))
        startpos2 = self.convert(startvec + adjacentvector, toindex=True)

        self.runmovementtestforpieces(
            ((core.KingPiece, startpos), (core.KingPiece, startpos2)),
            sameside=False
        )
        return None

    def test_PiecesOnSameRank(self):
        rank = randint(0, 7)  # Pick a rank randomly.
        file1 = randint(0, 7)
        file2 = randint(0, 7)
        while file1 == file2:  # Don't let the pieces be on the same square.
            file2 = randint(0, 7)

        startpos1 = self.convert(core.Vector(rank, file1), toindex=True)
        startpos2 = self.convert(core.Vector(rank, file2), toindex=True)

        self.runmovementtestforpieces(
            ((core.RookPiece, startpos1), (core.RookPiece, startpos2)),
            sameside=False
        )
        return None

    def test_PiecesOnSameFile(self):
        file_ = randint(0, 7)  # Pick a file randomly.
        rank1 = randint(0, 7)
        rank2 = randint(0, 7)
        while rank1 == rank2:  # Don't let the pieces be on the same square.
            rank2 = randint(0, 7)

        startpos1 = self.convert(core.Vector(rank1, file_), toindex=True)
        startpos2 = self.convert(core.Vector(rank2, file_), toindex=True)

        self.runmovementtestforpieces(
            ((core.RookPiece, startpos1), (core.RookPiece, startpos2)),
            sameside=False
        )
        return None

    def test_PiecesOnSameDiagonal(self):
        startpos1 = 18
        startpos2 = 45  # Magic numbers because cbf making randomised.

        self.runmovementtestforpieces(
            ((core.BishopPiece, startpos1), (core.BishopPiece, startpos2)),
            sameside=False
        )


class TestPins(CoreTestingSuite):
    """This testing suite only tests the ability of the engine to detect pins."""
    # WIP

    def test_FilePin(self):
        # Setup board.
        self.board.addpiece(core.KingPiece, 19, playerpiece=True)
        self.board.addpiece(core.RookPiece, 35, playerpiece=False)

        # Now add a piece between the King and Rook and see if pinned.
        self.runpinnedtestfor(core.KnightPiece, 27)
        return

    def test_RankPin(self):
        # Setup board.
        self.board.addpiece(core.KingPiece, 25, playerpiece=True)
        self.board.addpiece(core.RookPiece, 31, playerpiece=False)

        # Now add a piece between the King and Rook and see if pinned.
        self.runpinnedtestfor(core.BishopPiece, 28)
        return

    def test_DiagonalPin(self):
        # Setup board.
        self.board.addpiece(core.KingPiece, 9, playerpiece=True)
        self.board.addpiece(core.BishopPiece, 36, playerpiece=False)

        # Now add a piece between the King and Rook and see if pinned.
        self.runpinnedtestfor(core.PawnPiece, 18)
        return


class TestChecks(CoreTestingSuite):
    """Runs tests on checks."""
    pass


class TestCheckmates(CoreTestingSuite):
    """Runs tests on checkmate conditions."""
    pass
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.:.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~FINAL EXECUTION~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':
    unittest.main(verbosity=2)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.:.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
