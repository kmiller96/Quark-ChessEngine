# DESCRIPTION: Tests the UI and GUI.

# 4920646f6e5c2774206361726520696620697420776f726b73206f6e20796f7572206d61636869
# 6e652120576520617265206e6f74207368697070696e6720796f7572206d616368696e6521

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# TODO: Finsih off these tests.

import unittest
from lib import core, chessboard, pieces, usercontrol
from tests.test_core import errormessage

class BasicUICalls(unittest.TestCase):
    """Conducts the very basic tests on the UI."""

    def setUp(self):
        self.ui = usercontrol.EngineUI()
        return None

    def test_processusermove_King(self):
        startpos = core.Vector(4, 4)
        endpos = core.Vector(5, 4)
        piece = pieces.KingPiece
        string = 'Ke5>e6'
        self.assertEqual(
            self.ui.processusermove(string),
            (piece, (startpos, endpos))
        )
        return None

    def test_processusermove_Queen(self):
        startpos = core.Vector(2, 3)
        endpos = core.Vector(3, 4)
        piece = pieces.QueenPiece
        string = 'Qd3>e4'
        self.assertEqual(
            self.ui.processusermove(string),
            (piece, (startpos, endpos))
        )
        return None

    def test_processusermove_Bishop(self):
        startpos = core.Vector(0, 7)
        endpos = core.Vector(1, 6)
        piece = pieces.BishopPiece
        string = 'Bh1>g2'
        self.assertEqual(
            self.ui.processusermove(string),
            (piece, (startpos, endpos))
        )
        return None

    def test_processusermove_Knight(self):
        startpos = core.Vector(0, 5)
        endpos = core.Vector(2, 4)
        piece = pieces.KnightPiece
        string = 'Nf1>e3'
        self.assertEqual(
            self.ui.processusermove(string),
            (piece, (startpos, endpos))
        )
        return None

    def test_processusermove_Rook(self):
        startpos = core.Vector(0, 0)
        endpos = core.Vector(5, 0)
        piece = pieces.RookPiece
        string = 'Ra1>a6'
        self.assertEqual(
            self.ui.processusermove(string),
            (piece, (startpos, endpos))
        )
        return None

    def test_processusermove_Pawn(self):
        startpos = core.Vector(1, 4)
        endpos = core.Vector(3, 4)
        piece = pieces.PawnPiece
        string = 'Pe2>e4'
        self.assertEqual(
            self.ui.processusermove(string),
            (piece, (startpos, endpos))
        )
        return None

    def test_processusermove_badstring(self):
        with self.assertRaises(NameError):
            self.ui.processusermove('hello there')
        with self.assertRaises(NameError):
            self.ui.processusermove('Kg1>Jd2')
        return None

    def test_processusermove_badnotation(self):
        with self.assertRaises(core.UnknownPieceError):
            self.ui.processusermove('Me4>e6')
        return None

    def test_processusermove_nonstring(self):
        with self.assertRaises(TypeError):
            self.ui.processusermove([5, 1])
        with self.assertRaises(TypeError):
            self.ui.processusermove(12)
        with self.assertRaises(TypeError):
            self.ui.processusermove(-5.22)
        with self.assertRaises(TypeError):
            self.ui.processusermove(pieces.KingPiece)
        return None

    def test_addmovetohistory_basicmove(self):
        movestring = 'Pe2>e4'
        self.ui.addmovetohistory('P', 12, 28)
        self.assertEqual(
            self.ui.history[-1], movestring,
            errormessage(self.ui.history[-1], movestring)
        )
        return None

    def test_addmovetohistory_capture(self):
        movestring = 'Qe5xd5'
        self.ui.addmovetohistory('Q', 36, 35, capture=True)
        self.assertEqual(
            self.ui.history[-1], movestring,
            errormessage(self.ui.history[-1], movestring)
        )
        return None

    def test_addmovetohistory_check(self):
        movestring = 'Qe5>d5+'
        self.ui.addmovetohistory('Q', 36, 35, check=True)
        self.assertEqual(
            self.ui.history[-1], movestring,
            errormessage(self.ui.history[-1], movestring)
        )
        return None

    def test_addmovetohistory_checkmate(self):
        movestring = 'Bh7>f5#'
        self.ui.addmovetohistory('B', 55, 37, checkmate=True)
        self.assertEqual(
            self.ui.history[-1], movestring,
            errormessage(self.ui.history[-1], movestring)
        )
        return None

    def test_addmovetohistory_castlelong(self):
        movestring = '0-0-0'
        self.ui.addmovetohistory(castlelong=True)
        self.assertEqual(
            self.ui.history[-1], movestring,
            errormessage(self.ui.history[-1], movestring)
        )
        return None

    def test_addmovetohistory_castleshort(self):
        movestring = '0-0'
        self.ui.addmovetohistory(castleshort=True)
        self.assertEqual(
            self.ui.history[-1], movestring,
            errormessage(self.ui.history[-1], movestring)
        )
        return None

    def test_addmovetohistory_promotionto(self):
        movestring = 'Pa7>a8=Q'
        self.ui.addmovetohistory('P', 48, 56, promotionto='Q')
        self.assertEqual(
            self.ui.history[-1], movestring,
            errormessage(self.ui.history[-1], movestring)
        )
        return None


class BasicGUICalls(unittest.TestCase):
    """Conducts tests on the GUI."""

    def setUp(self):
        self.gui = usercontrol.EngineGUI()
        self.board = chessboard.ChessBoard()
        self.board.setupnormalboard()
        return None

    def test_generateasciiboard(self):
        print "\n"
        print self.gui.generateasciiboard(self.board, 'white')
        return None


if __name__ == '__main__':
    unittest.main(verbosity=2)
