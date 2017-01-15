# DESCRIPTION: Contains each different chess piece.

# 50726f6772616d6d696e6720697320627265616b696e67206f66206f6e652062696720696d706f
# 737369626c65207461736b20696e746f207365766572616c207665727920736d616c6c20706f73
# 7369626c65207461736b732e

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MAIN~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from lib import core

class BasePiece:
    """The class all chess pieces inherit from."""

    def __init__(self, colour, notationsymbol, moveunitvectors, crawler=False):
        # Sanity checks.
        assert isinstance(crawler, bool), \
            "'crawler' parameter must be true or false."
        assert colour in ('white', 'black'), \
            "The colour of the piece must be 'white' or 'black'"

        # Assignment of attributes.
        self.colour = colour

        if colour == 'white':
            notationsymbol = notationsymbol.upper()
        else:
            notationsymbol = notationsymbol.lower()
        self.notationsymbol = notationsymbol

        for vec in moveunitvectors:
            self._assertisvector(vec)
        self.moveunitvectors = moveunitvectors
        self.crawler = crawler
        return None

    def __str__(self):
        """How to print the class if called as a string."""
        return self.__class__.__name__

    def __eq__(self, other):
        """Controls equality. Checks to see if the same type."""
        return other.__class__.__name__ == self.__class__.__name__

    def __ne__(self, other):
        """Controls inequality."""
        return other.__class__.__name__ != self.__class__.__name__

    @staticmethod
    def _assertisvector(vector):
        """A sanity check to make sure all items in vectorlist are vectors."""
        try:
            assert isinstance(item, core.Vector)
        except AssertionError:
            raise AssertionError("The item %r isn't a vector." % item)

    def type(self):
        """Returns the class of which this piece inherits from."""
        return eval(self.__class__.__name__)

    def distancefromselfto(self, moveto):
        # TODO: Move this method into somewhere else, or remove it.
        """Find the relative vector between board index and current position."""
        return core.convert(moveto, tovector=True) - self._positionvector


class RookPiece(BasePiece):
    """The class for the Rook."""

    def __init__(self, colour):
        BasePiece.__init__(self, colour, 'R',
            moveunitvectors=(
                Vector(1,0), Vector(0,1), Vector(-1, 0), Vector(0, -1))
        )
        return None


class KnightPiece(BasePiece):
    """The class for the knight."""

    def __init__(self, colour):
        BasePiece.__init__(self, colour, 'N',
            moveunitvectors=(
                Vector(2, 1), Vector(1, 2), Vector(2, -1), Vector (1, -2),
                Vector(-2, -1), Vector(-1, -2), Vector(-2, 1), Vector (-1, 2)),
            crawler=True
        )
        return None


class BishopPiece(BasePiece):
    """The class for the bishop."""

    def __init__(self, colour):
        BasePiece.__init__(self, colour, 'B',
            moveunitvectors=(
                Vector(1, 1), Vector(1, -1), Vector(-1, -1), Vector(-1, 1))
        )
        return None

class QueenPiece(BasePiece):
    """The class for the queen."""

    def __init__(self, colour):
        BasePiece.__init__(self, colour, 'Q',
            moveunitvectors=(
                Vector(1, 0), Vector(0, 1), Vector(1, 1), Vector(1, -1),
                Vector(-1, 0), Vector(0, -1), Vector(-1, -1), Vector(-1, 1))
        )
        return None


class KingPiece(BasePiece):
    """The class for the King"""

    def __init__(self, colour):
        BasePiece.__init__(self, colour, 'K',
            moveunitvectors=(
                Vector(1, 0), Vector(0, 1), Vector(1, 1), Vector(1, -1),
                Vector(-1, 0), Vector(0, -1), Vector(-1, -1), Vector(-1, 1)),
            crawler=True
        )
        return None


class PawnPiece(BasePiece):
    """The very special class for the pawn."""

    def __init__(self, colour):
        if colour == 'white':
            movevector = Vector(1, 0)
            self._captureleft = Vector(1, -1)
            self._captureright = Vector(1, 1)
        elif colour == 'black':
            movevector = Vector(-1, 0)
            self._captureleft = Vector(-1, -1)
            self._captureright = Vector(-1, 1)

        BasePiece.__init__(self, colour, "P",
            moveunitvectors=(movevector,), crawler=True
        )
        return None

    def isvalidcapture(self, movetopos):
        """Pawns capture in a strange fashion. This method controls that."""
        # REVIEW: Do I ever call this method?
        diffvec = self.distancefromselfto(movetopos)
        capturemoves = (self._captureleft, self._captureright)
        return (diffvec in self._validcapturemoves)
