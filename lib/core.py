# DESCRIPTION: Contains all of the code, classes and functions corresponding to
# the board and pieces.

# 50726f6772616d6d696e6720697320627265616b696e67206f66206f6e652062696720696d706f
# 737369626c65207461736b20696e746f207365766572616c207665727920736d616c6c20706f73
# 7369626c65207461736b732e

# EXPLAINATION:
# The board works by allocating an index to each square, starting at the bottom
# left and moving right. Thus the white left rook is at index 0, the white king
# is at index 4 and the black queen at index 59.
# TODO: Add this description to the class itself.

# DEVELOPMENT LOG:
#    19/11/16: Initialized core file. Added core functionallity such as sanity
# checks, add/remove/move methods.
#    20/11/16: Added a getitem method.
#    26/12/16: Fixed line length so that it corresponded to PEP8 guidlines.
# Revisited the project, conducting some cleaning while I was in.
#    27/12/16: Added setion titles for easy viewing (Chess Board and Pieces).
# Creaed methods to check if the index is valid and if the move is legal in the
# base piece class. Added a method to call the postion of the piece, such it is
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

# NOTES:
# The board should have its internal structure (i.e. the locations) completely
# unaccessable from outside observers.

# The minimap headings are made using the "Banner" design.

# TODO:
# - Check to see if pieces between start and final destination when moving.

from lib.exceptions import *
from lib.vectors import Vector

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MAIN~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
            elif projected_selfvector != self.vector:
                return False
            else:
                return True
        except AttributeError:
            raise AttributeError("Other must be a vector.")

    @staticmethod
    def _assertIsVector(obj):
        """Assert that the object passed is a vector."""
        assert isinstance(obj, Vector), "The object passed is not a vector."
        return None

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

    def __mul__(self, other):
        """Allows for dot product and scalar multiplication."""
        try:
            if isinstance(other, int):
                return Vector(*self._scalar_multiply(other))
            else:
                return Vector(*self._dot(other))
        except AttributeError:
            raise AttributeError("Other must be a vector.")

    def __rmul__(self, other):
        """Reversed __mul__ method."""
        try:
            if isinstance(other, int):
                return Vector(*self._scalar_multiply(other))
            else:
                return Vector(*self._dot(other))
        except AttributeError:
            raise AttributeError("Other must be a vector.")

    def __abs__(self):
        """Magnitude of the vector"""
        return reduce(lambda x, y: x+y, map(lambda ii: ii**2, self.vector))**0.5


  #####  #     # #######  #####   #####     ######  #######    #    ######  ######
 #     # #     # #       #     # #     #    #     # #     #   # #   #     # #     #
 #       #     # #       #       #          #     # #     #  #   #  #     # #     #
 #       ####### #####    #####   #####     ######  #     # #     # ######  #     #
 #       #     # #             #       #    #     # #     # ####### #   #   #     #
 #     # #     # #       #     # #     #    #     # #     # #     # #    #  #     #
  #####  #     # #######  #####   #####     ######  ####### #     # #     # ######


class ChessBoard:
    """The parent class that controls the behaviour of the chess board.

    The reason for using a parent class on the chess board is simple: it will
    contain most of the methods and attributes but allows for flexability if
    different types of boards are to be initalised, such as setting up the board
    for puzzles or special game modes.

    Public methods
    ===============
    - __getitem__: This is using [] on the class to fetch the piece at that
      postion. Can be either a integer from 0 to 63 or a list/tuple of length
      two that specifies the row index and column index.
    - convert: ***TO BE COMPLETED***
    - addpiece: Adds a piece to the board.
    - makesquareempty: Removes a piece from the board (if one is there).
    - move: Moves a piece around the board.
    - capture: Captures a piece on the board.


    Private methods
    ================
    - assertIsChessPiece: Makes sure that the arguement is one of the chess
      pieces defined in this program. In reality, it checks to see if the class
      inherits from BasePiece.
    - assertPositionOnBoard: Asserts that the index passed is valid (i.e. is
      between 0 to 63).
    - assertIsUnoccupied: Asserts that the square passed is, in fact, unoccupied.

    """

    def __init__(self):
        """Initialises the board."""
        self.__board = [None] * 64
        self.playerturn = True

    def __getitem__(self, pos):
        """Controls calling the piece at a position on the board like a list."""

        errormsg = "The board is read either as a index from 0 to 63 or a " \
        "tuple/list that specifies the row and column index."
        try:
            return self.__board[pos]
        except TypeError:
            try:  # If it wasn't an integer see if it is a coordinate:
                assert len(pos) == 2, errormsg
                return self.__board[self.coordinate2index(pos)]
            except TypeError:
                raise TypeError(errormsg)  # If that still doesn't work it's fucked.

    @staticmethod
    def _assertIsChessPiece(piece):
        """Assert that the piece passed inherits from the BasePiece class."""
        assert isinstance(piece, BasePiece), \
               "The piece passed did not inherit from BasePiece."
        return None

    @staticmethod
    def _assertPositionOnBoard(indices):
        """Assert that the indices called are on the board as a sanity check."""
        # TODO: Rewrite this method to use try-chains instead of if-chains.
        if isinstance(indices, Vector):
            assert all([0 <= x <= 7 for x in indices])
        elif isinstance(indices, (list, tuple)):
            for ii in indices:
                assert isinstance(ii, int), "The value(s) passed are not integers."
                assert 0 <= ii <= 7, "Row/Column index is out the the board range."
        elif isinstance(indices, int):
            assert 0 <= indices <= 63, "The integer passed must be between 0 to 63."
        return None

    def _assertIsUnoccupied(self, index):
        """Asserts that the square is free and unoccupied."""
        try:
            assert self.__board[index] == None, "The target square is occupied."
        except IndexError:
            raise IndexError("The index used is off the board!")
        return None

    def convert(self, indexorcoordinateorvector,
                tocoordinate=False, toindex=False, tovector=False):
        """Makes the input into a coordinate, vector or index, regardless of form.

        This monolithic function basically forces either an index or a
        coordinate into the specified form. This is the translator required to
        calculate possible moves using vector attacks. See docs for more
        information into the algoithims used and why this method is required."""
        # TODO: Write notes on why this method is required.
        # Sanity checks.
        assert any([tocoordinate, toindex, tovector]), \
            "Specify the output using the optional arguments."
        assert [tocoordinate, toindex, tovector].count() == 1, \
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
        self._assertPositionOnBoard(x)
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
                return Vector((x/8, x % 8))
            elif iscoordinate(x):
                return Vector(*x)
            elif isvector(x):
                return x
        else:
            raise RuntimeError("Passed item is none of the allowed options.")

    def addpiece(self, piece, indexcoordinate, playerpiece=True, force=False):
        """Add a new piece to the board."""
        # Converting into index.
        index = self.convert(indexcoordinate, toindex=True)

        # Sanity checks.
        if not force: self._assertIsUnoccupied(index)  # Allow forced overwriting.
        self._assertPositionOnBoard(index)
        self._assertIsChessPiece(piece)

        # Now add the piece.
        self.__board[index] = piece(playerpiece, startpositionindex=index)
        return None

    def makesquareempty(self, indexcoordinate):
        """Removes a piece from the board."""
        # Converting into index.
        index = self.convert(indexcoordinate, toindex=True)

        self._assertPositionOnBoard(index)
        self.__board[index] = None

    def move(self, startindexcoordinate, endindexcoordinate):
        """Move a piece around on the board."""
        # Converting into index.
        startindex = self.convert(startindexcoordinate, toindex=True)
        endindex = self.convert(endindexcoordinate, toindex=True)

        self._assertPositionOnBoard((startindex, endindex))
        self._assertIsUnoccupied(endindex, 'The end square is occupied.')
        self.__board[endindex] = self.__board[startindex]
        self.__board[startindex] = None
        return None

    def capture(self, startindexcoordinate, endindexcoordinate):
        """Captures a piece on the board. A shorter call then remove then move."""
        # Converting into index.
        startindex = self.convert(startindexcoordinate, toindex=True)
        endindex = self.convert(endindexcoordinate, toindex=True)

        self.makesquareempty(endindex)
        self.move(startindex, endindex)
        return None


class DefaultChessBoard(ChessBoard):
    """The board that is created for a normal game of chess."""

    def __init__(self):
        """Initialise a basic chess board."""
        ChessBoard.__init__(self)
        self._setupboard()
        return None

    def _setupboard(self, playeriswhite):
        """Set up the chess board by placing the pieces at the correct spots."""
        # Initalise variables & sanity checks.
        assert isinstance(playeriswhite, bool), \
            "Specify if the player is white (true) or black (false)."
        x = playeriswhite  # Shorthand notation.
        backline = [RookPiece, KnightPiece, BishopPiece, QueenPiece, KingPiece,
                    BishopPiece, KnightPiece, RookPiece]  # Backline order.

        # Add the white pieces.
        for index in range(0, 7+1):
            self.addpiece(backline[index], index, playerpiece=x)
        for index in range(8,15+1):
            self.addpiece(PawnPiece, index, playerpiece=x)

        # Add the black pieces.
        for index in range(48,55+1):
            self.addpiece(PawnPiece, index, playerpiece=(not x))
        for index in range(56, 63+1):
            self.addpiece(backline[index], index, playerpiece=(not x))
        return None


class UserDefinedChessBoard(ChessBoard):
    """The board that prompts the user to set up the board how he/she likes."""

    def __init__(self, piecelist):
        """Initalise the chess board."""
        ChessBoard.__init__(self)
        self.defineboard(piecelist)
        return None

    def defineboard(self, piecelist):
        """Allows the user to pass in a list of pieces to setup the chess board.

        By passing in a list of ready-made chess pieces, one is able to generate
        a different board then that of a normal chess game. The method takes the
        intialised pieces and extracts the information it needs to generate a
        fresh copy on each, thus maintaining some resemblance of encapsulation.
        """
        def callableversionof(thisclass):
            return thisclass.__class__.__name__

        for piece in piecelist:
            self._assertIsChessPiece(piece)
            self.addpiece(
                callableversionof(piece),
                piece.position(),
                playerpiece=piece.isplayerpiece()
            )


 ######  ### #######  #####  #######  #####
 #     #  #  #       #     # #       #     #
 #     #  #  #       #       #       #
 ######   #  #####   #       #####    #####
 #        #  #       #       #             #
 #        #  #       #     # #       #     #
 #       ### #######  #####  #######  #####


class BasePiece:
    """The class all chess pieces inherit from."""

    def __init__(self, playerpiece, startpositionindex, validmovevectors,
                 onlyunitvectors=False):
        # Sanity checks.
        assert isinstance(onlyunitvectors, bool), \
            "'onlyunitvectors' parameter must be true or false."
        assert isinstance(playerpiece, bool), \
            "The piece either belongs to the user (True) or does not (False). " \
            "Please pass a boolean arguement."

        # Assignment of attributes.
        self._postion = startpositionindex
        self._validmovevectors = self._checkAllAreVectors(validmovevectors)
        self._onlyunitvectors = onlyunitvectors
        self._playerpiece = playerpiece
        return None

    def _checkAllAreVectors(self, vectorlist):
        """A sanity check to make sure all items in vectorlist are vectors."""
        for item in vectorlist:
            assert isinstance(item, Vector), "There are non-vectors in the list."
        return vectorlist

    @staticmethod
    def _tovector(index):
        """Converts an index on the board into a vector."""
        return Vector((index/8, index % 8))

    def distanceto(self, moveto):
        """Find the relative vector between board index and current position."""
        return self._tovector(movetopos) - self._tovector(self._postion)

    def isvalidmove(self, movetopos):
        """Checks that the move specified is valid."""
        diffvec = self.distanceto(movetopos))
        if not self._onlyunitvectors:
            if any([diffvec.intmultipleof(x) for x in self._validmovevectors]):
                return True
            else:
                return False
        elif self._onlyunitvectors:
            return (diffvec in self._validmovevectors)

    def isplayerpiece(self):
        """Returns true if player piece, false if not."""
        return self._playerpiece

    def postion(self, index=True, vector=False):
        """Returns the position of the piece. Used for encapsulation purposes."""
        if index: return self._postion
    elif vector: return self._tovector(self._postion)

    def move(self, index):
        """Moves the piece to new index."""
        if not self.isvalidindex(index):
            raise IndexError
        elif not self.isvalidmove(index):
            raise IllegalMoveError
        else:
            self._postion = index
        return None


class RookPiece(BasePiece):
    """The class for the Rook."""

    def __init__(self, playerpiece, startpositionindex):
        BasePiece.__init__(self, playerpiece, startpositionindex,
            validmovevectors=(
                Vector(1,0), Vector(0,1), Vector(-1, 0), Vector(0, -1))
        )
        return None


class KnightPiece(BasePiece):
    """The class for the knight."""

    def __init__(self, playerpiece, startpositionindex):
        BasePiece.__init__(self, playerpiece, startpositionindex,
            validmovevectors=(
                Vector(2, 1), Vector(1, 2), Vector(2, -1), Vector (1, -2),
                Vector(-2, -1), Vector(-1, -2), Vector(-2, 1), Vector (-1, 2)),
            onlyunitvectors=True
        )
        return None


class BishopPiece(BasePiece):
    """The class for the bishop."""

    def __init__(self, startpositionindex):
        BasePiece.__init__(self,
            playerpiece, startpositionindex,
            validmovevectors=(
                Vector(1, 1), Vector(1, -1), Vector(-1, -1), Vector(-1, 1))
        )
        return None

class QueenPiece(BasePiece):
    """The class for the queen."""

    def __init__(self, playerpiece, startpositionindex):
        BasePiece.__init__(self,
            playerpiece, startpositionindex,
            validmovevectors=(
                Vector(1, 0), Vector(0, 1), Vector(1, 1), Vector(1, -1),
                Vector(-1, 0), Vector(0, -1), Vector(-1, -1), Vector(-1, 1))
        )
        return None


class KingPiece(BasePiece):
    """The class for the King"""

    def __init__(self, playerpiece, startpositionindex):
        BasePiece.__init__(self,
            playerpiece, startpositionindex,
            validmovevectors=(
                Vector(1, 0), Vector(0, 1), Vector(1, 1), Vector(1, -1),
                Vector(-1, 0), Vector(0, -1), Vector(-1, -1), Vector(-1, 1)),
            onlyunitvectors=True
        )
        return None


class PawnPiece(BasePiece):
    """The very special class for the pawn."""

    def __init__(self, playerpiece, startpositionindex):
        BasePiece.__init__(self,
            playerpiece, startpositionindex,
            validmovevectors=(Vector(1, 0), Vector(2, 0)), onlyunitvectors=True
        )
        self._validcapturemoves = (Vector(1, 1), Vector(1, -1))
        return None

    def isvalidcapture(self, movetopos):
        """Pawns capture in a strange fashion. This method controls that."""
        diffvec = self.distanceto(movetopos)
        return (diffvec in self._validcapturemoves)

    def move(self, index):
        """Pawns move in a strange fashion, and are controlled here."""
        if not self.isvalidindex(index):
            raise IndexError
        elif not self.isvalidmove(index):
            raise IllegalMoveError
        else:
            # If pawn moves, it can't push (again) so overwrite validmovevectors.
            self._validmovevectors = (Vector(1, 0),)
            self._postion = index
        return None
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.:.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
