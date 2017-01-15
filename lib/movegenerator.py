# DESCRIPTION: The part of the chess engine that generates the legal moves.

# 50726f6772616d6d696e6720697320627265616b696e67206f66206f6e652062696720696d706f
# 737369626c65207461736b20696e746f207365766572616c207665727920736d616c6c20706f73
# 7369626c65207461736b732e

# NOTE:
# ================
# This file is currently a work in progress. The original chessboard.py file has
# become overly bloated and is detrimental to the moral of the project. This new
# script is aimed at taking only the methods that pertain to the move gen, while
# separating the other components into their own scrips

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MAIN~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from lib import core, chessboard, vectors, pieces
from lib import chessboardrefactor

  #####  ####### ######  #######
 #     # #     # #     # #
 #       #     # #     # #
 #       #     # ######  #####
 #       #     # #   #   #
 #     # #     # #    #  #
  #####  ####### #     # #######


class _CoreMoveGenerator:
    """Contains the core methods that are used in the move generation."""

    def __init__(self, currentboardstate):
        self.board = currentboardstate
        return

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

    def _piecesbetween(self, start, end):
        """Find the pieces between the start and end positions, not inclusive."""
        startvec = core.convert(start, tovector=True)
        endvec = core.convert(end, tovector=True)
        unitrelvec = (endvec - startvec).unitvector()
        currentposvec = startvec + unitrelvec

        pieceslist = list()
        while currentposvec != endvec:
            if self.board[currentposvec] != None:
                pieceslist.append(self.board[currentposvec])
            currentposvec += unitrelvec
        return pieceslist



 #     # ####### #     # #######
 ##   ## #     # #     # #
 # # # # #     # #     # #
 #  #  # #     # #     # #####
 #     # #     #  #   #  #
 #     # #     #   # #   #
 #     # #######    #    #######

  #####  ####### #     # ####### ######     #    ####### ### ####### #     #
 #     # #       ##    # #       #     #   # #      #     #  #     # ##    #
 #       #       # #   # #       #     #  #   #     #     #  #     # # #   #
 #  #### #####   #  #  # #####   ######  #     #    #     #  #     # #  #  #
 #     # #       #   # # #       #   #   #######    #     #  #     # #   # #
 #     # #       #    ## #       #    #  #     #    #     #  #     # #    ##
  #####  ####### #     # ####### #     # #     #    #    ### ####### #     #


class MoveGenerator:
    """Generates the possible moves based off the rules of chess."""

    def _basicmoves(self, colour):
        """Get the most basic moves, such as simple captures and movement."""
        # Define the method that finds the alllowed moves for each piece.
        def movesforpiece(piece, pos):
            """Get the moves for the piece at position 'pos'."""
            allowedmoves = list()
            for unitvector in piece.moveunitvectors:
                movetopos = core.convert(pos, tovector=True) + unitvector

                while self.board.positiononboard(movetopos):
                    endsquare = self.board[movetopos]
                    if endsquare != None:
                        if self._piecesareonsameside(piece, endsquare):
                            break
                        else:  # If opposition piece.
                            allowedmoves.append(movetopos)
                            break  # Can't go further then capture.
                    else:
                        allowedmoves.append(movetopos)

                    if piece.crawler: break
                    else: movetopos += unitvector

                continue
            return

        # Now apply that method to each piece on the board.
        movelist = list()
        for index, square in enumerate(self.board):
            if square == None:
                continue
            elif square.colour == colour:
                continue  # Skip over piece if it is different colour.
            startpos = index
            endposlist = core.convertlist(
                movesforpiece(square, startpos), toindex=True
            )
            movepairs = map(lambda x: (startpos, x), endposlist)
        return movepairs

    def _illegalmove(self, startpos, endpos, kingcolour):
        """Checks to see if the supplied move if illegal."""
        if kingcolour == 'white': oppositioncolour = 'black'
        else: oppositioncolour = 'white'

        simboard = self.board.duplicateboard()
        simboard.move(startpos, endpos, force=True)
        basicoppositionmoves = self._basicmoves(oppositioncolour)
        oppositionendmoves = map(lambda x: x[1], basicoppositionmoves)

        kingpos = self.board.findpiece(pieces.KingPiece, kingcolour)[0]
        if kingpos in oppositionendmoves:
            return True
        else:
            return False

    def _onlylegalmoves(self, colour, movepairlist):
        """Filter a list, keeping only legal moves."""
        ii = 0
        while ii < len(movepairlist):
            start, end = movepairlist[ii]
            if self._illegalmove(start, end, colour):
                del movepairlist[ii]
            else:
                ii += 1
        return movepairlist

    def _castlemoves(self, colour):
        """Get the caslting moves."""
        castlemoves = list(); castleleft = True; castleright = True
        # See if allowed to castle at all.
        if not self.cancastleleft: castleleft = False
        if not self.cancastleright: castleright = False

        if not castleleft and not castleright:
            return castlemoves  # Early exit to reduce overhead on move gen.

        # See if king or rook out of place.
        if self.board[king] != pieces.KingPiece:
            self.board.cancastleleft = False; self.board.cancastleright = False
            castleleft = False; castleright = False
        else:
            if self.board[rookleft] != pieces.RookPiece:
                castleleft = False; self.board.cancastleleft = False
            if self.board[rookright] != pieces.RookPiece:
                castleright = False; self.board.cancastleright = False

        # See if there are pieces between the rook and king.
        if self._piecesbetween(rookleft, king):
            castleleft = False
        if self._piecesbetween(rookright, king):
            castleright = False

        # See if the castle start/end/during puts the king in check.
        castleleftsteps = range(king, king - 3, -1)
        castlerightsteps = range(king, king + 3)
        for step in castleleftsteps:
            if self._illegalmove(king, step, colour):
                castleleft = False
            else:
                continue
        for step in castlerightsteps:
            if self._illegalmove(king, step, colour):
                castleright = False
            else:
                continue

        # Then see what if castle moves can be added.
        if castleleft:
            castlemoves.append(
                (rookleft, rookleft+3), (king, king-2)
            )
        if castleright:
            castlemoves.append(
                (rookleft, rookleft-2), (king, king+2)
            )
        return castlemoves


    def _enpassantmoves(self, colour):
        """Get the en passant moves."""
        def addtomovesifcanenpassant(pos, thelist):
            """Determines if the piece at pos can en passant."""
            if colour == 'white': capturerank = 5
            else: capturerank = 2

            square = self.board[pos]
            if square == pieces.PawnPiece:
                if square.colour == colour:
                    startindex = core.convert(pos, toindex=True)
                    endindex = core.convert((capturerank, file_), toindex=True)
                    thelist.append((startindex, endindex))
            return thelist

        # Determine if there are any en passant moves present.
        if self.board.enpassant == None: return list()
        else: file_ = self.board.enpassant

        # See if there are pawns of correct colour on either side.
        if colour == 'white': rank_ = 4
        else: rank_ = 3
        enpassantleft = (rank_, file_-1); enpassantright = (rank_, file_+1)
        movelist = list()
        if self.board.positiononboard(enpassantleft):
            movelist = addtomovesifcanenpassant(enpassantleft, movelist)
        if self.board.positiononboard(enpassantright):
            movelist = addtomovesifcanenpassant(enpassantright)
        return movelist

    def generatemovelist(self, colour):
        """Generate all of the possible moves for colour."""
        basicmoves = self._basicmoves(colour)
        castlemoves = self._castlemoves(colour)
        enpassantmoves = self._enpassantmoves(colour)
        allmoves = core.combinelists(basicmoves, castlemoves, enpassantmoves)

        allmoves = self._onlylegalmoves(colour, allmoves)
        return allmoves
