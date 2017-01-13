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

# REVIEW: Now there is a method that ends the turn of the player/computer, Lots
# of the "playerside=True" crap can go and just rely on the internal attribute.

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
        for ii in pieces:
            if side is None:
                side = ii.isplayerpiece
                continue

            if ii.isplayerpiece == side:
                continue
            else:
                return False
        return True

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

    def _piecesattackingking(self, playerking=True):
        """Find the pieces that are currently attacking the king in movelist."""
        try:
            kingposvec = self.convert(
                self.findpiece(KingPiece, playerside=playerking)[0], tovector=True)
        except IndexError:  # If there is no king on the board:
            return []  # Then he can't be attacked!
        oppositionmoves = self._fetchbasicmovesfor(playerside=(not playerking))

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

    def _fetchbasicmovesfor(self, playerside=True):
        """Gets all the basic moves for 'playerside'"""
        possiblemoves = dict()
        # First find all legal moves.
        for square in self._board:
            if square is None:  # Continue loop if square is empty.
                continue
            elif square.isplayerpiece is not playerside:  # Skip pieces on other side.
                continue
            movelist = self._allowedmovesforpiece(square)  # Basic allowed moves.
            possiblemoves[square] = movelist  # Add them to possible moves.
        return possiblemoves

    def _move(self, startindex, endindex):
        """Move a piece from startined to endindex."""
        if startindex == endindex:
            return None

        # Assertion check & enpassant enforcement.
        self._assertIsOccupied(startindex)
        if self._board[startindex].piecetype() is PawnPiece:
            relvec = (self.convert(endindex, tovector=True)
                    - self.convert(startindex, tovector=True))
            if abs(relvec) == 2:
                x = self.convert(startindex, tocoordinate=True)[1]
                if self._board[startindex].isplayerpiece:
                    self._enpassant_onplayer = x
                else:
                    self._enpassant_oncomputer = x

        # Actual movement code.
        self._board[startindex].movetoindex(endindex)
        self._board[endindex] = self._board[startindex]
        self._board[startindex] = None
        return None

    def _thismoveislegal(self, startpos, endpos, playerside=True):
        """Checks to see if the supplied move is legal. Returns bool."""
        # Simulate board and make move.
        simboard = self.simulateboard()
        simboard._move(startpos, endpos)

        # See if the king is under attack.
        attackingpiecelist = simboard._piecesattackingking(
            playerking=playerside)

        if len(attackingpiecelist) > 0:
            return False
        else:
            return True


  #####     #     #####  ####### #       ### #     #  #####
 #     #   # #   #     #    #    #        #  ##    # #     #
 #        #   #  #          #    #        #  # #   # #
 #       #     #  #####     #    #        #  #  #  # #  ####
 #       #######       #    #    #        #  #   # # #     #
 #     # #     # #     #    #    #        #  #    ## #     #
  #####  #     #  #####     #    ####### ### #     #  #####


class _ChessBoardCastling(_ChessBoardCore, _PiecesCore):
    """The component that handles the castling during the chess game."""

    def _allowedtocastle(self, left=False, right=False, playerside=True):
        """A special call that determines what castling is allowed."""
        # TODO: Fix this method by breaking it into smaller methods.
        assert any([left, right]) and not all([left, right])
        # Determine the correct positions for the pieces.
        if playerside:
            king = 4
            if left: rook = 0
            elif right: rook = 7
        else:
            king = 60
            if left: rook = 56
            elif right: rook = 63
        # Determine if the king "walks" right or left & see if legal to castle.
        if left:
            if not self._castleleft:
                return False
            else:
                walk = -3
        elif right:
            if not self._castleright:
                return False
            else:
                walk = 3

        # Check that the rook and king are there.
        if (self._board[rook] == None or self._board[king] == None):
            if left:
                self._castleleft = False
            elif right:
                self._castleright = False
            return False
        elif not (self._board[rook].piecetype() is RookPiece
                and self._board[king].piecetype() is KingPiece):
            if left:
                self._castleleft = False
            elif right:
                self._castleright = False
            return False
        # Check that the spaces between are open.
        elif self._piecesbetween(rook, king):
            return False
        # Check if the king moves through check.
        else:
            moveswerelegal = [
                self._thismoveislegal(king, index, playerside)
                for index in sorted(range(king, king + walk, walk/abs(walk)))]
            if not all(moveswerelegal):
                return False
            else:
                return True
        return -1


 ####### #     #    ######     #     #####   #####     #    #     # #######
 #       ##    #    #     #   # #   #     # #     #   # #   ##    #    #
 #       # #   #    #     #  #   #  #       #        #   #  # #   #    #
 #####   #  #  #    ######  #     #  #####   #####  #     # #  #  #    #
 #       #   # #    #       #######       #       # ####### #   # #    #
 #       #    ##    #       #     # #     # #     # #     # #    ##    #
 ####### #     #    #       #     #  #####   #####  #     # #     #    #


class _ChessBoardEnPassant(_ChessBoardCore, _PiecesCore):
    """This component handles the en passant rule."""

    def _enpassant(self, targetindex, left=False, right=False):
        assert any([left, right]), "Pass either left, right or both."

        attackedpiece = self._board[targetindex]

        # Get attackers.
        attackerlist = list(); capturelist = list()
        if left:
            attacker = self._board[targetindex - 1]
            if attacker == None:
                pass
            elif (attacker.piecetype() is PawnPiece
                  and xor(attacker.isplayerpiece, attackedpiece.isplayerpiece)):
                attackerlist.append(attacker)
                capturelist.append(attacker._captureright)
        if right:
            attacker = self._board[targetindex + 1]
            if attacker == None:
                pass
            elif (attacker.piecetype() is PawnPiece
                  and xor(attacker.isplayerpiece, attackedpiece.isplayerpiece)):
                attackerlist.append(attacker)
                capturelist.append(attacker._captureleft)
        return attackerlist, capturelist

    def _getenpassantattackers(self, playerside=True):
        """Returns pieces and vectors that are also allowed moves."""
        # Determine which side you want enpassant for.
        if playerside:
            enpassant = self._enpassant_oncomputer
            targetindex = self.convert((4, self._enpassant_oncomputer), toindex=True)
        else:
            enpassant = self._enpassant_onplayer
            targetindex = self.convert((3, self._enpassant_onplayer), toindex=True)

        # Now find the current attackers depending on location.
        capturelist = list()
        if enpassant == 0:
            attackerlist, capturelist = \
                self._enpassant(targetindex, left=False, right=True)
        elif enpassant == 7:
            attackerlist, capturelist = \
                self._enpassant(targetindex, left=True, right=False)
        else:
            attackerlist, capturelist = \
                self._enpassant(targetindex, left=True, right=True)
        attackvectors = map(
            lambda x, y: x.position(vectorform=True) + y,
            attackerlist,
            capturelist
        )
        return attackerlist, attackvectors


 ######  ### #######  #####  #######  #####
 #     #  #  #       #     # #       #     #
 #     #  #  #       #       #       #
 ######   #  #####   #       #####    #####
 #        #  #       #       #             #
 #        #  #       #     # #       #     #
 #       ### #######  #####  #######  #####

 #     #    #    #     # ######  #       ### #     #  #####
 #     #   # #   ##    # #     # #        #  ##    # #     #
 #     #  #   #  # #   # #     # #        #  # #   # #
 ####### #     # #  #  # #     # #        #  #  #  # #  ####
 #     # ####### #   # # #     # #        #  #   # # #     #
 #     # #     # #    ## #     # #        #  #    ## #     #
 #     # #     # #     # ######  ####### ### #     #  #####


class ChessBoard_Pieces(_ChessBoardEnPassant, _ChessBoardCastling):
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

    def allpossiblemoves(self, forplayerpieces=True):
        """Gets all of the possible moves available for each piece for either
        the player or the opposition."""
        # First fetch basic moves and captures.
        allpossiblemoves = self._fetchbasicmovesfor(playerside=forplayerpieces)

        # Add in en passant moves.
        if self._enpassant_onplayer != None and not forplayerpieces:
            pieces, vectors = self._getenpassantattackers(forplayerpieces)
        elif self._enpassant_oncomputer != None and forplayerpieces:
            pieces, vectors = self._getenpassantattackers(forplayerpieces)
        else:
            pieces, vectors = [], []
        try:
            for ii in xrange(len(pieces)):
                piece, vector = pieces[ii], vectors[ii]
                allpossiblemoves[piece].append(vector)
        except ValueError:
            pass  # This is the error thrown when pieces and vectors are empty.

        # Now remove moves that put/leave the king in check.
        for piece, movelist in allpossiblemoves.iteritems():
            piecestartposition = piece.position(indexform=True); ii = 0

            # Now iterate through each possible move:
            while ii < len(movelist):
                move = movelist[ii]
                pieceendposition = self.convert(move, toindex=True)
                if self._thismoveislegal(piecestartposition, pieceendposition):
                    ii += 1
                else:
                    movelist.remove(move)
        return allpossiblemoves

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
            self._assertPositionOnBoard(startindex)
            self._assertPositionOnBoard(endindex)
            self._assertIsOccupied(startindex)
            if not force: self._assertIsUnoccupied(endindex)
        except AssertionError:
            raise
        else:
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



class ChessBoard_UI(_ChessBoardCore):
    """Controls interacting with the user as well as algebraic notation."""
    # TODO: Update class docstring.

    def _addmovetohistory(self, piece, startposition, endposition,
                         movewascapture=False):
        """Writes a move into the game history using *my* notation rules."""
        # TODO: Update docstring.

        # ############################ #
        # Start with defining methods. #
        # ############################ #
        def positiontonotation(startpos, endpos, capture=False):
            def getpositionstring(pos):
                vec = self.convert(pos, tovector=True)
                (rank_, file_) = vec.tupleform()
                return self._filesymbols[file_] + self._ranksymbols[rank_]
            startnotation = getpositionstring(startpos)
            endnotation = getpositionstring(endpos)
            if capture: concat = 'x'
            else: concat = '->'
            return startnotation + concat + endnotation

        def addmovetohistory(move):
            history = self.movehistory
            history.append(move)
            self.__dict__['movehistory'] = move
        # ######################## #
        # Now process the request. #
        # ######################## #
        try:
            piecesymbol = piece.symbol()
            movesymbol = self.positiontonotation(
                startposition, endposition, capture=movewascapture)

            notationstring = piecesymbol + movesymbol
            self.movehistory.append(notationstring)
        except AttributeError as err1:
            raise
        except TypeError as err2:
            raise

    # REVIEW: What do I need this to return?
    def _processplayermovestring(self, userstring):
        """Figure out what the hell the user is trying to say.

        Currently this method only has the ability to read in my algebraic
        notation to specify where a piece goes. Eventually this method will
        become redundant when the GUI is developed.

        The method returns the piece that is to move, along with the position
        the piece will move to."""
        # TODO: Update docstring.

        # ############################ #
        # Start with defining methods. #
        # ############################ #
        def determinepiece(self, symbol):
            piecesymbols = tuple('RNBQK')
            pieces = (
                RookPiece,
                KnightPiece,
                BishopPiece,
                QueenPiece,
                KingPiece
            )
            try:
                return pieces[piecesymbols.index(symbol)]
            except ValueError:
                raise ValueError("The symbol passed isn't a valid option.")

        def notationtopositions(self, notationstring):
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

        # ######################## #
        # Now process the request. #
        # ######################## #
        # TODO: Add checks/more stringent tests for user input.
        if userstring[0] in 'RNBQK':  # Moving a backline piece.
            piecetomove = self.determinepiece(userstring[0])
            startvec, endvec = self.notationtopositions(userstring[1:])
        elif userstring[0] in self._filesymbols:  # If just moving a pawn.
            piecetomove = PawnPiece
            startvec, endvec = self.notationtopositions(userstring)
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



class ChessBoard_GUI(_ChessBoardCore):
    """The component that handles drawing up the board on the screen."""
    # TODO: Update the class docstring

    def displayASCIIboard(self):
        """Prints the board using ASCII graphics"""
        # TODO: Flesh out docstring.

        # ############################ #
        # Start with defining methods. #
        # ############################ #
        def _asciisymbolofoccupiedsquare(index):
            """Returns the string to be used if occupied."""
            piece = self._board[index]
            if piece.isplayerpiece:
                return piece.symbol(forasciiboard=True).upper()
            else:
                return piece.symbol(forasciiboard=True).lower()

        def _asciisymbolforemptysquare(index):
            """Returns the string for the board at the supplied index."""
            if True:  # NOTE: This is an early exit since below is a WIP.
                return '.'

            # [[  WIP CODE  ]]
            coordinate = self.convert(index, tocoordinate=True)
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

        def join(x):
            """Joins a list of strings together."""
            return reduce(lambda x, y: x+y, x)

        # ######################## #
        # Now process the request. #
        # ######################## #
        spacing = " "; edgeborder = ' | '
        topborder = '+----------+'
        bottomborder = topborder

        # Get the board state in ASCII art.
        asciisquares = [None] * 64
        for index, square in enumerate(self._board):
            if square is None:
                asciisquares[index] = self._asciisymbolforemptysquare(index)
            else:
                asciisquares[index] = self._asciisymbolofoccupiedsquare(index)
        rankrows = [
            join(asciisquares[0:8]),    # First rank
            join(asciisquares[8:16]),   # Second rank
            join(asciisquares[16:24]),  # ...
            join(asciisquares[24:32]),  # ...
            join(asciisquares[32:40]),  # ...
            join(asciisquares[40:48]),  # ...
            join(asciisquares[48:56]),  # Seventh rank
            join(asciisquares[56:64])   # Eigth rank
        ]
        if self.playercolour is 'white':
            rankrows = rankrows[::-1]  # Print the first rank last.
        else:
            rankrows = rankrows  # Print eighth rank last.

        # Now print it.
        print spacing + topborder
        for row in rankrows:
            print edgeborder + row + edgeborder
        print spacing + bottomborder
        return


 ####### #     #  #####  ### #     # #######
 #       ##    # #     #  #  ##    # #
 #       # #   # #        #  # #   # #
 #####   #  #  # #  ####  #  #  #  # #####
 #       #   # # #     #  #  #   # # #
 #       #    ## #     #  #  #    ## #
 ####### #     #  #####  ### #     # #######


class ChessBoard_Engine(_ChessBoardCore):
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


class ChessBoard(_ChessBoardCore, ChessBoard_Pieces, ChessBoard_Engine,
                 ChessBoard_UI, ChessBoard_GUI):
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
        self._needtoupdate = True

        self.protectedattributes = (
            'movesforwhite',
            'movesforblack',
            'movehistory'
        )

    def drawboard(self):
        """Displays the board in the terminal from either side."""
        # WIP!
        self.displayASCIIboard()
        return

    def legalmovesfor(self, colour):
        "Gets all of the legal moves for the colour supplied."
        if colour.lower() == 'white':
            if self._needtoupdate:
                self.movesforwhite = self.fetchpossiblemovesfor(white=True)
                self._needtoupdate = False
            return self.movesforwhite
        elif colour.lower() == 'black':
            if self._needtoupdate:
                self.movesforwhite = self.fetchpossiblemovesfor(black=True)
                self._needtoupdate = False
            return self.movesforblack
        return

    def makemove(self, userstring):
        """Moves a piece to the position supplied."""
        return

    def endturn(self):
        """Ends the turn and runs some cleanup code."""
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
