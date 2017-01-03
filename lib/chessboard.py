# DESCRIPTION: Contains all of the code, classes and functions corresponding to
# the board.

# 50726f6772616d6d696e6720697320627265616b696e67206f66206f6e652062696720696d706f
# 737369626c65207461736b20696e746f207365766572616c207665727920736d616c6c20706f73
# 7369626c65207461736b732e

# DEVELOPMENT LOG:
#    01/01/17: Initialized chessboard.py, the new script that controls the
# board. Was moved from core as it was becoming much larger then I anticipated
# and made the core.py script too large. Changed the ChessBoard class from being
# a monolithic class by breaking it apart into components and used the OOP
# composition to rebuild it.
#    03/01/17: Lots of small changes/aesthetics fixes. ASCII headings were added
# to help organise the script better. Added some more private attributes to the
# chessboard that control move history and notation generation. Refactord some
# code to make it more readable. Initalised the UI and GUI classes for the
# chessboard.

from lib.exceptions import *
from lib.core import *

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MAIN~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  #####  ####### #     # ######  ####### #     # ####### #     # #######  #####
 #     # #     # ##   ## #     # #     # ##    # #       ##    #    #    #     #
 #       #     # # # # # #     # #     # # #   # #       # #   #    #    #
 #       #     # #  #  # ######  #     # #  #  # #####   #  #  #    #     #####
 #       #     # #     # #       #     # #   # # #       #   # #    #          #
 #     # #     # #     # #       #     # #    ## #       #    ##    #    #     #
  #####  ####### #     # #       ####### #     # ####### #     #    #     #####


class _ChessBoardCore:
    """The grandfather class to all of the components of the chessboard.

    This class is all of the very basic components of the board. It contains
    the low-level board representation, assertion checks and conversions between
    different input styles by the front-end of the engine."""

    def __init__(self):
        """Initialises the board."""
        # Needed for the core operations:
        self._board = [None] * 64
        self.playerturn = True

        # Needed for UI:
        self._movehistory = list()
        self._ranksymbols = tuple(map(lambda x: str(x), range(1, 8+1)))
        self._filesymbols = tuple('abcdefgh')

    def __getitem__(self, pos):
        """Controls calling the piece at a position on the board like a list."""

        errormsg = "The board is read either as a index from 0 to 63 or a " \
        "tuple/list that specifies the row and column index."
        try:
            return self._board[pos]
        except TypeError:
            try:  # If it wasn't an integer see if it is a coordinate:
                assert len(pos) == 2, errormsg
                return self._board[self.convert(pos, toindex=True)]
            except TypeError:
                raise TypeError(errormsg)  # If that still doesn't work it's fucked.

    def _onlyone(self, iterable):
        """Returns true if only one of the items in iterable is true."""
        # REVIEW: I know there is a better way to write this.
        count = 0
        for ii in iterable:
            if ii:
                count += 1
        return count == 1

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
        assert self._onlyone([tocoordinate, toindex, tovector]), \
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
                return Vector(x/8, x % 8)
            elif iscoordinate(x):
                return Vector(*x)
            elif isvector(x):
                return x
        else:
            raise TypeError("Passed item is none of the allowed options.")

    @staticmethod
    def _assertPositionOnBoard(indices):
        """Assert that the indices called are on the board as a sanity check."""
        # TODO: Rewrite this method to use try-chains instead of if-chains.
        if isinstance(indices, Vector):
            assert all([0 <= x <= 7 for x in indices.vector]), \
                "Row/Column index is out the the board range."
        elif isinstance(indices, (list, tuple)):
            for ii in indices:
                assert isinstance(ii, int), \
                    "The value(s) passed are not integers."
                assert 0 <= ii <= 7, \
                    "Row/Column index is out the the board range."
        elif isinstance(indices, int):
            assert 0 <= indices <= 63, "The integer passed must be between 0 to 63."
        else:
            raise TypeError("Please pass an index, coordinate or vector.")
        return None

    def _assertIsUnoccupied(self, index):
        """Asserts that the square is free and unoccupied."""
        try:
            assert self._board[index] == None, "The target square is occupied."
        except IndexError:
            raise IndexError("The index used is off the board!")
        return None

    def _assertIsOccupied(self, index):
        """Asserts that the square is occupied."""
        try:
            assert self._board[index] != None, "The target square is unoccupied."
        except IndexError:
            raise IndexError("The index used is off the board!")
        return None

    def _isoccupied(self, index):
        """Similar to _assertIsUnoccupied but just returns a True/False only."""
        return self._board[index] != None


class _ChessBoardPieces(_ChessBoardCore):
    """The component that handles the pieces on the board."""

    def piecesbetween(self, start, end):
        """Find the pieces between the start and end index."""
        startvec = self.convert(start, tovector=True)
        endvec = self.convert(end, tovector=True)
        unitrelvec = (endvec - startvec).unitvector()
        currentposvec = startvec

        pieceslist = list()
        while currentposvec != endvec:
            currentposvec += unitrelvec
            currentposindex = self.convert(currentposvec, toindex=True)
            if self._isoccupied(currentposindex):
                pieceslist.append(self._board[currentposindex])
        return pieceslist

    def addpiece(self, piece, indexcoordinate, playerpiece=True, force=False):
        """Add a new piece to the board."""
        # Converting into index and sanity checks.
        index = self.convert(indexcoordinate, toindex=True)
        if not force: self._assertIsUnoccupied(index)  # Allow forced overwriting.
        self._assertPositionOnBoard(index)

        # Now add the piece.
        self._board[index] = piece(playerpiece, startpositionindex=index)
        return None

    def emptysquare(self, indexcoordinate):
        """Removes a piece from the board."""
        index = self.convert(indexcoordinate, toindex=True)
        self._assertPositionOnBoard(index)
        self._board[index] = None

    def move(self, startindexcoordinate, endindexcoordinate):
        """Move a piece around on the board."""
        assert startindexcoordinate != endindexcoordinate, \
            "To move the piece, the start and end points must be different."
        startindex = self.convert(startindexcoordinate, toindex=True)
        endindex = self.convert(endindexcoordinate, toindex=True)

        self._assertPositionOnBoard(startindex)
        self._assertPositionOnBoard(endindex)
        self._assertIsUnoccupied(endindex)
        self._board[endindex] = self._board[startindex]
        self._board[startindex] = None
        return None

    def capture(self, startindexcoordinate, endindexcoordinate):
        """Captures a piece on the board. Shorter call then emptysquare & move."""
        startindex = self.convert(startindexcoordinate, toindex=True)
        endindex = self.convert(endindexcoordinate, toindex=True)
        self._assertPositionOnBoard(startindex)
        self._assertPositionOnBoard(endindex)
        self._assertIsOccupied(endindex)

        self.emptysquare(endindex)
        self.move(startindex, endindex)
        return None


class _ChessBoardUI(_ChessBoardCore):
    """Controls interacting with the user as well as algebraic notation."""

    def displayboard(self):
        """Prints the board using ASCII graphics"""
        return

    def movehistory(self):
        """Fetches the list with the move history."""
        return self._movehistory

    def _positiontonotation(self, indexorcoordinateorvector):
        posvector = self.convert(indexorcoordinateorvector, tovector=True)
        (rank_, file_) = posvector.tupleform()
        return self._filesymbols[file_] + self._ranksymbols[rank_]

    def _notationtoposition(self, notationstring,
                            indexform=False, vectorform=False):
        try:
            assert any([indexform, vectorform]), \
                "Specify the output using the optional arguments."
            assert self._onlyone([indexform, vectorform]), \
                "The output is only a vector or an index, not both."
            (file_, rank_) = tuple(notationstring)
            iFile = self._filesymbols.index(file_)
            iRank = self._ranksymbols.index(rank_)
            if indexform:
                return iRank*8 + iFile
            elif vectorform:
                return Vector(iRank, iFile)
            else:
                raise RuntimeError
        except ValueError as e:
            raise
        except AssertionError as e:
            raise
        except RuntimeError as e:
            raise RuntimeError("This shouldn't be raised! Something went wrong.")

    def addmovetohistory(self, piece, endposition, movewascapture=False):
        """Writes a move into the game history."""
        # BUG: Sometimes in a game you need to specify which piece moved/took
        # a piece. This method currently doesn't account for that.
        # BUG: Doesn't work with pawn captures.
        try:
            piecesymbol = piece._notationsymbol
            if movewascapture:
                capturesymbol = 'x'
                if isinstance(piece, PawnPiece):  # HACK: Fix captures for pawns.
                    pos = piece.position(vectorform=True)
                    filestring = self._filesymbols[pos.vector[1]]
                    capturesymbol = filestring + capturesymbol
            else:
                capturesymbol = ''
            movesymbol = self._positiontonotation(endposition)

            notationstring = piecesymbol + capturesymbol + movesymbol
            self._movehistory.append(notationstring)
        except AttributeError as err1:
            raise
        except TypeError as err2:
            raise

    def processplayersmove(self, userstring):
        """Figure out what the hell the user is trying to say.

        Currently this method only has the ability to read in algebraic notation
        to specify where a piece goes. Eventually this method will become
        redundant when the GUI is developed.

        The method returns the piece that is to move, along with the position
        the piece will move to."""
        # WIP: UI is really hard to make.
        if len(userstring) == 2:  # If just moving a pawn. e.g. e4
            piecetomove = PawnPiece
            endindex = self._notationtoposition(userstring, indexform=True)

        whichpiece = userstring[0]  # The first character is the chess piece.
        return None



class _ChessBoardGUI(_ChessBoardCore):
    """The component that handles drawing up the board on the screen."""
    # WIP: First get UI working, test to make sure the engine works then try to
    # make GUI.
    pass


class _ChessBoardEngine(_ChessBoardCore):
    """The component that handles all of the engine behind the board."""
    # WIP: This is not even close to being started, but is placeholder for when
    # it will begin to be developed.
    pass


  #####  #     # #######  #####   #####  ######  #######    #    ######  ######
 #     # #     # #       #     # #     # #     # #     #   # #   #     # #     #
 #       #     # #       #       #       #     # #     #  #   #  #     # #     #
 #       ####### #####    #####   #####  ######  #     # #     # ######  #     #
 #       #     # #             #       # #     # #     # ####### #   #   #     #
 #     # #     # #       #     # #     # #     # #     # #     # #    #  #     #
  #####  #     # #######  #####   #####  ######  ####### #     # #     # ######


class ChessBoard(_ChessBoardCore, _ChessBoardPieces, _ChessBoardEngine,
                 _ChessBoardUI, _ChessBoardGUI):
    """The parent of all public classes for the chessboard.

    Since the board embraces composition OOP mentality, this class is where the
    board gets 'assembled' together. This parent class conatins all of the
    public calls the engine/front-end needs to worry about. The children of the
    class are for different game modes of the engine, such as default matches,
    puzzles or special game modes.

    Public methods
    ===============
    - __getitem__: This is using [] on the class to fetch the piece at that
      position. Can be either a integer from 0 to 63 or a list/tuple of length
      two that specifies the row index and column index.
    - convert: ***TO BE COMPLETED***
    - addpiece: Adds a piece to the board.
    - emptysquare: Clears a square on the board.
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
        """Initalise the chessboard."""
        # Call the __init__ of all the parents.
        _ChessBoardCore.__init__(self)


class DefaultChessBoard(ChessBoard):
    """The board that is created for a normal game of chess."""

    def __init__(self):
        """Initialise a basic chess board."""
        ChessBoard.__init__(self)
        self._setupboard(playeriswhite=True)
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
        for index in range(8, 15+1):
            self.addpiece(PawnPiece, index, playerpiece=x)

        # Add the black pieces.
        for index in range(48,55+1):
            self.addpiece(PawnPiece, index, playerpiece=(not x))
        for index in range(56, 63+1):
            self.addpiece(backline[index-56], index, playerpiece=(not x))
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
            self.addpiece(
                callableversionof(piece),
                piece.position(),
                playerpiece=piece.isplayerpiece()
            )
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.:.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
