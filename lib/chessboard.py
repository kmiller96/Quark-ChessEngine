# DESCRIPTION: Contains all of the code, classes and functions corresponding to
# the board.

# 50726f6772616d6d696e6720697320627265616b696e67206f66206f6e652062696720696d706f
# 737369626c65207461736b20696e746f207365766572616c207665727920736d616c6c20706f73
# 7369626c65207461736b732e

# REVIEW: Now there is a method that ends the turn of the player/computer, Lots
# of the "playerside=True" crap can go and just rely on the internal attribute.

# FIXME: For the move dictionaries, now make the move-to-positions indices, not
# vectors.

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
        self.playercolour = 'white'
        self.computercolour = 'black'

        # Needed for move generation.
        self.movesforwhite = dict()
        self.movesforblack = dict()

        # Needed for castling rules.
        self._castleleft = True
        self._castleright = True

        # Needed for En Passant.
        self._enpassant_onplayer = None
        self._enpassant_oncomputer = None

        # Needed for UI:
        self.movehistory = list()
        self._ranksymbols = tuple(map(lambda x: str(x), range(1, 8+1)))
        self._filesymbols = tuple('abcdefgh')

    # REVIEW: Do I need this method?
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

    # REVIEW: Where is this being used, and why?
    @staticmethod
    def _piecesareonsameside(*pieces):
        """Checks to see if the passed pieces are all on the same side."""
        side = None
        for piece in pieces:
            if side is None:
                side = piece.colour  # Use the first piece's colour as comparison.
                continue

            if piece.colour == side:  # Same side is ok.
                continue
            else:  # Different sides are not.
                return False
        return True

    def isplayercolour(self, colour):
        """Determines if the colour passed is the player's colour or not."""
        assert colour.lower() in ('white', 'black'), \
            "The colour of the piece must be 'white' or 'black'"
        if colour.lower() == 'white':
            return True
        else:
            return False

    def simulateboard(self):
        """Creates an instance of the chess board exactly as it is now."""
        return deepcopy(self)

    def assertPositionOnBoard(self, position):
        """Asserts that the position is valid."""
        try:
            index = convert(position, toindex=True)
            self._board[index]
        except IndexError:  # If off board.
            raise AssertionError("The position %r is off the board." % position)
        return None

    def assertIsUnoccupied(self, position):
        """Asserts that the square is free and unoccupied."""
        try:
            index = convert(position, toindex=True)
            assert self._board[index] == None, "The target square is occupied."
        except IndexError:
            raise IndexError("The index used is off the board!")
        return None

    def assertIsOccupied(self, position):
        """Asserts that the square is occupied."""
        try:
            index = convert(position, toindex=True)
            assert self._board[index] != None, "The target square is unoccupied."
        except IndexError:
            raise IndexError("The index used is off the board!")
        return None

    def squareisoccupied(self, index):
        """Returns true if the square is occupied, false if empty."""
        return self._board[index] != None


 ######  ### #######  #####  #######  #####
 #     #  #  #       #     # #       #     #
 #     #  #  #       #       #       #
 ######   #  #####   #       #####    #####
 #        #  #       #       #             #
 #        #  #       #     # #       #     #
 #       ### #######  #####  #######  #####

  #####  ####### ######  #######
 #     # #     # #     # #
 #       #     # #     # #
 #       #     # ######  #####
 #       #     # #   #   #
 #     # #     # #    #  #
  #####  ####### #     # #######


class _PiecesCore(_ChessBoardCore):
    """A class that stores the private methods of the ChessBoardPieces component."""

    def _piecesattacking(self, position, attackingcolour):
        """Find what pieces are attacking the position specified."""
        # Sanity checks.
        if attackingcolour is 'white':
            oppositionmoves = self.movesforwhite
        elif attackingcolour is 'black':
            oppositionmoves = self.movesforblack
        else:
            raise ColourError(
                "The colour %r is neither white or black" % attackingcolour)

        index = convert(position, toindex=True)
        assert self.squareisoccupied(index)

        # Now check which pieces have moves onto position.
        attackerlist = list()
        for piece, movelist in oppositionmoves.iteritems():
            if index in movelist:
                attackerlist.append(piece)
            else:
                continue
        return attackerlist

    def _piecesbetween(self, start, end):
        """Find the pieces between the start and end positions, not inclusive."""
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

    def _kingincheckaftermove(self, startpos, endpos, kingcolour):
        """Checks to see if the supplied move leaves the king in check."""
        # Find the king.
        playerking = self.isplayercolour(kingcolour)
        for ii, square in enumerate(self._board):
            if square == None:
                continue
            elif square == KingPiece and xnor(square.isplayerpiece, playerking):
                kinglocation = ii
                break

        # Simulate board, make move and see if the king is under attack.
        simboard = self.simulateboard()
        simboard._move(startpos, endpos)

        if playerking: attackingcolour = self.computercolour
        else: attackingcolour = self.playercolour
        attackers = simboard._piecesattacking(kinglocation, attackingcolour)
        return len(attackers) > 0

    def _castle(self, colour, longside=False, shortside=False):
        """Castle the king long."""
        assert any((longside, shortside)) and not all((longside, shortside)), \
            "Please specify whether you are castling long or short."
        playercastle = self.isplayercolour(colour)
        if playercastle:
            if longside:
                self._move(4, 2)
                self._move(0, 3)
            elif shortside:
                self._move(4, 6)
                self._move(7, 5)
        elif not playercastle:
            if longside:
                self._move(60, 58)
                self._move(56, 59)
            elif shortside:
                self._move(60, 62)
                self._move(63, 61)
        return None

    def _move(self, startindex, endindex):
        """Move a piece from startined to endindex."""
        if startindex == endindex:
            return None
        self.assertIsOccupied(startindex)  # Just so the method call doesn't fail.
        self._board[startindex].movetoindex(endindex)
        self._board[endindex] = self._board[startindex]
        self._board[startindex] = None
        return None


 ######  ### #######  #####  #######  #####       ##
 #     #  #  #       #     # #       #     #     #  #
 #     #  #  #       #       #       #            ##
 ######   #  #####   #       #####    #####      ###
 #        #  #       #       #             #    #   # #
 #        #  #       #     # #       #     #    #    #
 #       ### #######  #####  #######  #####      ###  #

 #     # ####### #     # ####### #     # ####### #     # #######
 ##   ## #     # #     # #       ##   ## #       ##    #    #
 # # # # #     # #     # #       # # # # #       # #   #    #
 #  #  # #     # #     # #####   #  #  # #####   #  #  #    #
 #     # #     #  #   #  #       #     # #       #   # #    #
 #     # #     #   # #   #       #     # #       #    ##    #
 #     # #######    #    ####### #     # ####### #     #    #


class ChessBoard_Pieces(_ChessBoardEnPassant, _ChessBoardCastling):
    """The component that handles the pieces and their motion on the board."""

    def findpiece(self, piecetype, colour):
        """Finds all instances of piece on the board that belong to one side.

        Returns a list of the board indices."""
        piecepositions = list()
        for ii, square in enumerate(self._board):
            if square is None:
                continue
            elif ((piecetype is square.piecetype())
                    and square.colour == colour):
                piecepositions.append(ii)
        return piecepositions

    def kingincheck(self, playerking=True):
        """Returns a bool for whether the king is in check or not."""
        return len(self._piecesattackingking(playerking=playerking)) > 0

    def checkmate(self, playerking=True):
        """Determine if the player's king is in checkmate."""
        underattack = len(self._piecesattackingking(playerking=playerking)) > 0
        kinginstance = self._board[
            self.findpiece(KingPiece, playerside=playerking)[0]]
        kingmoves = self.allpossiblemoves()[kinginstance]
        cantescapeattack = len(kingmoves) == 0
        return underattack and cantescapeattack

    def stalemate(self, playerking=True):
        """Determine if the player's king is in a stalemate."""
        underattack = len(self._piecesattackingking(playerking=playerking)) > 0
        kinginstance = self._board[
            self.findpiece(KingPiece, playerside=playerking)[0]]
        kingmoves = self.allpossiblemoves()[kinginstance]
        cantmove = len(kingmoves) == 0
        return (not underattack) and cantmove

    def addpiece(self, piece, position, playerpiece=True, force=False):
        """Add a new piece to the board."""
        try:
            index = self.convert(position, toindex=True)
            if not force: self._assertIsUnoccupied(index)  # Allow forced overwriting.
            self._assertPositionOnBoard(index)
        except AssertionError:
            raise
        else:
            self._board[index] = piece(playerpiece, startpositionindex=index)
        return None

    def emptysquare(self, position):
        """Removes a piece from the board."""
        try:
            index = self.convert(position, toindex=True)
            self._assertPositionOnBoard(index)
        except AssertionError:
            raise
        else:
            self._board[index] = None

    def move(self, startindexcoordinate, endindexcoordinate, force=False):
        """Move a piece around on the board."""
        # Sanity checks and conversion to indices.
        try:
            assert startindexcoordinate != endindexcoordinate, \
                "To move the piece, the start and end points must be different."
            startindex = self.convert(startindexcoordinate, toindex=True)
            endindex = self.convert(endindexcoordinate, toindex=True)

            self.assertPositionOnBoard(startindex)
            self.assertPositionOnBoard(endindex)
            self.assertIsOccupied(startindex)
            if not force: self._assertIsUnoccupied(endindex)

        except AssertionError:
            raise
        else:
            # Enpassant enforcement.
            if self._board[startindex] == PawnPiece:
                relvec = (self.convert(endindex, tovector=True)
                        - self.convert(startindex, tovector=True))
                if abs(relvec) == 2:
                    x = self.convert(startindex, tocoordinate=True)[1]
                    if self._board[startindex].isplayerpiece:
                        self._enpassant_onplayer = x
                    else:
                        self._enpassant_oncomputer = x

            # TODO: Move this to the public call of move()
            # Castling enforcement
            elif self._board[startindex] == KingPiece:
                relvec = (self.convert(endindex, tovector=True)
                        - self.convert(startindex, tovector=True))
                if abs(relvec) == 2:
                    if relvec.vector[1] < 0:
                        self._castle(longside=True)
                    elif relvec.vector[1] > 0:
                        self._castle(shortside=True)
                    return None

            self._move(startindex, endindex)
        return None

    def capture(self, startindexcoordinate, endindexcoordinate):
        """Captures a piece on the board. Shorter call then emptysquare & move."""
        try:
            startindex = self.convert(startindexcoordinate, toindex=True)
            endindex = self.convert(endindexcoordinate, toindex=True)
            self._assertPositionOnBoard(startindex)
            self._assertPositionOnBoard(endindex)
            self._assertIsOccupied(startindex)
            self._assertIsOccupied(endindex)
        except AssertionError:
            raise
        else:
            self._move(startindex, endindex)
        return None    


  #####  #     # #######  #####   #####  ######  #######    #    ######  ######
 #     # #     # #       #     # #     # #     # #     #   # #   #     # #     #
 #       #     # #       #       #       #     # #     #  #   #  #     # #     #
 #       ####### #####    #####   #####  ######  #     # #     # ######  #     #
 #       #     # #             #       # #     # #     # ####### #   #   #     #
 #     # #     # #       #     # #     # #     # #     # #     # #    #  #     #
  #####  #     # #######  #####   #####  ######  ####### #     # #     # ######


class ChessBoard(_ChessBoardCore, _PiecesCore, ChessBoard_Pieces,
                 ChessBoard_MoveGeneration, ChessBoard_UI, ChessBoard_GUI,
                 ChessBoard_Engine):
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

    # WHAT DO YOU WANT TO BE ABLE TO CALL?
    # ======================================
    # - Fetch the allowed moves for the current board state
    # - Get a user input and process it
    # - Draw the board if requested.
    # - Figure out whos turn it is.

    def __init__(self):
        """Initalise the chessboard."""
        # Call the __init__ of all the parents.
        _ChessBoardCore.__init__(self)

        # Define your own attributes.
        self.movesforwhite = dict()
        self.movesforblack = dict()

        self.protectedattributes = (
            'movesforwhite',
            'movesforblack',
            'movehistory'
        )
        return None

    def fetchpossiblemovesfor(self, white=False, black=False):
        """Generate the move dictionary for either white or black."""
        # First fetch basic moves and captures.
        assert any((white, black)) and not all((white, black)), \
            "Pick one colour only (white or black)."
        if white:
            colour = 'white'
        elif black:
            colour = 'black'
        possiblemoves = self._basicmovementfor(colour)

        # Add in en passant moves.
        if self._enpassant_onplayer != None and not forplayerpieces:
            pieces, vectors = self._enpassantattackers(forplayerpieces)
        elif self._enpassant_oncomputer != None and forplayerpieces:
            pieces, vectors = self._enpassantattackers(forplayerpieces)
        else:
            pieces, vectors = [], []
        try:
            for ii in xrange(len(pieces)):
                piece, vector = pieces[ii], vectors[ii]
                possiblemoves[piece].append(vector)
        except ValueError:
            pass  # This is the error thrown when pieces and vectors are empty.

        # Add in castling moves.
        kingpiece = self._board[self.findpiece(KingPiece, colour)[0]]
        if self._allowedtocastle(colour, left=True):
            possiblemoves[kingpiece].append(Vector(0, 2))
        if self._allowedtocastle(colour, right=True):
            possiblemoves[kingpiece].append(Vector(0, 6))

        # Remove the moves that leave/put the king in check.
        possiblemoves = self._removeillegalmoves(possiblemoves)
        return possiblemoves

    def drawboard(self):
        """Displays the board in the terminal from either side."""
        # WIP: I don't know what I want in here...
        self.displayASCIIboard()
        return

    def legalmovesfor(self, colour):
        "Gets all of the legal moves for the colour supplied."
        if colour.lower() == 'white':
            return self.movesforwhite
        elif colour.lower() == 'black':
            return self.movesforblack
        return

    def makemove(self, userstring):
        """Moves a piece to the position supplied."""
        return

    def endturn(self):
        """Ends the turn and runs some cleanup code."""
        # Update the legal move lists.
        self.movesforwhite = self.fetchpossiblemovesfor(white=True)
        self.movesforblack = self.fetchpossiblemovesfor(black=True)

        # Do some cleanup/altering of attributes
        self.playerturn = not self.playerturn
        if self.playerturn:
            self._enpassant_onplayer = None
        else:
            self._enpassant_oncomputer = None
        return None


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
