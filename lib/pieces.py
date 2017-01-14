# DESCRIPTION: Contains each different chess piece.

# 50726f6772616d6d696e6720697320627265616b696e67206f66206f6e652062696720696d706f
# 737369626c65207461736b20696e746f207365766572616c207665727920736d616c6c20706f73
# 7369626c65207461736b732e

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MAIN~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BasePiece:
    """The class all chess pieces inherit from."""

    def __init__(self, colour, startpositionindex, notationsymbol,
                 validmovevectors, onlyunitvectors=False):
        # Sanity checks.
        assert isinstance(onlyunitvectors, bool), \
            "'onlyunitvectors' parameter must be true or false."
        assert colour in ('white', 'black'), \
            "The colour of the piece must be 'white' or 'black'"

        # Assignment of attributes.
        self._positionvector = self._tovector(startpositionindex)
        self._notationsymbol = notationsymbol
        self._validmovevectors = self._checkAllAreVectors(validmovevectors)
        self._onlyunitvectors = onlyunitvectors
        self.colour = colour
        return None

    def __str__(self):
        """How to print the class if called as a string."""
        return self.__class__.__name__

    def _sametype(self, other):
        """Sees if the other is the same type of piece as this one."""
        return other.__class__.__name__ == self.__class__.__name__

    def __eq__(self, other):
        """Controls equality."""
        return self._sametype(other)

    def __ne__(self, other):
        """Controls inequality."""
        return not self._sametype(other)

    @staticmethod
    def _checkAllAreVectors(vectorlist):
        """A sanity check to make sure all items in vectorlist are vectors."""
        try:
            for item in vectorlist:
                assert isinstance(item, Vector)
            return vectorlist
        except TypeError as error1:
            raise TypeError("Arg1 must be an iterable.")
        except AssertionError as error2:
            raise AssertionError("There are non-vectors in the list.")

    @staticmethod
    def _tovector(indexorvector):
        """Converts an index on the board into a vector."""
        try:
            if isinstance(indexorvector, Vector):
                vector = indexorvector
                return vector
            else:
                index = indexorvector
                assert isinstance(index, int)
                assert 0 <= index <= 63
        except AssertionError as error:
            raise TypeError("The argument must be an index from 0 to 63.")
        else:
            return Vector(index/8, index % 8)

    @staticmethod
    def _toindex(indexorvector):
        """Converts a vector on the board to an index."""
        try:
            if isinstance(indexorvector, int):
                index = indexorvector
                return index
            else:
                vector = indexorvector
                return vector.vector[0]*8 + vector.vector[1]
        except AttributeError as error:
            raise TypeError("The argument must be a vector.")

    def piecetype(self):
        """Returns the class of which this piece inherits from."""
        # NOTE: This has no catches in place for bad inputs!
        return eval(self.__class__.__name__)

    def symbol(self, forasciiboard=False):
        """Fetches the symbol of the piece. Optional argument is a WIP."""
        return self._notationsymbol

    def distancefromselfto(self, moveto):
        """Find the relative vector between board index and current position."""
        return self._tovector(moveto) - self._positionvector

    def possiblemoves(self):
        """Gets possibles moves for piece if board was empty.

        The chess board controls whether the move is legal or not in terms of
        occupacy, pins etc. but this method just returns possible moves that
        each piece could take if the board was completely empty.
        """
        # Quick definition of function.
        def vectoronboard(vectorclass):
            """Checks to see if a vector is on the board."""
            vector = vectorclass.vector
            return (0 <= vector[0] <= 7 and 0 <= vector[1] <= 7)

        # Main execution.
        possiblemoveslist = list()
        for unitvector in self._validmovevectors:
            posvector = self._positionvector + unitvector
            while vectoronboard(posvector):  # Break if vector now off the board.
                possiblemoveslist.append(posvector)
                if self._onlyunitvectors: break  # Don't loop if onlyunitvectors.
                posvector += unitvector
        return possiblemoveslist

    def position(self, indexform=False, vectorform=False):
        """Returns the position of the piece. Used for encapsulation purposes."""
        assert (indexform or vectorform), \
            "Specify either index-form or vector-form of returned position."
        assert not (indexform and vectorform), \
            "Can only return either index-form or vector-form."

        if indexform: return self._toindex(self._positionvector)
        elif vectorform: return self._positionvector
        else: raise RuntimeError("Something went wrong.")

    def movetoindex(self, index):
        """Moves the piece to new index."""
        self._positionvector = self._tovector(index)
        return None

    def movetovector(self, vector):
        """Moves the piece to the position specified by the vector."""
        self._positionvector = vector
        return None


class RookPiece(BasePiece):
    """The class for the Rook."""

    def __init__(self, colour, startpositionindex):
        BasePiece.__init__(self, colour, startpositionindex, 'R',
            validmovevectors=(
                Vector(1,0), Vector(0,1), Vector(-1, 0), Vector(0, -1))
        )
        return None


class KnightPiece(BasePiece):
    """The class for the knight."""

    def __init__(self, colour, startpositionindex):
        BasePiece.__init__(self, colour, startpositionindex, 'N',
            validmovevectors=(
                Vector(2, 1), Vector(1, 2), Vector(2, -1), Vector (1, -2),
                Vector(-2, -1), Vector(-1, -2), Vector(-2, 1), Vector (-1, 2)),
            onlyunitvectors=True
        )
        return None


class BishopPiece(BasePiece):
    """The class for the bishop."""

    def __init__(self, colour, startpositionindex):
        BasePiece.__init__(self, colour, startpositionindex, 'B',
            validmovevectors=(
                Vector(1, 1), Vector(1, -1), Vector(-1, -1), Vector(-1, 1))
        )
        return None

class QueenPiece(BasePiece):
    """The class for the queen."""

    def __init__(self, colour, startpositionindex):
        BasePiece.__init__(self, colour, startpositionindex, 'Q',
            validmovevectors=(
                Vector(1, 0), Vector(0, 1), Vector(1, 1), Vector(1, -1),
                Vector(-1, 0), Vector(0, -1), Vector(-1, -1), Vector(-1, 1))
        )
        return None


class KingPiece(BasePiece):
    """The class for the King"""

    def __init__(self, colour, startpositionindex):
        BasePiece.__init__(self, colour, startpositionindex, 'K',
            validmovevectors=(
                Vector(1, 0), Vector(0, 1), Vector(1, 1), Vector(1, -1),
                Vector(-1, 0), Vector(0, -1), Vector(-1, -1), Vector(-1, 1)),
            onlyunitvectors=True
        )
        return None


class PawnPiece(BasePiece):
    """The very special class for the pawn."""
    # WIP: Still be fixed.

    def __init__(self, colour, startpositionindex):
        if colour == 'white':
            movevector = Vector(1, 0)
            self._captureleft = Vector(1, -1)
            self._captureright = Vector(1, 1)
        elif colour == 'black':
            movevector = Vector(-1, 0)
            self._captureleft = Vector(-1, -1)
            self._captureright = Vector(-1, 1)

        BasePiece.__init__(self, colour, startpositionindex, "",
            validmovevectors=(movevector,), onlyunitvectors=True
        )
        self._validcapturemoves = (Vector(1, 1), Vector(1, -1))
        return None

    def symbol(self, forasciiboard=False):
        """A hack-fix of symbol in order to use the same method in the UI"""
        if forasciiboard: return 'P'
        else: return ""

    def isvalidcapture(self, movetopos):
        """Pawns capture in a strange fashion. This method controls that."""
        # REVIEW: Can this be moved into chessboard class?
        diffvec = self.distancefromselfto(movetopos)
        capturemoves = (self._captureleft, self._captureright)
        return (diffvec in self._validcapturemoves)
