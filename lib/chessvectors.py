# DESCRIPTION: The class for vectors.

# 50726f6772616d6d696e6720697320627265616b696e67206f66206f6e652062696720696d706f
# 737369626c65207461736b20696e746f207365766572616c207665727920736d616c6c20706f73
# 7369626c65207461736b732e

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MAIN~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from lib import core

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
            projectedvector = map(lambda x, y: x*y, integers, shortestvector)

            if tuple(projectedvector) == longestvector: return True
            else: return False
        except AttributeError:
            raise AttributeError("Other must be a vector.")

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
            if isinstance(other, int):
                return self._scalar_multiply(other)
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
            return Vector(*self._multiply(other))
        except AttributeError:
            raise TypeError("Other must be a vector.")

    def __rmul__(self, other):
        """Reversed __mul__ method."""
        try:
            return Vector(*self._multiply(other))
        except AttributeError:
            raise TypeError("Other must be a vector.")

    def __abs__(self):
        """Magnitude of the vector"""
        return int(self._mag())  # Only return integer lengths.
