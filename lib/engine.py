# DESCRIPTION: Contains the heavy-lifting of the engine: search & evaluation.

# 50726f6772616d6d696e6720697320627265616b696e67206f66206f6e652062696720696d706f
# 737369626c65207461736b20696e746f207365766572616c207665727920736d616c6c20706f73
# 7369626c65207461736b732e

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MAIN~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from copy import copy, deepcopy
from lib import chessboard, core, movegenerator, pieces


class Node(object):
    """A node in the tree search. Stores the moves."""

    def __init__(self, movepair, parent=None):
        """Stores information about the node."""
        if parent != None: self.moves = copy(parent.moves)
        else: self.moves = list()

        self.moves += [movepair]
        return None

    def __str__(self):
        """Prints the move instructions."""
        return str(self.moves)

    def __eq__(self, other):
        """Compares nodes."""
        return self.moves == other.moves


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

    def pawnstructurescore(self, board):
        """Looks at the pawn structure and gives a net score.

        Refer to the list below which states the specific scores allocated to
        a side based on their pawn structure. Note that the values are for white
        thus black's values would simply be the negative.

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
        # Define the pawn structure calculator (to remove duplicate code.)
        def pawnstructurevalue(pawnpositions, colour):
            """Gets the value of the pawn structure."""
            if colour == 'white': multiplier = 1
            elif colour == 'black': multiplier = -1
            else: raise core.ColourError()

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

        # Then execute the code for both white and black pawns.
        whitepawns = board.findpiece(pieces.PawnPiece, 'white')
        blackpawns = board.findpiece(pieces.PawnPiece, 'black')

        netscore = 0
        if whitepawns:
            netscore += pawnstructurevalue(whitepawns, 'white')
        if blackpawns:
            netscore += pawnstructurevalue(blackpawns, 'black')
        return netscore

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
        netscore += self.pawnstructurescore(board)
        return netscore


class ChessEngine:
    """The brains of the computer. It searches and evaluates positions."""

    def __init__(self):
        self.movegenerator = movegenerator.MoveGenerator
        self.evaluate = Evaluator.evaluate
        return None

    def search_single(self, board, maxdepth, startcolour):
        """Looks only one move deep (used as placeholder until proper search
        function is complete)."""
        results = list()

        generator = self.movegenerator(board)
        moves = generator.generatemovelist(startcolour)
        for move in moves:
            newboard = board.duplicateboard()
            newboard.move(*move)
            parentnode = Node(move)

            newgenerator = self.movegenerator(newboard)
            newmoves = generator.generatemovelist(core.oppositecolour(startcolour))
            print move, newmoves

            for newmove in newmoves:
                results.append(Node(newmove, parentnode))
        return results

    def search(self, board, maxdepth, startcolour, _depth=0, _parent=None, nodes=list()):
        """Generates the moves up to depth for colour."""
        while _depth < maxdepth:
            # Find moves for board state.
            generator = self.movegenerator(board)
            moves = generator.generatemovelist(startcolour)
            print moves

            # Make move recursively
            for move in moves:
                newboard = board.duplicateboard()
                newboard.move(*move)
                parentnode = Node(move, parent=_parent)
                print parentnode

                if _depth == maxdepth:
                    nodes.append(parentnode)
                    continue
                else:
                    return self.search(
                        newboard,
                        maxdepth, core.oppositecolour(startcolour),
                        _depth+0.5,  # HACK: Half step so we measure both black's and white's moves.
                        parentnode, nodes
                    )
        return nodes

    def netattackers(self, board, position):
        """Looks at the position on the board and sees the number of attackers
        and defenders. This is used to see if there is a possibiliy of exchange."""
        try:
            piececolour = board[position].colour
        except AttributeError:
            raise core.EmptySquareError(position)

        endmoves = lambda l: map(lambda x: x[1], l)
        movegen = self.movegenerator(board)

        defenderendmoves = endmoves(
            movegen.basicmoves(piececolour, defendingmoves=True))
        attackerendmoves = endmoves(
            movegen.basicmoves(core.oppositecolour(piececolour)))
        return attackerendmoves.count(position) - defenderendmoves.count(position)
