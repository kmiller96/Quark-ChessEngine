# DESCRIPTION: The classes that pertain to the UI and GUI.

# 50726f6772616d6d696e6720697320627265616b696e67206f66206f6e652062696720696d706f
# 737369626c65207461736b20696e746f207365766572616c207665727920736d616c6c20706f73
# 7369626c65207461736b732e

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MAIN~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from lib import core, vectors, pieces

 #     # ###
 #     #  #
 #     #  #
 #     #  #
 #     #  #
 #     #  #
  #####  ###


class EngineUI:
    """The class that handles the UI for the engine."""

    def __init__(self):
        self.history = list()
        self._symboltopiece = {
            'R': pieces.RookPiece,
            'N': pieces.KnightPiece,
            'B': pieces.BishopPiece,
            'Q': pieces.QueenPiece,
            'K': pieces.KingPiece,
            'P': pieces.PawnPiece
        }
        self._ranksymbols = '12345678'
        self._filesymbols = 'abcdefgh'

    def processusermove(self, userstring):
        """Converts the movement notation into an action within the engine."""
        # Determine what piece the user is using.
        def determinepiece(symbol):
            try:
                return self._symboltopiece[symbol]
            except KeyError:
                if symbol.upper() in self._symboltopiece:
                    raise NameError(
                        "I don't know the piece %r. Did you mean %r?" % \
                        (symbol, symbol.upper()))
                else:
                    raise core.UnknownPieceError(
                        "I don't know the piece with the symbol %r." % symbol)

        # Convert the notation into a positon.
        def notationtopositions(notationstring):
            try:
                assert 'x' in notationstring or '>' in notationstring
                (startpos, endpos) = (notationstring[1:3], notationstring[-2:])

                filefunc = lambda x: self._filesymbols.index(x[0])
                rankfunc = lambda x: self._ranksymbols.index(x[1])

                startvec = core.Vector(rankfunc(startpos), filefunc(startpos))
                endvec = core.Vector(rankfunc(endpos), filefunc(endpos))
            except AssertionError:
                if notationstring == '0-0' or notationstring == '0-0-0':
                    pass  # TODO: Castling code.
                else:
                    raise NameError(
                    "The notation string doesn't follow correct syntax rules.")
            else:
                return startvec, endvec

        # Now execute the process in order.
        if not isinstance(userstring, str):
            raise TypeError('Parameter must be a string.')
        elif len(userstring) != 6:
            raise NameError("%r is not syntaxically correct." % userstring)
        piecetomove = determinepiece(userstring[0])
        startvec, endvec = notationtopositions(userstring)
        return piecetomove, (startvec, endvec)

    def addmovetohistory(self, piecesymbol=None, startpos=None, endpos=None,
                         capture=False, check=False, checkmate=False,
                         castlelong=False, castleshort=False, promotionto=False):
        """Add a move to the recorded history."""
        # First turn the position into a notation string.
        def convertpositiontonotation():
            def getpositionstring(pos):
                (rank_, file_) = core.convert(pos, tocoordinate=True)
                return self._filesymbols[file_] + self._ranksymbols[rank_]

            if castlelong:
                return '0-0-0'
            elif castleshort:
                return '0-0'

            startnotation = getpositionstring(startpos)
            endnotation = getpositionstring(endpos)
            if capture: concat = 'x'
            else: concat = '>'

            movestring = piecesymbol + startnotation + concat + endnotation

            if check:
                movestring += '+'
            elif checkmate:
                movestring += '#'
            if promotionto:
                movestring += '=' + promotionto

            return movestring

        # Now add it to the history.
        self.history.append(convertpositiontonotation())
        return None

  #####  #     # ###
 #     # #     #  #
 #       #     #  #
 #  #### #     #  #
 #     # #     #  #
 #     # #     #  #
  #####   #####  ###


class EngineGUI:
    """The class that handles displaying and creating the GUI for the engine.

    The board, once decorated, looks like so:

    + -------- +
    | ....kq.. |
    | .bb..... |
    | ........ |
    | ..pp.... |
    | ..P..N.. |
    | ........ |
    | ....Q... |
    | ..k..... |
    + -------- +

    Where each '.' is a square on the board and the letter are the pieces.
    """

    def __init__(self):
        self.topborder = '  + -------- + \n'
        self.bottomborder = '  + -------- + \n'
        self.leftedgeborder = '| '
        self.rightedgeborder = ' | \n'
        self.ranks = '12345678'
        self.files = 'abcdefgh'
        return None

    def generateasciiboard(self, board, side):
        """Draws the ascii board."""
        def insertsymbolinrankstring(symbol, position, rankstr):
            """Inserts the character into position."""
            ranklist = list(rankstr)
            ranklist[position] = symbol
            rankstr = reduce(lambda x, y: x+y, ranklist)
            return rankstr

        # Sanity checks.
        try:
            assert side in ('white', 'black')
        except AssertionError:
            raise TypeError("The parameter 'side' must be either 'white' or 'black'")

        # Start by drawing an empty board.
        rankstrings = ['........'] * 8

        # Assign piece symbols to the undecorated board.
        for ii, square in enumerate(board):
            if square == None:
                continue
            else:
                piece = square
                symbol = piece.notationsymbol
                (rank_, file_) = core.convert(ii, tocoordinate=True)

                rankstrings[rank_] = \
                    insertsymbolinrankstring(symbol, file_, rankstrings[rank_])

        # Determine which way to print the board.
        if side =='white':
            rankstrings = rankstrings[::-1]
            rankcoordinates = self.ranks[::-1]
            filecoordinates = self.files
        elif side == 'black':
            for ii in range(len(rankstrings)):  # HACK: Reverse ranks too.
                rankstrings[ii] = rankstrings[ii][::-1]
            rankcoordinates = self.ranks
            filecoordinates = self.files[::-1]

        # Now decorate board.
        board = reduce(lambda x, y: x+y, map(
            lambda rankstr, ranknotation: \
                (' ' + ranknotation + self.leftedgeborder +
                rankstr +
                self.rightedgeborder),
            rankstrings, rankcoordinates))
        board = (self.topborder + board + self.bottomborder + '    ' +
                 filecoordinates + '\n')
        return board
