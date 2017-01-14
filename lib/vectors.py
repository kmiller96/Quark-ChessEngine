# DESCRIPTION: The class for vectors.

# 50726f6772616d6d696e6720697320627265616b696e67206f66206f6e652062696720696d706f
# 737369626c65207461736b20696e746f207365766572616c207665727920736d616c6c20706f73
# 7369626c65207461736b732e

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MAIN~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from lib import core

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
