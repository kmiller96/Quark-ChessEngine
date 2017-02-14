# DESCRIPTION: Contains the heavy-lifting of the engine: search & evaluation.

# 50726f6772616d6d696e6720697320627265616b696e67206f66206f6e652062696720696d706f
# 737369626c65207461736b20696e746f207365766572616c207665727920736d616c6c20706f73
# 7369626c65207461736b732e

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MAIN~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from copy import deepcopy
from lib import chessboard, core, movegenerator, pieces

class EngineSearch:
    """This is the search part of the engine, that finds moves to make."""

    def __init__(self, boardstate):
        self.board = deepcopy(boardstate)
        return None


class EngineEvaluation:
    """This is the evaluation part of the engine, which determines if the move
    is any good."""

    def __init__(self, boardstate):
        self.board = deepcopy(boardstate)
        return None


class ChessEngine:
    """The class that combines the two separate components to work together."""

    def __init__(self, boardstate):
        self.search = EngineSearch(boardstate)
        self.evaluate = EngineEvaluation(boardstate)
        return NOne
