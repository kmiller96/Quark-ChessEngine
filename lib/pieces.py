# DESCRIPTION: Contains each different chess piece.

# 50726f6772616d6d696e6720697320627265616b696e67206f66206f6e652062696720696d706f
# 737369626c65207461736b20696e746f207365766572616c207665727920736d616c6c20706f73
# 7369626c65207461736b732e

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MAIN~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from lib import core

class BasePiece(object):
    """The class all chess pieces inherit from.

    Since all of the chess pieces behave nearly identically, bar their legal
    moves, all of the pieces inherit from this class. It controls things like
    how comparisons between pieces are made and how they are created. For the
    most part however they are just containers for other classes to use easily.

    PUBLIC ATTRIBUTES
    ==================
    :type: Returns the class name.

    PUBLIC METHODS
    ===============
    :__init__: Takes in parameters of the piece colour, its notationsymbol,
               its legal moves and an optional parameter on if it can only move
               one unit of the legal moves.
    :__str__:  Prints the name of the piece. If not overwritten in the children
               it uses the class name.
    :__eq__:   Determines if the other is the same piece (as defined by class,
               not by instance).
    :__ne__:   Same as the __eq__ class.

    PRIVATE METHODS
    ================
    :_assertisvector: Asserts that the value passed is a vector. Returns
                      TypeError if that isn't the case.
    """

    def __init__(self, colour, notationsymbol, moveunitvectors, crawler=False):
        """"Initialise the piece. Performs sanity checks on inputs."""
        # Sanity checks.
        try:
            assert isinstance(crawler, bool)
        except AssertionError:
            raise TypeError("'crawler' parameter must be true or false.")

        try:
            assert colour.lower() in ('white', 'black')
        except AssertionError:
            raise TypeError("The colour of the piece must be 'white' or 'black'")
        except AttributeError:
            raise TypeError("The colour must be a string of either 'white' or 'black'")

        # Assignment of attributes.
        self.colour = colour.lower()

        if colour == 'white': notationsymbol = notationsymbol.upper()
        else: notationsymbol = notationsymbol.lower()
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
        try:
            return other.type == self.type
        except AttributeError:
            return False

    def __ne__(self, other):
        """Controls inequality. Just not-version of __eq__."""
        try:
            return other.type != self.type
        except AttributeError:
            return True


    @staticmethod
    def _assertisvector(vector):
        """A sanity check to make sure variable is a vectors."""
        try:
            assert isinstance(vector, core.Vector)
        except AssertionError:
            raise TypeError("The item %r isn't a vector, instead %r." % (vector, type(vector)))

    @property
    def type(self):
        """Returns the class of which this piece inherits from."""
        return eval(self.__class__.__name__)


class RookPiece(BasePiece):
    """The class for the Rook."""

    def __init__(self, colour):
        super(self.__class__, self).__init__(
            colour=colour, notationsymbol='R',
            moveunitvectors=(
                core.Vector(1,0),
                core.Vector(0,1),
                core.Vector(-1, 0),
                core.Vector(0, -1)
            )
        )
        return None


class KnightPiece(BasePiece):
    """The class for the knight."""

    def __init__(self, colour):
        super(self.__class__, self).__init__(
            colour=colour, notationsymbol='N', crawler=True,
            moveunitvectors=(
                core.Vector(2, 1), core.Vector(1, 2),
                core.Vector(2, -1), core.Vector (1, -2),
                core.Vector(-2, -1), core.Vector(-1, -2),
                core.Vector(-2, 1), core.Vector (-1, 2)
            )
        )
        return None


class BishopPiece(BasePiece):
    """The class for the bishop."""

    def __init__(self, colour):
        super(self.__class__, self).__init__(
            colour=colour, notationsymbol='B',
            moveunitvectors=(
                core.Vector(1, 1),
                core.Vector(1, -1),
                core.Vector(-1, -1),
                core.Vector(-1, 1)
            )
        )
        return None

class QueenPiece(BasePiece):
    """The class for the queen."""

    def __init__(self, colour):
        super(self.__class__, self).__init__(
            colour=colour, notationsymbol='Q',
            moveunitvectors=(
                core.Vector(1, 0), core.Vector(0, 1),
                core.Vector(1, 1), core.Vector(1, -1),
                core.Vector(-1, 0), core.Vector(0, -1),
                core.Vector(-1, -1), core.Vector(-1, 1)
            )
        )
        return None


class KingPiece(BasePiece):
    """The class for the King"""

    def __init__(self, colour):
        super(self.__class__, self).__init__(
            colour=colour, notationsymbol='K', crawler=True,
            moveunitvectors=(
                core.Vector(1, 0), core.Vector(0, 1),
                core.Vector(1, 1), core.Vector(1, -1),
                core.Vector(-1, 0), core.Vector(0, -1),
                core.Vector(-1, -1), core.Vector(-1, 1)
            )
        )
        return None


class PawnPiece(BasePiece):
    """The very special class for the pawn."""

    def __init__(self, colour):
        if colour == 'white': movevector = core.Vector(1, 0)
        elif colour == 'black': movevector = core.Vector(-1, 0)
        else: raise core.ColourError()

        super(self.__class__, self).__init__(
            colour=colour, notationsymbol="P", crawler=True,
            moveunitvectors=(movevector,)
        )
        return None
