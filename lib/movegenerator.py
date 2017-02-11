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

from lib import core, chessboard, vectors, pieces, usercontrol

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
        try:
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
        except AttributeError:
            raise TypeError("You must pass pieces from the pieces script.")

    def _piecesbetween(self, start, end, inclusive=False):
        """Find the pieces between the start and end positions, not inclusive."""
        startvec = core.convert(start, tovector=True)
        endvec = core.convert(end, tovector=True)
        unitrelvec = (endvec - startvec).unitvector()
        if inclusive:
            currentposvec = startvec
            endvec += unitrelvec  # HACK: Shift up if inclusive.
        else:
            currentposvec = startvec + unitrelvec

        pieceslist = list()
        while currentposvec != endvec:
            if self.board[currentposvec] != None:
                pieceslist.append(self.board[currentposvec])
            currentposvec += unitrelvec
        return pieceslist

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
            return allowedmoves

        # Sanity checks.
        if colour not in ('white', 'black'):
            raise core.ColourError()

        # Now apply that method to each piece on the board.
        movelist = list()
        for index, square in enumerate(self.board):
            if square == None:
                continue
            elif square.colour != colour:
                continue  # Skip over piece if it is different colour.
            startpos = index
            endposlist = core.convertlist(
                movesforpiece(square, startpos), toindex=True
            )
            movepairs = map(lambda x: (startpos, x), endposlist)
            movelist.append(movepairs)
        return core.flattenlist(movelist)

    def kingincheck(self, kingcolour):
        """Determine if the king of a certain colour is in check."""
        if kingcolour == 'white':
            oppositioncolour = 'black'
        elif kingcolour == 'black':
            oppositioncolour = 'white'
        else:
            raise core.ColourError()

        basicoppositionmoves = self._basicmoves(oppositioncolour)
        oppositionendmoves = map(lambda x: x[1], basicoppositionmoves)
        kingpos = self.board.findpiece(pieces.KingPiece, kingcolour.lower())[0]
        return (kingpos in oppositionendmoves)



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


class MoveGenerator(_CoreMoveGenerator):
    """Generates the possible moves based off the rules of chess."""

    def illegalmove(self, movepair, kingcolour):
        """Checks to see if the supplied move if illegal."""
        if kingcolour.lower() == 'white': oppositioncolour = 'black'
        elif kingcolour.lower() == 'black': oppositioncolour = 'white'
        else: raise TypeError("King is either white or black.")

        # Make the move and see if the king is in check.
        originalboard = self.board.duplicateboard()
        if isinstance(movepair[0],tuple) and isinstance(movepair[1],tuple):
            for move in movepair:
                self.board.move(move[0], move[1], force=True)
        else:
            self.board.move(movepair[0], movepair[1], force=True)
        result = self.kingincheck(kingcolour)

        self.board = originalboard  # Cleanup (restore actual board state)
        return result

    def _onlylegalmoves(self, colour, movepairlist):
        """Filter a list, keeping only legal moves."""
        ii = 0
        while ii < len(movepairlist):
            movepairlist[ii]
            if self.illegalmove(movepairlist[ii], colour):
                del movepairlist[ii]
            else:
                ii += 1
        return movepairlist

    def _castlemoves(self, colour):
        """Get the caslting moves."""
        # ---------------------------------------------------------------------
        def isking(position):
            """Determine if the piece at position is a king."""
            try:
                result = (self.board[position].type() == pieces.KingPiece)
            except AttributeError:
                result = False  # If position is empty, return false.
            return result

        def isrook(position):
            """Determine if the piece at position is a rook."""
            try:
                result = (self.board[position].type() == pieces.RookPiece)
            except AttributeError:
                result = False  # If position is empty, return false.
            return result
        # ---------------------------------------------------------------------
        castlemoves = list(); castleleft = True; castleright = True

        # See if allowed to castle at all.
        if not self.board.cancastleleft: castleleft = False
        if not self.board.cancastleright: castleright = False

        if not castleleft and not castleright:
            return castlemoves  # Early exit to reduce overhead.

        # Determine where the king and rook are.
        if colour == 'white': kingpos, rookleftpos, rookrightpos = 4, 0, 7
        elif colour == 'black': kingpos, rookleftpos, rookrightpos = 60, 56, 63
        else:
            raise core.ColourError('%r is neither white nor black' % colour)

        # See if king or rook out of place.
        if not isking(kingpos):
            self.board.cancastleleft = False; self.board.cancastleright = False
            castleleft = False; castleright = False
        else:
            if not isrook(rookleftpos):
                castleleft = False; self.board.cancastleleft = False
            if not isrook(rookrightpos):
                castleright = False; self.board.cancastleright = False

        # See if there are pieces between the rook and king.
        if self._piecesbetween(rookleftpos, kingpos):
            castleleft = False
        if self._piecesbetween(rookrightpos, kingpos):
            castleright = False

        # See if the castle start/end/during puts the king in check.
        castleleftsteps = range(kingpos-1, kingpos - 3, -1)
        for step in castleleftsteps:
            if self.illegalmove((kingpos, step), colour):
                castleleft = False
            else:
                continue
        castlerightsteps = range(kingpos+1, kingpos + 3)
        for step in castlerightsteps:
            if self.illegalmove((kingpos, step), colour):
                castleright = False
            else:
                continue

        # Then see what if castle moves can be added.
        if castleleft:
            castlemoves.append(
                ((kingpos, kingpos-2), (rookleftpos, rookleftpos+3))
            )
        if castleright:
            castlemoves.append(
                ((kingpos, kingpos+2), (rookleftpos, rookleftpos-2))
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
