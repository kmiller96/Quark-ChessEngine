# DESCRIPTION: Contains all of the code, classes and functions corresponding to
# the board.

# 50726f6772616d6d696e6720697320627265616b696e67206f66206f6e652062696720696d706f
# 737369626c65207461736b20696e746f207365766572616c207665727920736d616c6c20706f73
# 7369626c65207461736b732e

# NOTE:
# ================
# This file is currently a work in progress. The original chessboard.py file has
# become overly bloated and is detrimental to the moral of the project. This new
# script is aimed at taking only the methods that pertain to a chessboard, while
# separating the other components into their own scrips

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MAIN~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from lib import core, exceptions

class _ChessBoardCore:
    """Contains the core methods, plus the __init__ method."""

    def __init__(self):
        return None


class ChessBoard(_ChessBoardCore):
    """The public class that is the chessboard.

    This class creates a chessboard, much like you have a physical board when
    you play chess. It is a pretty dumb class however; it doesn't have many
    checks in place for moves and it can't do anything special like make moves.
    """

    pass
