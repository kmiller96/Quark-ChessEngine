# DESCRIPTION: Tests the performance of the engine.

# 4920646f6e5c2774206361726520696620697420776f726b73206f6e20796f7572206d61636869
# 6e652120576520617265206e6f74207368697070696e6720796f7572206d616368696e6521

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import time, unittest
from lib import chessboard, core, engine, movegenerator, pieces, usercontrol

class Timer(object):
    def __init__(self, verbose=False):
        self.verbose = verbose

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000  # millisecs
        if self.verbose:
            print 'elapsed time: %f ms' % self.msecs

class TestMoveGenerator(unittest.TestCase):
    """Tests the performance of the move generator."""

    def setUp(self):
        self.board = chessboard.ChessBoard()
        self.board[27] = pieces.KingPiece('white')
        self.board[45] = pieces.KingPiece('black')
        self.generator = movegenerator.MoveGenerator(self.board)
        return None

    def test_basicmoves(self):
        with Timer() as t:
            for x in xrange(10000):
                self.generator._basicmoves('white')
        print '\n\t=> elapsed time for 10000 loops: %s s' % t.secs
        return None

    def test_pawnpushmoves(self):
        with Timer() as t:
            for x in xrange(10000):
                self.generator._pawnpushmoves('white')
        print '\n\t=> elapsed time for 10000 loops: %s s' % t.secs
        return None

    def test_pawncapturemoves(self):
        with Timer() as t:
            for x in xrange(10000):
                self.generator._pawncapturemoves('white')
        print '\n\t=> elapsed time for 10000 loops: %s s' % t.secs
        return None

    def test_castlemoves(self):
        with Timer() as t:
            for x in xrange(10000):
                self.generator._castlemoves('white')
        print '\n\t=> elapsed time for 10000 loops: %s s' % t.secs
        return None

    def test_enpassantmoves(self):
        with Timer() as t:
            for x in xrange(10000):
                self.generator._enpassantmoves('white')
        print '\n\t=> elapsed time for 10000 loops: %s s' % t.secs
        return None

    def test_onlylegalmoves(self):
        moves = self.generator._basicmoves('white')
        with Timer() as t:
            for x in xrange(10000):
                self.generator._onlylegalmoves('white', moves)
        print '\n\t=> elapsed time for 10000 loops: %s s' % t.secs
        return None

    def test_illegalmove(self):
        with Timer() as t:
            for x in xrange(10000):
                self.generator.illegalmove((27, 36), 'white')
        print '\n\t=> elapsed time for 10000 loops: %s s' % t.secs
        return None

    def test_kingincheck(self):
        with Timer() as t:
            for x in xrange(10000):
                self.generator.kingincheck('white')
        print '\n\t=> elapsed time for 10000 loops: %s s' % t.secs
        return None

    def test_generatemovelist(self):
        with Timer() as t:
            for x in xrange(10000):
                self.generator.generatemovelist('white')
        print '\n\t=> elapsed time for 10000 loops: %s s' % t.secs
        return None

    def test_initialise_and_generate(self):
        with Timer() as t:
            for x in xrange(10000):
                movegenerator.MoveGenerator(self.board).generatemovelist('white')
        print '\n\t=> elapsed time for 10000 loops: %s s' % t.secs
        return None


class TestChessboard(unittest.TestCase):
    """Tests the performance of the chessboard."""

    def setUp(self):
        self.board = chessboard.ChessBoard()
        self.board.setupnormalboard()
        return None

    def test_duplicateboard(self):
        with Timer() as t:
            for x in xrange(10000):
                self.board.duplicateboard()
        print '\n\t=> elapsed time for 10000 loops: %s s' % t.secs
        return None

    def test_move(self):
        with Timer() as t:
            for x in xrange(5000):
                self.board.move(12, 28)
                self.board.move(28, 12)
        print '\n\t=> elapsed time for 10000 loops: %s s' % t.secs
        return None


class TestNodeAndTree(unittest.TestCase):
    """Looks at the node and tree in the recursive search."""

    def setUp(self):
        self.node = engine.Node
        return None

    def test_node_noparent(self):
        # Set up the board state.
        state = chessboard.ChessBoard()
        state[5] = pieces.RookPiece('white')
        # Then time it.
        with Timer() as t:
            for x in xrange(10000):
                engine.Node(None, (1, 5), state)
        print '\n\t=> elapsed time for 10000 loops: %s s' % t.secs
        return None

    def test_node_parent(self):
        # Make the parent first.
        parentstate = chessboard.ChessBoard()
        parentstate[1] = pieces.RookPiece('white')
        parent = engine.Node(None, (0, 1), parentstate)

        # Set up the board state.
        state = chessboard.ChessBoard()
        state[5] = pieces.RookPiece('white')

        # Then time it.
        with Timer() as t:
            for x in xrange(10000):
                engine.Node(parent, (1, 5), state)
        print '\n\t=> elapsed time for 10000 loops: %s s' % t.secs
        return None

    def test_tree_initialise(self):
        with Timer() as t:
            for x in xrange(10000):
                engine.TreeStructure()
        print '\n\t=> elapsed time for 10000 loops: %s s' % t.secs
        return None

    def test_tree_addnode(self):
        # Initilise Tree
        tree = engine.TreeStructure()

        # Make the parent first.
        parentstate = chessboard.ChessBoard()
        parentstate[1] = pieces.RookPiece('white')
        parent = engine.Node(None, (0, 1), parentstate)

        # Set up the board state.
        state = chessboard.ChessBoard()
        state[5] = pieces.RookPiece('white')
        child = engine.Node(parent, (1, 5), state)
        with Timer() as t:
            for x in xrange(10000):
                tree.addnode(child)
        print '\n\t=> elapsed time for 10000 loops: %s s' % t.secs
        return None


if __name__ == '__main__':
    unittest.main(verbosity=2)
