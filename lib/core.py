# DESCRIPTION: Contains all of the code, classes and functions corresponding to
# the board and pieces.

# 50726f6772616d6d696e6720697320627265616b696e67206f66206f6e652062696720696d706f
# 737369626c65207461736b20696e746f207365766572616c207665727920736d616c6c20706f73
# 7369626c65207461736b732e

# DEVELOPMENT LOG:
#    19/11/16: Initialized core file. Added core functionallity such as sanity
# checks, add/remove/move methods.
#    20/11/16: Added a getitem method.
#    26/12/16: Fixed line length so that it corresponded to PEP8 guidlines.
# Revisited the project, conducting some cleaning while I was in.
#    27/12/16: Added setion titles for easy viewing (Chess Board and Pieces).
# Creaed methods to check if the index is valid and if the move is legal in the
# base piece class. Added a method to call the position of the piece, such it is
# a private attribute. Added a method to move the pieces. Added special methods
# to handle if the move is valid in the rook and king classes.
#    28/12/16: Fixed RookPiece class's identification of the current rank.
#    29/12/16: Fixed QueenPiece class's isvalidmove method, which was allowing
# certain moves that were illegal. Added PawnPiece class. Did some refactoring
# on pieces to remove repeat code. Added special PawnPiece move method to handle
# pawn pushing.
#    30/12/16: Added an extra parameter to the chess pieces to determine if it
# is a player's piece or the computer's piece. Added assertion test in ChessBoard
# class and a isplayerpiece check in BasePiece. Created two brand new classes
# of ChessBoard: one for a default game and one for debugging/user created.
#    31/12/16: Overhauled (what seems like) entire progress so far. As a result
# bugs in finding legal moves, now the entire engine runs on coordinate
# notation but stores and calculates on index notation. Did some major
# refactoring of the entire core file to remove redunant functions, rename other
# functions and remove hackish code. Added vector class, which was reused from
# a previous project.
#    01/01/17: Moved the ChessBoard class to new script. Made the chess pieces
# now only use vectors in all methods, but allows use of indices for backwards
# compatability.
#    03/01/17: Made _toindex and _tovector work for both index and vector
# arguments. Refactored the multiplication methods in vectors. Lots of small
# fixes.
#    04/01/17: Added symbol method for the chess pieces.
#    05/01/17: Small fixes over all code.
#    !!NOTE!! This development log has been made redundant now that it is on
# GitHub.

# NOTES:
# The board should have its internal structure (i.e. the locations) completely
# unaccessable from outside observers.

# The minimap headings are made using the "Banner" design.

# TODO:
# - Check to see if pieces between start and final destination when moving.

# REVIEW: Do I need all of these imports?
from lib.exceptions import *
from copy import deepcopy

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MAIN~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


  #####  ####### #     # ####### ######     #    #
 #     # #       ##    # #       #     #   # #   #
 #       #       # #   # #       #     #  #   #  #
 #  #### #####   #  #  # #####   ######  #     # #
 #     # #       #   # # #       #   #   ####### #
 #     # #       #    ## #       #    #  #     # #
  #####  ####### #     # ####### #     # #     # #######

 ####### #     # #     #  #####  ####### ### ####### #     #  #####
 #       #     # ##    # #     #    #     #  #     # ##    # #     #
 #       #     # # #   # #          #     #  #     # # #   # #
 #####   #     # #  #  # #          #     #  #     # #  #  #  #####
 #       #     # #   # # #          #     #  #     # #   # #       #
 #       #     # #    ## #     #    #     #  #     # #    ## #     #
 #        #####  #     #  #####     #    ### ####### #     #  #####


def xor(x, y):
    """An XOR gate for two arguments"""
    if ((x and y) or (not x and not y)):
        return False
    else:
        return True

def xnor(x, y):
    """An XNOR gate for two arguments."""
    return (not xor(x, y))

def onlyone(iterable):
    """Returns true if only one of the items in iterable is true."""
    count = 0
    for ii in iterable:
        if count > 1:
            return False
        elif ii:
            count += 1
            continue
    return True

def convert(indexorcoordinateorvector,
            tocoordinate=False, toindex=False, tovector=False):
    """Makes the input into a coordinate, vector or index, regardless of form.

    This monolithic function basically forces either an index or a
    coordinate into the specified form. This is the translator required to
    calculate possible moves using vector attacks. See docs for more
    information into the algoithims used and why this method is required."""
    # TODO: Flesh out this docsting.
    # Sanity checks.
    assert any([tocoordinate, toindex, tovector]), \
        "Specify the output using the optional arguments."
    assert onlyone([tocoordinate, toindex, tovector]), \
        "The output is only a coordinate, vector or an index, not multiple."

    # Define functions
    def isindex(x):
        return isinstance(x, int)
    def iscoordinate(x):
        return (isinstance(x, (tuple, list)) and len(x) == 2)
    def isvector(x):
        return isinstance(x, Vector)

    # Convert to desired form:
    x = indexorcoordinateorvector  # Shorthand notation.
    if tocoordinate:  # Convert to coordinate.
        if isindex(x):
            return (x/8, x % 8)
        elif isvector(x):
            return x.tupleform()
        elif iscoordinate(x):
            return x
    elif toindex:  # Convert to index.
        if isindex(x):
            return x
        elif isvector(x):
            x = x.tupleform()
            return x[0]*8 + x[1]
        elif iscoordinate(x):
            return x[0]*8 + x[1]
    elif tovector:  # Convert to vector.
        if isindex(x):
            return Vector(x/8, x % 8)
        elif iscoordinate(x):
            return Vector(*x)
        elif isvector(x):
            return x
    else:
        raise TypeError("Passed item is none of the allowed options.")
    # If x isn't a vector, index or coordinate:
    raise TypeError("The item to be converted isn't a valid type.")
    return None

def convertlist(lst, **kwargs):
    """Same call as convert but for a list. Basically, a shortcut call."""
    return map(lambda x: convert(x, **kwargs), lst)

def readablelistof(lst):
    """Prints the list as expected, instead of a jumble of instances.

    This is to be called when dealing with pieces or vectors."""
    string = ''
    for item in lst:
        string += str(item) + ', '
    return '[' + string[:-2] + ']'


 #     # #######  #####  ####### ####### ######   #####
 #     # #       #     #    #    #     # #     # #     #
 #     # #       #          #    #     # #     # #
 #     # #####   #          #    #     # ######   #####
  #   #  #       #          #    #     # #   #         #
   # #   #       #     #    #    #     # #    #  #     #
    #    #######  #####     #    ####### #     #  #####

class Vector:
    """Creates a 2D vector for the chess engine.

    This class contains all of the necessary backbone to do vector calculations.
    It has the ability to add/subtract vectors, scalar multiply and do both the
    dot product and the cross product. All of these abilities have native use
    with the various operators.

    Public Methods
    ================
    The public methods are using the various operation symbols.

    Private Methods
    ================
    :isvector: Returns true or false depending if the object passed is an
        instance of the Vector class.
    :eq: Determines if two vectors are equal.
    :ne: Determines if the two vectors are unequal.
    :add: Adds vectors together. Use the +/- characters.
    :scalar_multiply: Scale a vector. Use the * character.
    :dot: Dots vectors together. Use the * character.

    Notes
    ================
    Currently no notes.
    """
    # TODO: Fix class to "Beg for Forgiveness" mentality.

    def __init__(self, x, y):
        """Initialise the Vector class."""
        self.vector = (x, y)

    def __str__(self):
        """String representation of vector."""
        return str(self.vector)

    def tupleform(self):
        """A more obvious way of getting the vector as a tuple."""
        return self.vector

    def intmultipleof(self, other):
        """See if self is an integer multiple of other."""
        # FIXME: This is a clusterfuck.
        try:
            intdivide = map(lambda x, y: x / y, self.vector, other.vector)
            projected_selfvector = map(lambda i: intdivide[0]*i, other.vector)
            if intdivide[0] != intdivide[1]:
                return False
            elif tuple(projected_selfvector) != self.vector:
                return False
            else:
                return True
        except AttributeError:
            raise AttributeError("Other must be a vector.")

    def unitvector(self):
        """Fetches a quasi-unit vector of the current vector."""
        # REVIEW: Can this be made neater?
        if (self.vector[0] == 0 or self.vector[1] == 0):
            return Vector(*tuple(map(lambda i: int(i/self._mag()), self.vector)))
        elif abs(self.vector[0]) == abs(self.vector[1]):
            return Vector(*tuple(map(lambda i: int(i/abs(i)), self.vector)))
        else:
            raise NotImplementedError("This call doesn't work for this vector.")

    def _scalar_multiply(self, intscalar):
        """Core for the scalar multiplication."""
        return map(lambda i: intscalar*i, self.vector)

    def _add(self, other):
        """Core for the vector addition."""
        return map(lambda i, j: i+j, self.vector, other.vector)

    def _dot(self, other):
        """Core for the dot product operation."""
        return reduce(lambda x, y: x+y,
            map(lambda k, l: k*l, self.vector, other.vector)
        )

    def _mag(self):
        """Core for the magnitude of the vector."""
        return reduce(lambda x, y: x+y, map(lambda ii: ii**2, self.vector))**0.5

    def _multiply(self, other):
        """Core for the multiplication."""
        try:
            if isinstance(other, int):
                return Vector(*self._scalar_multiply(other))
            else:
                return self._dot(other)
        except AttributeError:
            raise AttributeError("Other must be a vector.")

    def __eq__(self, other):
        """Implement equality operations."""
        try:
            return self.vector == other.vector
        except AttributeError:
            raise AttributeError(
                "Equality can only be determined against another vector.")

    def __ne__(self, other):
        """Implement unequality operations."""
        try:
            return self.vector != other.vector
        except AttributeError:
            raise AttributeError(
                "Equality can only be determined against another vector.")

    def __add__(self, other):
        """Allows for vector addition with the use of the + character."""
        try:
            return Vector(*self._add(other))
        except AttributeError:
            raise AttributeError("Other must be a vector.")

    def __radd__(self, other):
        """Reversed __add__ method."""
        try:
            return Vector(*self._add(other))
        except AttributeError:
            raise AttributeError("Other must be a vector.")

    def __iadd__(self, other):
        """ The += operation."""
        try:
            return Vector(*self._add(other))
        except AttributeError:
            raise AttributeError("Other must be a vector.")

    def __sub__(self, other):
        """Allows for vector subtraction with the use of the - character."""
        try:
            return Vector(*self._add(-1*other))
        except AttributeError:
            raise AttributeError("Other must be a vector.")

    def __rsub__(self, other):
        """Reversed __sub__ method."""
        try:
            return Vector(*self._add(-1*other))
        except AttributeError:
            raise AttributeError("Other must be a vector.")

    def __isub__(self, other):
        """The -= operation."""
        try:
            return Vector(*self._add(-1*other))
        except AttributeError:
            raise AttributeError("Other must be a vector.")

    def __mul__(self, other):
        """Allows for dot product and scalar multiplication."""
        return self._multiply(other)

    def __rmul__(self, other):
        """Reversed __mul__ method."""
        return self._multiply(other)

    def __abs__(self):
        """Magnitude of the vector"""
        return self._mag()


 ######  ### #######  #####  #######  #####
 #     #  #  #       #     # #       #     #
 #     #  #  #       #       #       #
 ######   #  #####   #       #####    #####
 #        #  #       #       #             #
 #        #  #       #     # #       #     #
 #       ### #######  #####  #######  #####


class BasePiece:
    """The class all chess pieces inherit from."""

    def __init__(self, playerpiece, startpositionindex, notationsymbol,
                 validmovevectors, onlyunitvectors=False):
        # Sanity checks.
        assert isinstance(onlyunitvectors, bool), \
            "'onlyunitvectors' parameter must be true or false."
        assert isinstance(playerpiece, bool), \
            "The piece either belongs to the user (True) or does not (False). " \
            "Please pass a boolean arguement."

        # Assignment of attributes.
        self._positionvector = self._tovector(startpositionindex)
        self._notationsymbol = notationsymbol
        self._validmovevectors = self._checkAllAreVectors(validmovevectors)
        self._onlyunitvectors = onlyunitvectors
        self.isplayerpiece = playerpiece
        return None

    def __str__(self):
        """How to print the class if called as a string."""
        return self.__class__.__name__

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

    def __init__(self, playerpiece, startpositionindex):
        BasePiece.__init__(self, playerpiece, startpositionindex, 'R',
            validmovevectors=(
                Vector(1,0), Vector(0,1), Vector(-1, 0), Vector(0, -1))
        )
        return None


class KnightPiece(BasePiece):
    """The class for the knight."""

    def __init__(self, playerpiece, startpositionindex):
        BasePiece.__init__(self, playerpiece, startpositionindex, 'N',
            validmovevectors=(
                Vector(2, 1), Vector(1, 2), Vector(2, -1), Vector (1, -2),
                Vector(-2, -1), Vector(-1, -2), Vector(-2, 1), Vector (-1, 2)),
            onlyunitvectors=True
        )
        return None


class BishopPiece(BasePiece):
    """The class for the bishop."""

    def __init__(self, playerpiece, startpositionindex):
        BasePiece.__init__(self, playerpiece, startpositionindex, 'B',
            validmovevectors=(
                Vector(1, 1), Vector(1, -1), Vector(-1, -1), Vector(-1, 1))
        )
        return None

class QueenPiece(BasePiece):
    """The class for the queen."""

    def __init__(self, playerpiece, startpositionindex):
        BasePiece.__init__(self, playerpiece, startpositionindex, 'Q',
            validmovevectors=(
                Vector(1, 0), Vector(0, 1), Vector(1, 1), Vector(1, -1),
                Vector(-1, 0), Vector(0, -1), Vector(-1, -1), Vector(-1, 1))
        )
        return None


class KingPiece(BasePiece):
    """The class for the King"""

    def __init__(self, playerpiece, startpositionindex):
        BasePiece.__init__(self, playerpiece, startpositionindex, 'K',
            validmovevectors=(
                Vector(1, 0), Vector(0, 1), Vector(1, 1), Vector(1, -1),
                Vector(-1, 0), Vector(0, -1), Vector(-1, -1), Vector(-1, 1)),
            onlyunitvectors=True
        )
        return None


class PawnPiece(BasePiece):
    """The very special class for the pawn."""
    # WIP: Still be fixed.

    def __init__(self, playerpiece, startpositionindex):
        if playerpiece:
            movevector = Vector(1, 0)
            self._captureleft = Vector(1, -1)
            self._captureright = Vector(1, 1)
        else:
            movevector = Vector(-1, 0)
            self._captureleft = Vector(-1, -1)
            self._captureright = Vector(-1, 1)

        BasePiece.__init__(self, playerpiece, startpositionindex, "",
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
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.:.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
