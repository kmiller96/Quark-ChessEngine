# DESCRIPTION: A script that contains the small, miscellaneous functions and
# classes that are used everywhere. Also contains the vector class.

# 50726f6772616d6d696e6720697320627265616b696e67206f66206f6e652062696720696d706f
# 737369626c65207461736b20696e746f207365766572616c207665727920736d616c6c20706f73
# 7369626c65207461736b732e

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MAIN~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from copy import deepcopy


 ####### #     # #     #  #####  ####### ### ####### #     #  #####
 #       #     # ##    # #     #    #     #  #     # ##    # #     #
 #       #     # # #   # #          #     #  #     # # #   # #
 #####   #     # #  #  # #          #     #  #     # #  #  #  #####
 #       #     # #   # # #          #     #  #     # #   # #       #
 #       #     # #    ## #     #    #     #  #     # #    ## #     #
 #        #####  #     #  #####     #    ### ####### #     #  #####


def xor(x, y):
    """An XOR gate for two condition checks."""
    if ((x and y) or (not x and not y)):
        return False
    else:
        return True

def xnor(x, y):
    """An XNOR gate, which is simply a NOT XOR gate."""
    return (not xor(x, y))

def onlyone(iterable):
    """Returns true if only one of the items in iterable is true."""
    count = 0
    for ii in iterable:
        if count > 1:
            return False  # Stop iterating if there is more then one.
        elif ii:
            count += 1
            continue
    return True

def combinelists(*lists):
    """Combine lists together into a single list (i.e. unflatten lists)."""
    if any([not isinstance(x, list) for x in lists]):
        raise TypeError("Only lists can be used in this function.")
    return [element for sublist in lists for element in sublist]

def convert(indexorcoordinateorvector,
            tocoordinate=False, toindex=False, tovector=False):
    """Converts the input into a coordinate, vector or index.

    What this function does is it forces the input to change into the desired
    form, with each different form being useful in different conditions. This
    conversion is done via if-elif chains nested inside an if-elif-else chain.

    This method has catches in place: only one of the output types are allowed
    and if the input isn't an index, coordinate or vector it raises TypeErrors.

    PARAMETERS & RETURNS
    ======================
    :indexorcoordinateorvector: This parameter is the item to convert.
    :toindex:       Converts the input into an index.
    :tocoordinate:  Converts the input into the coordinate (rank, file).
    :tovector:      Converts the input into a vector define by core.Vector with
                    the x-component being the rank and the y-component being the
                    file.

    :return:        The input but in the forced form.

    EXAMPLES
    ======================
    How this function works on a basic level, input the square 'b1' as an index:
        >>> print core.convert(9, tocoordinate=True)
        >>> (1, 1)

        >>> print core.convert((1, 1), toindex=True)
        >>> 9

    Using the tovector parameter is harder to observe (as it is just a class):
        >>> print core.convert(9, tovector=True) == vector.Vector(1, 1)
        >>> True  # An equivalent call

        >>> a = core.convert(10, tovector=True)  # (1, 2)
        >>> b = core.convert(25, tovector=True)  # (3, 1)
        >>> print a + b
        >>> (4, 3)
    """
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
            return x.vector
        elif iscoordinate(x):
            return x
    elif toindex:  # Convert to index.
        if isindex(x):
            return x
        elif isvector(x):
            x = x.vector
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
    """Calls the __str__ method of classes, but structures it traditionally."""
    string = ''
    for item in lst:
        string += str(item) + ', '
    return '[' + string[:-2] + ']'


 ######  #######  #####  ### ####### ### ####### #     #
 #     # #     # #     #  #     #     #  #     # ##    #
 #     # #     # #        #     #     #  #     # # #   #
 ######  #     #  #####   #     #     #  #     # #  #  #
 #       #     #       #  #     #     #  #     # #   # #
 #       #     # #     #  #     #     #  #     # #    ##
 #       #######  #####  ###    #    ### ####### #     #

  #####  #          #     #####   #####
 #     # #         # #   #     # #     #
 #       #        #   #  #       #
 #       #       #     #  #####   #####
 #       #       #######       #       #
 #     # #       #     # #     # #     #
  #####  ####### #     #  #####   #####


class Position:
    """Store a position as a coordinate, vector or index.

    The position is stored internally in the class as all three types (since
    it isn't too heavy computationally) and allows the user to get any form of
    the position without any extensive calls.

    The only parameter of the initalisation of the class is a position, which
    can be either an index, coordinate or vector. There is a catch in place to
    ensure this is always true. Then the user can call any of the attributes to
    get the value.

    EXAMPLES
    ======================
    How this class works on a basic level, input the square 'b1' as an index:
        >>> x = core.Position(9)
        >>> x.index
        >>> 9
        >>> x.coordinate
        >>> (1, 1)
        >>> str(x.vector + 2*x.vector)
        >>> (3, 3)
    """

    def __init__(self, indexorcoordinateorvector):
        assert (
            self._isindex(indexorcoordinateorvector) or
            self._iscoordinate(indexorcoordinateorvector) or
            self._isvector(indexorcoordinateorvector)
        ), "The postion on the board is either a index, coordinate or vector."

        self._locked = False
        self.index = self._toindex(indexorcoordinateorvector)
        self.coordinate = self._tocoordinate(indexorcoordinateorvector)
        self.vector = self._tovector(indexorcoordinateorvector)
        self._locked = True

    def __setattr__(self, name, value):
        if name in ('index', 'coordinate', 'vector'):
            if self._locked:
                raise RuntimeError(
                "You are not permitted to make this change. Make a new instance"
                " of this class to change the postiion on the board."
                )
            else:
                pass
        else:
            pass
        self.__dict__[name] = value
        return None

    @staticmethod
    def _isindex(x):
        return isinstance(x, int)

    @staticmethod
    def _iscoordinate(x):
        return (isinstance(x, (tuple, list)) and len(x) == 2)

    @staticmethod
    def _isvector(x):
        return isinstance(x, Vector)

    def _toindex(self, x):
        if self._isindex(x):
            return x
        elif self._isvector(x):
            x = x.vector
            return x[0]*8 + x[1]
        elif self._iscoordinate(x):
            return x[0]*8 + x[1]
        return None

    def _tocoordinate(self, x):
        if self._isindex(x):
            return (x/8, x % 8)
        elif self._isvector(x):
            return x.vector
        elif self._iscoordinate(x):
            return x
        return None

    def _tovector(self, x):
        if self._isindex(x):
            return Vector(x/8, x % 8)
        elif self._iscoordinate(x):
            return Vector(*x)
        elif self._isvector(x):
            return x
        return None


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
    These vectors are specially talored to fit in with the chess engine, making
    the coordinates used only ever integers.

    INITALISATION PARAMETERS
    =========================
    :rank: The rank of the position
    :File: The file of the position

    PUBLIC METHODS
    ========================
    :+: Add vectors together.
    :-: Subtract vectors from one another.
    :*: Either scalar multiply or dot product vectors.
    :==: Equate vector components.
    :!=: Unequate vector components.
    :abs: Get the magnitude of the vector
    :parallelto: Boolean return on if a vector is parallel to self.
    :unitvector: Returns the quasi-unit vector of self.
    """

    def __init__(self, rank, File):
        """Initialise the Vector class."""
        try:
            assert isinstance(rank, int) and isinstance(File, int)
        except AssertionError:
            raise TypeError("Both initialisation parameters must be integers.")
        else:
            self.vector = (rank, File)
    def __str__(self):
        """String representation of vector."""
        return str(self.vector)

    def parallelto(self, other):
        """See if self is parallel to other."""
        try:
            # First exit if they are the same vector.
            if self.vector == other.vector:
                return True
            # Now find which vector is larger.
            elif self._mag() > other._mag():
                longestvector = self.vector
                shortestvector = other.vector
            elif self._mag() < other._mag():
                longestvector = other.vector
                shortestvector = self.vector

            # Now project the shorter vector onto the larger one.
            integers = map(lambda x, y: x / y, longestvector, shortestvector)
            if integers[0] != integers[1]:
                return False
            projectedvector = map(lambda x, y: x*y, integers, shortestvector)

            if tuple(projectedvector) == longestvector: return True
            else: return False
        except AttributeError:
            raise TypeError("Other must be a vector.")

    def unitvector(self):
        """Fetches a quasi-unit vector of the current vector."""
        if (self.vector[0] == 0 or self.vector[1] == 0):
            return Vector(*tuple(map(lambda i: int(i/self._mag()), self.vector)))
        elif abs(self.vector[0]) == abs(self.vector[1]):
            return Vector(*tuple(map(lambda i: int(i/abs(i)), self.vector)))
        else:
            raise NotImplementedError

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
            if isinstance(other, (int, float)):
                return Vector(*self._scalar_multiply(other))
            elif isinstance(other, Vector):
                return self._dot(other)
            else:
                raise AttributeError
        except AttributeError:
            raise TypeError("Other must be a vector or scalar.")

    def __eq__(self, other):
        """Implement equality operations."""
        try:
            return self.vector == other.vector
        except AttributeError:
            raise TypeError(
                "Equality can only be determined against another vector.")

    def __ne__(self, other):
        """Implement unequality operations."""
        try:
            return self.vector != other.vector
        except AttributeError:
            raise TypeError(
                "Equality can only be determined against another vector.")

    def __add__(self, other):
        """Allows for vector addition with the use of the + character."""
        try:
            return Vector(*self._add(other))
        except AttributeError:
            raise TypeError("Other must be a vector.")

    def __radd__(self, other):
        """Reversed __add__ method."""
        try:
            return Vector(*self._add(other))
        except AttributeError:
            raise TypeError("Other must be a vector.")

    def __iadd__(self, other):
        """ The += operation."""
        try:
            return Vector(*self._add(other))
        except AttributeError:
            raise TypeError("Other must be a vector.")

    def __sub__(self, other):
        """Allows for vector subtraction with the use of the - character."""
        try:
            return Vector(*self._add(-1*other))
        except AttributeError:
            raise TypeError("Other must be a vector.")

    def __rsub__(self, other):
        """Reversed __sub__ method."""
        try:
            return Vector(*self._add(-1*other))
        except AttributeError:
            raise TypeError("Other must be a vector.")

    def __isub__(self, other):
        """The -= operation."""
        try:
            return Vector(*self._add(-1*other))
        except AttributeError:
            raise TypeError("Other must be a vector.")

    def __mul__(self, other):
        """Allows for dot product and scalar multiplication."""
        try:
            return self._multiply(other)
        except AttributeError:
            raise TypeError("Other must be a vector.")

    def __rmul__(self, other):
        """Reversed __mul__ method."""
        try:
            return self._multiply(other)
        except AttributeError:
            raise TypeError("Other must be a vector.")

    def __abs__(self):
        """Magnitude of the vector"""
        return int(self._mag())  # Only return integer lengths.


 ####### #     #  #####  ####### ######  ####### ### ####### #     #  #####
 #        #   #  #     # #       #     #    #     #  #     # ##    # #     #
 #         # #   #       #       #     #    #     #  #     # # #   # #
 #####      #    #       #####   ######     #     #  #     # #  #  #  #####
 #         # #   #       #       #          #     #  #     # #   # #       #
 #        #   #  #     # #       #          #     #  #     # #    ## #     #
 ####### #     #  #####  ####### #          #    ### ####### #     #  #####


class IllegalMoveError(IndexError):
    """Called if the move is illegal for any reason."""

    def __init__(self, errormsg=None):
        if errormsg == None:
            errormsg = "The move supplied is not valid."
        IndexError.__init__(self, errormsg)

class ColourError(TypeError):
    """Raised if the colour specified isn't either white or black."""

    def __init__(self, errormsg=None):
        if errormsg == None:
            errormsg = "The colours of the players are either white or black."
        NameError.__init__(self, errormsg)

class UnknownPieceError(TypeError):
    """The piece passed is unknown (not in 'RNBQK')."""

    def __init__(self, errormsg=None):
        if errormsg == None:
            errormsg = "I don't know the piece passed."
        TypeError.__init__(self, errormsg)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.:.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
