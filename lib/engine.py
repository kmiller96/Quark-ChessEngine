# DESCRIPTION: Contains the heavy-lifting of the engine: search & evaluation.

# 50726f6772616d6d696e6720697320627265616b696e67206f66206f6e652062696720696d706f
# 737369626c65207461736b20696e746f207365766572616c207665727920736d616c6c20706f73
# 7369626c65207461736b732e

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MAIN~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from copy import copy, deepcopy
from lib import chessboard, core, movegenerator, pieces

class Evaluator:
    """Evaluate a board as a "chess score" in order to pick the best moves."""

    def __init__(self):
        return None

    def materialscore(self, board):
        """Looks at the material advantage present on the board."""
        def piecediff(piecetype):
            """Find if one side is up pieces (+ for white, - for black)"""
            whitepieces = len(board.findpiece(piecetype, 'white'))
            blackpieces = len(board.findpiece(piecetype, 'black'))
            return whitepieces - blackpieces

        positionvalue = (
            piecediff(pieces.KingPiece)*100000 +
            piecediff(pieces.QueenPiece)*9000 +
            piecediff(pieces.RookPiece)*5000 +
            piecediff(pieces.BishopPiece)*2500 +
            piecediff(pieces.KnightPiece)*2500 +
            piecediff(pieces.PawnPiece)*1000
        )
        return positionvalue

    def mobilityscore(self, board):
        """Determines how mobile each side is and returns a net score."""
        generator = movegenerator.MoveGenerator(board)
        whitemobility = len(generator.generatemovelist('white'))*100
        blackmobility = len(generator.generatemovelist('black'))*100
        return whitemobility - blackmobility

    def evaluate(self, board):
        """Evaluates the board passed, considering lots of factors."""
        netscore = 0
        netscore += self.materialscore(board)
        netscore += self.mobilityscore(board)
        return None


class ChessEngine:
    """The brains of the computer. It searches and evaluates positions."""

    def __init__(self):
        self.evaluate = Evaluator.evaluate
        return None
