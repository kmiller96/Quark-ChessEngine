# DESCRIPTION: Tests the engine itself.

# 4920646f6e5c2774206361726520696620697420776f726b73206f6e20796f7572206d61636869
# 6e652120576520617265206e6f74207368697070696e6720796f7572206d616368696e6521

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import unittest
from lib import chessboard, core, engine, movegenerator, pieces, usercontrol

class TestSearch(unittest.TestCase):
    """Does tests on the search algorithm, especially making sure that it can
    find and note all of the legal moves irregardless of how good they are."""

    def setUp(self):
        self.board = chessboard.ChessBoard()
        self.search = engine.EngineSearch
        return None

    def test_brutesearch_onlykings(self):
        self.board[0] = pieces.KingPiece('white')
        self.board[56] = pieces.KingPiece('black')

        search = self.search(self.board)
        tree = search.brutesearch(4, 'white')

        # See if following boards in tree.
        simboard = chessboard.ChessBoard()
        simboard[18] = pieces.KingPiece('white')
        simboard[42] = pieces.KingPiece('black')
        self.assertIn(simboard, tree.treeboardstates)

        simboard = chessboard.ChessBoard()
        simboard[0] = pieces.KingPiece('white')
        simboard[56] = pieces.KingPiece('black')
        self.assertIn(simboard, tree.treeboardstates)

        simboard = chessboard.ChessBoard()
        simboard[9] = pieces.KingPiece('white')
        simboard[40] = pieces.KingPiece('black')
        self.assertIn(simboard, tree.treeboardstates)
        return None


class TestEvaluation(unittest.TestCase):
    """Does basic tests on the evaluation algorithm, making sure that the values
    it assigns are accurate based on the position."""

    def setUp(self):
        self.board = chessboard.ChessBoard()
        self.board[60] = pieces.KingPiece('black')
        self.board[4] = pieces.KingPiece('white')

        self.eval = engine.EngineEvaluation
        return None

    def test_uppiece_white(self):
        self.board[55] = pieces.QueenPiece('white')
        evaluator = self.eval(self.board)
        self.assertGreaterEqual(evaluator.evaluateposition(), 9)
        return None

    def test_uppiece_black(self):
        self.board[55] = pieces.QueenPiece('black')
        evaluator = self.eval(self.board)
        self.assertLessEqual(evaluator.evaluateposition(), -9)
        return None

    def test_equalpawns_whitedoubled(self):
        self.board[51] = pieces.PawnPiece('black')
        self.board[52] = pieces.PawnPiece('black')
        self.board[53] = pieces.PawnPiece('black')

        self.board[11] = pieces.PawnPiece('white')
        self.board[12] = pieces.PawnPiece('white')
        self.board[20] = pieces.PawnPiece('white')

        evaluator = self.eval(self.board)
        self.assertLess(evaluator.evaluateposition(), 0)
        return None

if __name__ == '__main__':
    unittest.main(verbosity=2)
