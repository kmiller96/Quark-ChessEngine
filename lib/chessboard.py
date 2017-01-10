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
#    04/01/17: Added basic UI and GUI functionality. Started adding move
# generation from the board state. Currently this is heavily untested however.
#    05/01/17: Added banner titles for each component of the chessboard, for
# easy navigation. Fixed the _allowedmovesforpiece method which now works for
# pieces by themselves on the board and for basic movements and captures.
#    !!NOTE!! This development log has been made redundant now that it is on
# GitHub.

from lib.exceptions import *
from lib.core import *

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MAIN~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


  #####  ####### ######  #######
 #     # #     # #     # #
 #       #     # #     # #
 #       #     # ######  #####
 #       #     # #   #   #
 #     # #     # #    #  #
  #####  ####### #     # #######


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

        # Needed for pieces:
        self._pieceslist = list()

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
            try:  # If it wasn't an integer then try to convert it:
                return self._board[self.convert(pos, toindex=True)]
            except TypeError:
                raise TypeError(errormsg)  # If that still doesn't work it's fucked.

    @staticmethod
    def _readablelistof(lst):
        """Prints the list as expected, instead of a jumble of instances.

        This is to be called when dealing with pieces or vectors."""
        string = ''
        for item in lst:
            string += str(item) + ', '
        return '[' + string[:-2] + ']'

    def _onlyone(self, iterable):
        """Returns true if only one of the items in iterable is true."""
        # REVIEW: I know there is a better way to write this.
        count = 0
        for ii in iterable:
            if ii:
                count += 1
        return count == 1

    @staticmethod
    def _piecesareonsameside(*pieces):
        """Checks to see if the passed pieces are all on the same side."""
        side = None
        for ii in pieces:
            if side is None:
                side = ii.isplayerpiece
                continue

            if ii.isplayerpiece == side:
                continue
            else:
                return False
        return True

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

    def convertlist(self, lst, **kwargs):
        """Same call as convert but for a list. Basically, a shortcut call."""
        return map(lambda x: self.convert(x, **kwargs), lst)

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


 ######  ### #######  #####  #######  #####
 #     #  #  #       #     # #       #     #
 #     #  #  #       #       #       #
 ######   #  #####   #       #####    #####
 #        #  #       #       #             #
 #        #  #       #     # #       #     #
 #       ### #######  #####  #######  #####


class _ChessBoardPiecesCore(_ChessBoardCore):
    """A class that stores the private methods of the ChessBoardPieces component."""

    def _piecesattackingking(self, playerking=True):
        """Find the pieces that are currently attacking the king in movelist."""
        try:
            kingposvec = self.convert(
                self.findpiece(KingPiece, playerside=playerking)[0], tovector=True)
        except IndexError:  # If there is no king on the board:
            return []  # Then he can't be attacked!
        oppositionmoves = self._fetchbasicmovesfor(side=(not playerking))

        piecesattacking = list()
        for piece, movetolist in oppositionmoves.iteritems():
            if kingposvec in movetolist:
                piecesattacking.append(piece)
        return piecesattacking

    def _piecesbetween(self, start, end):
        """Find the pieces between the start and end positions."""
        startvec = self.convert(start, tovector=True)
        endvec = self.convert(end, tovector=True)
        unitrelvec = (endvec - startvec).unitvector()
        currentposvec = startvec + unitrelvec

        pieceslist = list()
        while currentposvec != endvec:
            currentposindex = self.convert(currentposvec, toindex=True)
            if self._isoccupied(currentposindex):
                pieceslist.append(self._board[currentposindex])
            currentposvec += unitrelvec
        return pieceslist

    def _allowedmovesforpiece(self, piece):
        """Finds the allowed moves for 'piece' at its current position.

        This method filters out some of the moves generated by a piece's
        possiblemoves method by checking the board conditions. It uses the
        method _piecesbetween to find where is legal to move.

        Note that this method doesn't consider if there are any pins, checks
        etc. but simply what it is legally allowed to do on the board."""
        # TODO: Can this method be improved?
        startpos = piece.position(indexform=True)
        movelist = piece.possiblemoves(); allowedmoves = list()

        # HACK: Add an extra move to the pawn piece if on 2nd or 7th rank.
        if piece.piecetype() is PawnPiece:
            startposvec = piece.position(vectorform=True)
            if startposvec.tupleform()[0] == 1 and piece.isplayerpiece:
                movelist.append(startposvec + Vector(2, 0))
            elif startposvec.tupleform()[0] == 6 and not piece.isplayerpiece:
                movelist.append(startposvec + Vector(-2, 0))

        # Iterate through all moves and filter out bad ones.
        for move in movelist:
            moveindex = self.convert(move, toindex=True)
            if piece.piecetype() is KnightPiece:
                pass
            elif self._piecesbetween(startpos, moveindex):
                continue

            if self._board[moveindex] != None:
                if self._piecesareonsameside(piece, self._board[moveindex]):
                    continue  # Can't capture your own side.
            allowedmoves.append(move)
        return allowedmoves

    def _fetchbasicmovesfor(self, side=True):
        """Gets all the basic moves for 'side'"""
        possiblemoves = dict()
        # First find all legal moves.
        for square in self._board:
            if square is None:  # Continue loop if square is empty.
                continue
            elif square.isplayerpiece is not side:  # Skip pieces on other side.
                continue
            movelist = self._allowedmovesforpiece(square)  # Basic allowed moves.
            possiblemoves[square] = movelist  # Add them to possible moves.
        return possiblemoves


class _ChessBoardPieces(_ChessBoardPiecesCore):
    """The component that handles the pieces on the board."""

    def findpiece(self, piecetype, playerside=True):
        """Finds all instances of piece on the board that belong to one side.

        Returns a list of the board indices."""
        piecepositions = list()
        for ii, square in enumerate(self._board):
            if square is None:
                continue
            elif ((piecetype is square.piecetype())
                    and xnor(square.isplayerpiece, playerside)):
                piecepositions.append(ii)
        return piecepositions

    def kingincheck(self, playerking=True):
        """Returns a bool for whether the king is in check or not."""
        return len(self._piecesattackingking(playerking=playerking)) > 0

    def allpossiblemoves(self, forplayerpieces=True):
        """Gets all of the possible moves available for each piece for either
        the player or the opposition."""
        # First fetch basic moves and captures.
        allpossiblemoves = self._fetchbasicmovesfor(side=forplayerpieces)

        # Now remove moves that put/leave the king in check.
        for piece, movelist in allpossiblemoves.iteritems():
            piecestartposition = piece.position(indexform=True); ii = 0

            while ii < len(movelist):
                move = movelist[ii]
                pieceendposition = self.convert(move, toindex=True)
                if self._board[pieceendposition] != None:
                    fixboardoncedone = True  # HACK
                    endpiece = self._board[pieceendposition]
                else:
                    fixboardoncedone = False
                self.move(piecestartposition, pieceendposition, force=True)
                attackingpiecelist = self._piecesattackingking(
                    playerking=forplayerpieces)

                # If the move leaves the king in check, remove it from allowed moves.
                if len(self._piecesattackingking(playerking=forplayerpieces)) > 0:
                    movelist.remove(move)
                else:
                    ii += 1
                self.move(pieceendposition, piecestartposition)
                if fixboardoncedone:
                    self.addpiece(
                        endpiece.piecetype(), endpiece.position(indexform=True),
                        endpiece.isplayerpiece)
        return allpossiblemoves

    def addpiece(self, piece, position, playerpiece=True, force=False):
        """Add a new piece to the board."""
        # Converting into index and sanity checks.
        index = self.convert(position, toindex=True)
        if not force: self._assertIsUnoccupied(index)  # Allow forced overwriting.
        self._assertPositionOnBoard(index)

        # Now add the piece.
        self._board[index] = piece(playerpiece, startpositionindex=index)
        return None

    def emptysquare(self, position):
        """Removes a piece from the board."""
        index = self.convert(position, toindex=True)
        self._assertPositionOnBoard(index)
        self._board[index] = None

    def move(self, startindexcoordinate, endindexcoordinate, force=False):
        """Move a piece around on the board."""
        # Sanity checks and conversion to indices.
        assert startindexcoordinate != endindexcoordinate, \
            "To move the piece, the start and end points must be different."
        startindex = self.convert(startindexcoordinate, toindex=True)
        endindex = self.convert(endindexcoordinate, toindex=True)
        self._assertPositionOnBoard(startindex)
        self._assertPositionOnBoard(endindex)
        self._assertIsOccupied(startindex)
        if not force: self._assertIsUnoccupied(endindex)  # Allow forced overwriting.

        # Move the piece to the new position.
        self._board[startindex].movetoindex(endindex)
        self._board[endindex] = self._board[startindex]
        self._board[startindex] = None
        return None

    def capture(self, startindexcoordinate, endindexcoordinate):
        """Captures a piece on the board. Shorter call then emptysquare & move."""
        startindex = self.convert(startindexcoordinate, toindex=True)
        endindex = self.convert(endindexcoordinate, toindex=True)
        self._assertPositionOnBoard(startindex)
        self._assertPositionOnBoard(endindex)
        self._assertIsOccupied(startindex)
        self._assertIsOccupied(endindex)

        self.emptysquare(endindex)
        self.move(startindex, endindex)
        return None


 #     #  #####  ####### ######
 #     # #     # #       #     #
 #     # #       #       #     #
 #     #  #####  #####   ######
 #     #       # #       #   #
 #     # #     # #       #    #
  #####   #####  ####### #     #

 ### #     # ####### ####### ######  #######    #     #####  #######
  #  ##    #    #    #       #     # #         # #   #     # #
  #  # #   #    #    #       #     # #        #   #  #       #
  #  #  #  #    #    #####   ######  #####   #     # #       #####
  #  #   # #    #    #       #   #   #       ####### #       #
  #  #    ##    #    #       #    #  #       #     # #     # #
 ### #     #    #    ####### #     # #       #     #  #####  #######



class _ChessBoardUI(_ChessBoardCore):
    """Controls interacting with the user as well as algebraic notation."""

    def _determinepiece(self, symbol):
        """Using the symbols for the pieces, return class for passed symbol."""
        piecesymbols = tuple('RNBQK')
        pieces = (RookPiece, KnightPiece, BishopPiece, QueenPiece, KingPiece)
        try:
            return pieces[piecesymbols.index(symbol)]
        except ValueError:
            raise ValueError("The symbol passed isn't a valid option.")


    def _positiontonotation(self, startpos, endpos, capture=False):
        """Converts a position into *my* notation."""

        def getpositionstring(pos):
            """Gets the position as a algebraic string."""
            vec = self.convert(pos, tovector=True)
            (rank_, file_) = vec.tupleform()
            return self._filesymbols[file_] + self._ranksymbols[rank_]

        startnotation = getpositionstring(startpos)
        endnotation = getpositionstring(endpos)
        if capture: concat = 'x'
        else: concat = '->'
        return startnotation + concat + endnotation

    def _notationtopositions(self, notationstring):
        """Converts *my* algebraic notation to a chess position.

        This method takes the movement part of the string the user passes and
        converts it into a vector. Note that this only takes the movement part.
        You can not include the piece symbol at the start."""
        try:
            assert 'x' in notationstring or '->' in notationstring
            (startpos, endpos) = (notationstring[:2], notationstring[-2:])

            filefunc = lambda x: self._filesymbols.index(x[0])
            rankfunc = lambda x: self._ranksymbols.index(x[1])

            startvec = Vector(rankfunc(startpos), filefunc(startpos))
            endvec = Vector(rankfunc(endpos), filefunc(endpos))
        except AssertionError:
            raise Exception(
                "The notation string doesn't follow correct syntax rules.")
        except RuntimeError as e:
            raise RuntimeError("This shouldn't be raised! Something went wrong.")
        else:
            return startvec, endvec

    def fetchmovehistory(self):
        """Fetches the list with the move history."""
        return self._movehistory

    def addmovetohistory(self, piece, startposition, endposition,
                         movewascapture=False):
        """Writes a move into the game history using *my* notation."""
        try:
            piecesymbol = piece.symbol()
            movesymbol = self._positiontonotation(
                startposition, endposition, capture=movewascapture)

            notationstring = piecesymbol + movesymbol
            self._movehistory.append(notationstring)
        except AttributeError as err1:
            raise
        except TypeError as err2:
            raise

    def processplayermove(self, userstring):
        """Figure out what the hell the user is trying to say.

        Currently this method only has the ability to read in my algebraic
        notation to specify where a piece goes. Eventually this method will
        become redundant when the GUI is developed.

        The method returns the piece that is to move, along with the position
        the piece will move to."""
        # TODO: Add checks/more stringent tests for user input.
        # REVIEW: What do I need this function to return?
        if userstring[0] in 'RNBQK':  # Moving a backline piece.
            piecetomove = self._determinepiece(userstring[0])
            startvec, endvec = self._notationtopositions(userstring[1:])
        elif userstring[0] in self._filesymbols:  # If just moving a pawn.
            piecetomove = PawnPiece
            startvec, endvec = self._notationtopositions(userstring)
        else:
            raise SyntaxError("Notation has invalid syntax.")
        return piecetomove, (startvec, endvec)


  #####  ######     #    ######  #     # ###  #####     #    #
 #     # #     #   # #   #     # #     #  #  #     #   # #   #
 #       #     #  #   #  #     # #     #  #  #        #   #  #
 #  #### ######  #     # ######  #######  #  #       #     # #
 #     # #   #   ####### #       #     #  #  #       ####### #
 #     # #    #  #     # #       #     #  #  #     # #     # #
  #####  #     # #     # #       #     # ###  #####  #     # #######

 #     #  #####  ####### ######
 #     # #     # #       #     #
 #     # #       #       #     #
 #     #  #####  #####   ######
 #     #       # #       #   #
 #     # #     # #       #    #
  #####   #####  ####### #     #

 ### #     # ####### ####### ######  #######    #     #####  #######
  #  ##    #    #    #       #     # #         # #   #     # #
  #  # #   #    #    #       #     # #        #   #  #       #
  #  #  #  #    #    #####   ######  #####   #     # #       #####
  #  #   # #    #    #       #   #   #       ####### #       #
  #  #    ##    #    #       #    #  #       #     # #     # #
 ### #     #    #    ####### #     # #       #     #  #####  #######



class _ChessBoardGUI(_ChessBoardCore):
    """The component that handles drawing up the board on the screen."""

    def _uppercaseif(self, condition, string):
        """Either force a string into uppercase or lower case."""
        if condition:
            return string.upper()
        else:
            return string.lower()

    def _asciiemptysquare(self, indexorcoordinateorvector):
        """Returns the string for the board at the supplied index."""
        vector = self.convert(indexorcoordinateorvector, tocoordinate=True)
        darksquare = ':::'
        lightsquare = '   '

        if coordinate[0] % 2 == 0:  # If even rank.
            if coordinate[1] % 2 == 0:  # If even file.
                return darksquare
            else:  # If odd.
                return lightsquare
        else:  # If odd rank.
            if coordinate[1] % 2 == 0:  # If even file.
                return lightsquare
            else:  # If odd.
                return darksquare

    def _asciioccupiedsquare(self, index):
        """Returns the string to be used if occupied."""
        piece = self._board[index]
        piecesym = self._uppercaseif(
            piece.isplayerpiece, piece.symbol(forasciiboard=True))
        return piecesym

    def _topborder(self):
        """Returns the top border string."""
        return '+----------+'

    def _bottomborder(self):
        """Returns the bottom border string. WIP for when it is interesting."""
        return '+----------+'

    def displayboard(self):
        """Prints the board using ASCII graphics"""
        # Get the board state in ASCII art.
        asciisquares = [None] * 64
        for index, square in enumerate(self._board):
            if square is None:
                # WIP: Future code below.
                # asciisquares[index] = self._asciiemptysquare(index)
                asciisquares[index] = '.'
            else:
                asciisquares[index] = self._asciioccupiedsquare(index)

        # Now print it.
        # FIXME: Find a better way of doing this.
        join = lambda l: reduce(lambda x, y: x+y, l)
        print " " + self._topborder()
        print ' | ' + join(asciisquares[56:63+1]) + ' |'
        print ' | ' + join(asciisquares[48:55+1]) + ' |'
        print ' | ' + join(asciisquares[40:47+1]) + ' |'
        print ' | ' + join(asciisquares[32:39+1]) + ' |'
        print ' | ' + join(asciisquares[24:31+1]) + ' |'
        print ' | ' + join(asciisquares[16:23+1]) + ' |'
        print ' | ' + join(asciisquares[8:15+1]) + ' |'
        print ' | ' + join(asciisquares[0:7+1]) + ' |'
        print " " + self._bottomborder()
        return


 ####### #     #  #####  ### #     # #######
 #       ##    # #     #  #  ##    # #
 #       # #   # #        #  # #   # #
 #####   #  #  # #  ####  #  #  #  # #####
 #       #   # # #     #  #  #   # # #
 #       #    ## #     #  #  #    ## #
 ####### #     #  #####  ### #     # #######


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

    Eventually the public methods from the parents will be replaced with private
    ones as this class begins to handle everything public.

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
                piece.position(indexform=True),
                playerpiece=piece.isplayerpiece()
            )
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.:.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
