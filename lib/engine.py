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
        self.generator = movegenerator.MoveGenerator(self.board)
        return None

    def makemoves(self, board, startcolour):
        """Iterates over movelist and finds the set of moves one level deeper."""
        # First get all possible moves for startcolour.
        oldgen = movegenerator.MoveGenerator(board)
        movelist = oldgen.generatemovelist(startcolour)

        # Now iterate over them, find next level of moves and add to dict.
        movedboards = list()
        for themove in movelist:
            simboard = board.duplicateboard()
            simboard.move(*themove)
            movedboards.append(simboard)
        return movedboards

    def brutesearch(self, movesdeep, startcolour):
        """Searchs so many moves 'deep' and returns a list of possible moves."""
        return None


class EngineEvaluation:
    """This is the evaluation part of the engine, which determines if the move
    is any good."""

    def __init__(self, boardstate):
        self.board = deepcopy(boardstate)
        self.generator = movegenerator.MoveGenerator(boardstate)
        return None

    def evaluateposition(self):
        """Looks at the board conditions and returns a number based on how good
        the position is.

        MATERIAL ADVANTAGE
        ====================
            King Value = infinity (100 000)
            Queen Value = 9 000
            Rook Value = 5 000
            Bishop Value = 2 500
            Knight Value = 2 500
            Pawn Value = 1 000

        MOBILITY ADVANTAGE
        ====================
            Mobility Value = Number of moves x 100

        PAWN STRUCTURE
        ================
            Pair pawns = +200
            Backward pawn = -75
            Isolated pawn = -400
            Doubled pawns = -250
            Trippled pawns = -600
            Protected by two pawns = +150
            Protected by one pawn = +75
        """
        def piecediff(piecetype):
            """Find if one side is up pieces (+ for white, - for black)"""
            whitepieces = len(self.board.findpiece(piecetype, 'white'))
            blackpieces = len(self.board.findpiece(piecetype, 'black'))
            return whitepieces - blackpieces
        # Initalise variables.
        whitepawns = self.board.findpiece(pieces.PawnPiece, 'white')
        blackpawns = self.board.findpiece(pieces.PawnPiece, 'black')

        # >> First find the value based on piece value. <<
        positionvalue = (
            piecediff(pieces.KingPiece)*100000 +
            piecediff(pieces.QueenPiece)*9000 +
            piecediff(pieces.RookPiece)*5000 +
            piecediff(pieces.BishopPiece)*2500 +
            piecediff(pieces.KnightPiece)*2500 +
            (len(whitepawns) - len(blackpawns))*1000  # Used to save overhead.
        )

        # >> Next find value based on mobility. <<
        positionvalue += len(self.generator.generatemovelist('white'))*100
        positionvalue -= len(self.generator.generatemovelist('black'))*100

        # >> Get a value based on pawn structure for white. <<
        if whitepawns:
            whitepawnvectors = core.convertlist(whitepawns, tovector=True)
            whitepawnranks, whitepawnfiles = zip(*map(lambda x: x.vector, whitepawnvectors))
            for pos, posvec in zip(whitepawns, whitepawnvectors):
                # Look for pair pawns.
                if (pos+1) in whitepawns:
                    positionvalue += 200

                # Look for isolated and protected pawns.
                posrank, posfile = posvec.vector
                if posfile-1 in whitepawnranks and posfile+1 in whitepawnranks:
                    positionvalue += 150
                elif posfile-1 in whitepawnranks or posfile+1 in whitepawnranks:
                    positionvalue += 50
                else:
                    positionvalue -= 400

                # Look for doubled or trippled pawns.
                if whitepawnfiles.count(posfile) == 2:
                    positionvalue -= 250/2  # Because it will be counted twice.
                elif whitepawnfiles.count(posfile) >= 3:
                    positionvalue -= 200  # Lose 200 everytime it is counted.

                # Determine if the pawn is proteced.
                if (posvec-core.Vector(1, 1)) in whitepawnvectors:
                    positionvalue += 75
                if (posvec-core.Vector(1, -1)) in whitepawnvectors:
                    positionvalue += 75

            # Look for (2 or less) backward pawns.
            if whitepawnranks.count(min(whitepawnranks)) <= 2:
                positionvalue -= 75

        # >> Get a value based on pawn structure for black. <<
        if blackpawns:
            blackpawnvectors = core.convertlist(blackpawns, tovector=True)
            blackpawnranks, blackpawnfiles = zip(*map(lambda x: x.vector, blackpawnvectors))
            for pos, posvec in zip(blackpawns, blackpawnvectors):
                # Look for pair pawns.
                if (pos+1) in blackpawns:
                    positionvalue += -200

                # Look for isolated and protected pawns.
                posrank, posfile = posvec.vector
                if posfile-1 in blackpawnranks and posfile+1 in blackpawnranks:
                    positionvalue += -150
                elif posfile-1 in blackpawnranks or posfile+1 in blackpawnranks:
                    positionvalue += -50
                else:
                    positionvalue -= -400

                # Look for doubled or trippled pawns.
                if blackpawnfiles.count(posfile) == 2:
                    positionvalue -= -250/2  # Because it will be counted twice.
                elif blackpawnfiles.count(posfile) >= 3:
                    positionvalue -= -200  # Lose 200 everytime it is counted.

                # Determine if the pawn is proteced.
                if (posvec-core.Vector(-1, 1)) in blackpawnvectors:
                    positionvalue += -75
                if (posvec-core.Vector(-1, -1)) in blackpawnvectors:
                    positionvalue += -75

            # Look for (2 or less) backward pawns.
            if blackpawnranks.count(min(blackpawnranks)) <= 2:
                positionvalue -= -75

        # >> Finally, return the value but divided by 1000 <<
        return positionvalue/1000.0



class ChessEngine:
    """The class that combines the two separate components to work together."""

    def __init__(self, boardstate):
        self.search = EngineSearch(boardstate)
        self.evaluate = EngineEvaluation(boardstate)
        return None
