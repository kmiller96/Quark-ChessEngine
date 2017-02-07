# DESCRIPTION: Tests the UI and GUI.

# 4920646f6e5c2774206361726520696620697420776f726b73206f6e20796f7572206d61636869
# 6e652120576520617265206e6f74207368697070696e6720796f7572206d616368696e6521

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import unittest
from lib import core, chessboard, pieces, usercontrol

class BasicUICalls(unittest.TestCase):
    """Conducts the very basic tests on the UI."""

    def setUp(self):
        self.ui = usercontrol.EngineUI()
        return None

    def test_processusermove_King(self):
        startpos = core.Vector(4, 4)
        endpos = core.Vector(5, 4)
        piece = pieces.KingPiece
        string = 'Ke5>Ke6'
        self.assertEqual(
            self.ui.processusermove(string),
            (piece, (startpos, endpos))
        )
        return None

    def test_processusermove_Queen(self):
        startpos = core.Vector(2, 3)
        endpos = core.Vector(3, 4)
        piece = pieces.QueenPiece
        string = 'Qd3>Ke4'
        self.assertEqual(
            self.ui.processusermove(string),
            (piece, (startpos, endpos))
        )
        return None

class BasicGUICalls(unittest.TestCase):
    """Conducts tests on the GUI."""

    def setUp(self):
        return None


if __name__ == '__main__':
    unittest.main(verbosity=2)
