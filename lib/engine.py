# DESCRIPTION: Contains the heavy-lifting of the engine: search & evaluation.

# 50726f6772616d6d696e6720697320627265616b696e67206f66206f6e652062696720696d706f
# 737369626c65207461736b20696e746f207365766572616c207665727920736d616c6c20706f73
# 7369626c65207461736b732e

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MAIN~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from copy import copy, deepcopy
from lib import chessboard, core, movegenerator, pieces

class Node:
    """Represents a node in the tree search."""

    def __init__(self, parent, move, state):
        # Initialise the node attributes.
        self.parent = parent
        self.move = move
        self.state = state

        # Add the move history.
        if self.parent == None: self.history = list()
        else: self.history = copy(self.parent.history)
        self.history.append(self.move)
        return None

    def __str__(self):
        return (str(self.parent) + ' -> ' + str(self.move)
                if self.parent != None else str(self.move))


class TreeStructure:
    """Represents the entire tree for the search algorithm."""

    def __init__(self):
        self.tree = list()
        self.treeboardstates = list()
        return None

    def addnode(self, node):
        """Adds a new node into the tree."""
        # REVIEW - How much overhead is the if statement adding?
        if node.state in self.treeboardstates: pass
        else:
            self.tree.append(node)
            self.treeboardstates.append(node.state)
        return None


class EngineSearch:
    """This is the search part of the engine, that finds moves to make."""

    def __init__(self, boardstate):
        self.board = deepcopy(boardstate)
        self.generator = movegenerator.MoveGenerator(self.board)
        self.finalpositions = TreeStructure()
        return None

    def fetchmoves(self, state, colour):
        """Gets the move list for colour in state, but cleaner."""
        return movegenerator.MoveGenerator(state).generatemovelist(colour)

    def brutesearch(self, movesdeep, startcolour, board=None, parent=None):
        """Searchs so many moves 'deep' and returns a list of possible moves."""
        # Sanity checking.
        if startcolour not in ('white', 'black'):
            raise core.ColourError()

        # Determine if you are in middle of recursive call or at the start.
        if board == None:
            board = self.board
        movelist = self.fetchmoves(board, startcolour)

        if movesdeep == 0:  # If you are deep enough:
            return None  # Exit this part of the tree.
        if not movelist:  # If there are no legal moves:
            return None

        for move in movelist:
            # Make the move on a simulated board.
            simboard = board.duplicateboard()
            simboard.move(*move)

            # Make a node of the position and add it to the tree if correct depth.
            movenode = Node(parent, move, simboard)
            if movesdeep == 1:
                self.finalpositions.addnode(movenode)

            nodemovelist = self.fetchmoves(
                movenode.state,
                core.oppositecolour(startcolour)
            )
            if nodemovelist:
                self.brutesearch(
                    movesdeep-1,
                    core.oppositecolour(startcolour),
                    board=simboard,
                    parent=movenode
                )
        return self.finalpositions

    def selectivesearch(self, movesdeep, startcolour, board=None, parent=None):
        """Does a selective search, which is far more efficient then brute
        search methods."""
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

        def pawnstructurevalue(pawnpositions, colour):
            """Gets the value of the pawn structure."""
            if colour == 'white':
                multiplier = 1
            elif colour == 'black':
                multiplier = -1
            else:
                raise core.ColourError()

            value = 0
            pawnvectors = core.convertlist(pawnpositions, tovector=True)
            pawnranks, pawnfiles = zip(*map(lambda x: x.vector, pawnvectors))
            for pos, posvec in zip(pawnpositions, pawnvectors):
                # Look for pair pawns.
                if (pos+1) in pawnpositions:
                    value += 200

                # Look for isolated and protected pawns.
                posrank, posfile = posvec.vector
                if posfile-1 in pawnranks and posfile+1 in pawnranks:
                    value += 150
                elif posfile-1 in pawnranks or posfile+1 in pawnranks:
                    value += 50
                else:
                    value -= 400

                # Look for doubled or trippled pawns.
                if pawnfiles.count(posfile) == 2:
                    value -= 250/2  # Because it will be counted twice.
                elif pawnfiles.count(posfile) >= 3:
                    value -= 200  # Lose 200 everytime it is counted.

                # Determine if the pawn is proteced.
                if (posvec-core.Vector(1, 1)) in pawnvectors:
                    value += 75
                if (posvec-core.Vector(1, -1)) in pawnvectors:
                    value += 75

            # Look for (2 or less) backward pawns.
            if pawnranks.count(min(pawnranks)) <= 2:
                value -= 75
            return value

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
            positionvalue += pawnstructurevalue(whitepawns, 'white')

        # >> Get a value based on pawn structure for black. <<
        if blackpawns:
            positionvalue += pawnstructurevalue(blackpawns, 'black')

        # >> Finally, return the value but divided by 1000 <<
        return positionvalue/1000.0



class ChessEngine:
    """The class that combines the two separate components to work together."""

    def __init__(self, boardstate):
        self.search = EngineSearch(boardstate)
        self.evaluate = EngineEvaluation(boardstate)
        return None
