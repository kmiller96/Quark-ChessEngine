# DESCRIPTION: The part of the chess engine that generates the legal moves.

# 50726f6772616d6d696e6720697320627265616b696e67206f66206f6e652062696720696d706f
# 737369626c65207461736b20696e746f207365766572616c207665727920736d616c6c20706f73
# 7369626c65207461736b732e

# NOTE:
# ================
# This file is currently a work in progress. The original chessboard.py file has
# become overly bloated and is detrimental to the moral of the project. This new
# script is aimed at taking only the methods that pertain to the move gen, while
# separating the other components into their own scrips

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MAIN~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  #####  ####### ######  #######
 #     # #     # #     # #
 #       #     # #     # #
 #       #     # ######  #####
 #       #     # #   #   #
 #     # #     # #    #  #
  #####  ####### #     # #######


class _CoreMoveGenerator:
    """Contains the core methods that are used in the move generation."""

 #     # ####### #     # #######
 ##   ## #     # #     # #
 # # # # #     # #     # #
 #  #  # #     # #     # #####
 #     # #     #  #   #  #
 #     # #     #   # #   #
 #     # #######    #    #######

  #####  ####### #     # ####### ######     #    ####### ### ####### #     #
 #     # #       ##    # #       #     #   # #      #     #  #     # ##    #
 #       #       # #   # #       #     #  #   #     #     #  #     # # #   #
 #  #### #####   #  #  # #####   ######  #     #    #     #  #     # #  #  #
 #     # #       #   # # #       #   #   #######    #     #  #     # #   # #
 #     # #       #    ## #       #    #  #     #    #     #  #     # #    ##
  #####  ####### #     # ####### #     # #     #    #    ### ####### #     #


class MoveGenerator:
    """Generates the possible moves based off the rules of chess."""

    def __init__(self):
        return None
