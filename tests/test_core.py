# DESCRIPTION: Tests the core functions and classes.

# 4920646f6e5c2774206361726520696620697420776f726b73206f6e20796f7572206d61636869
# 6e652120576520617265206e6f74207368697070696e6720796f7572206d616368696e6521

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import unittest
from lib import core

def errormessage(resultstring, expectedstring):
    """Does the formatting for the error message"""
    return "\n\nRESULT: %s.\nEXPECTED: %s." % (resultstring, expectedstring)

class TestBooleanLogic(unittest.TestCase):
    """The tests for the xor and xnor methods."""

    def setUp(self):
        self.a = True
        self.b = False
        self.c = True
        self.d = False
        return None

    def test_xor_truetrue(self):
        result = core.xor(self.a, self.c)
        self.assertFalse(
            result, errormessage(result, "False")
        )
        return None

    def test_xor_truefalse(self):
        result = core.xor(self.a, self.b)
        self.assertTrue(
            result, errormessage(result, "True")
        )
        return None

    def test_xor_falsefalse(self):
        result = core.xor(self.b, self.d)
        self.assertFalse(
            result, errormessage(result, "False")
        )
        return None

    def test_xnor_truetrue(self):
        result = core.xnor(self.a, self.c)
        self.assertTrue(
            result, errormessage(result, "True")
        )
        return None

    def test_xnor_truefalse(self):
        result = core.xnor(self.a, self.b)
        self.assertFalse(
            result, errormessage(result, "False")
        )
        return None

    def test_xnor_falsefalse(self):
        result = core.xnor(self.b, self.d)
        self.assertTrue(
            result, errormessage(result, "True")
        )
        return None


class TestOnlyOneFunction(unittest.TestCase):
    """Tests the function 'onlyone'. Currently there is nothing here."""
    pass


class TestCombineLists(unittest.TestCase):
    """Tests the 'combinelists' method under different conditions."""

    def setUp(self):
        self.func = core.combinelists

    def test_onelist(self):
        flatlist = self.func([1, 2, 3])
        self.assertEqual(
            flatlist, [1, 2, 3],
            errormessage(flatlist, '[1, 2, 3]')
        )
        return None

    def test_twolists(self):
        flatlist = self.func([1, 2], [3, 4])
        self.assertEqual(
            flatlist, [1, 2, 3, 4],
            errormessage(flatlist, '[1, 2, 3, 4]')
        )
        return None

    def test_threelists(self):
        flatlist = self.func([1], [2, 3], [4, 5, 6, 7])
        self.assertEqual(
            flatlist, [1, 2, 3, 4, 5, 6, 7],
            errormessage(flatlist, '[1, 2, 3, 4, 5, 6, 7]')
        )
        return None

    def test_stringinput(self):
        with self.assertRaises(TypeError):
            self.func('string')
        return None

    def test_noniterable(self):
        with self.assertRaises(TypeError):
            self.func(10)
        return None


class TestConvertFunction(unittest.TestCase):
    """This suite, obviously, tests the way the function converts between ints,
    tuples and vectors."""

    def setUp(self):
        self.indexpos = 56
        self.tuplepos = (7, 0)
        self.vectorpos = core.Vector(7, 0)

    def test_convertfunction_indextoindex(self):
        finalpos = core.convert(self.indexpos, toindex=True)
        self.assertEqual(
            finalpos, self.indexpos,
            errormessage(finalpos, self.indexpos)
        )
        return None

    def test_convertfunction_indextocoordinate(self):
        finalpos = core.convert(self.indexpos, tocoordinate=True)
        self.assertEqual(
            finalpos, self.tuplepos,
            errormessage(finalpos, self.tuplepos)
        )
        return None

    def test_convertfunction_indextovector(self):
        finalpos = core.convert(self.indexpos, tovector=True)
        self.assertEqual(
            finalpos, self.vectorpos,
            errormessage(finalpos, self.vectorpos)
        )
        return None

    def test_convertfunction_coordinatetoindex(self):
        finalpos = core.convert(self.tuplepos, toindex=True)
        self.assertEqual(
            finalpos, self.indexpos,
            errormessage(finalpos, self.indexpos)
        )
        return None

    def test_convertfunction_coordtocoord(self):
        finalpos = core.convert(self.tuplepos, tocoordinate=True)
        self.assertEqual(
            finalpos, self.tuplepos,
            errormessage(finalpos, self.tuplepos)
        )
        return None

    def test_convertfunction_coordinatetovector(self):
        finalpos = core.convert(self.tuplepos, tovector=True)
        self.assertEqual(
            finalpos, self.vectorpos,
            errormessage(finalpos, self.vectorpos)
        )
        return None

    def test_convertfunction_vectortoindex(self):
        finalpos = core.convert(self.vectorpos, toindex=True)
        self.assertEqual(
            finalpos, self.indexpos,
            errormessage(finalpos, self.indexpos)
        )
        return None

    def test_convertfunction_vectortocoordinate(self):
        finalpos = core.convert(self.vectorpos, tocoordinate=True)
        self.assertEqual(
            finalpos, self.tuplepos,
            errormessage(finalpos, self.tuplepos)
        )
        return None

    def test_convertfunction_vectortovector(self):
        finalpos = core.convert(self.vectorpos, tovector=True)
        self.assertEqual(
            finalpos, self.vectorpos,
            errormessage(finalpos, self.vectorpos)
        )
        return None


class TestPositionClass(unittest.TestCase):
    """Confirms that the position class behaves as expected."""

    def setUp(self):
        self.indexpos = 41
        self.tuplepos = (5, 1)
        self.vectorpos = core.Vector(5, 1)

    def test_Positionclass_indexinput(self):
        pos = core.Position(self.indexpos)
        self.assertEqual(
            pos.index, self.indexpos,
            errormessage(pos.index, self.indexpos)
        )
        self.assertEqual(
            pos.coordinate, self.tuplepos,
            errormessage(pos.coordinate, self.tuplepos)
        )
        self.assertEqual(
            pos.vector, self.vectorpos,
            errormessage(pos.vector, self.vectorpos)
        )
        return None

    def test_Positionclass_coordinateinput(self):
        pos = core.Position(self.tuplepos)
        self.assertEqual(
            pos.index, self.indexpos,
            errormessage(pos.index, self.indexpos)
        )
        self.assertEqual(
            pos.coordinate, self.tuplepos,
            errormessage(pos.coordinate, self.tuplepos)
        )
        self.assertEqual(
            pos.vector, self.vectorpos,
            errormessage(pos.vector, self.vectorpos)
        )
        return None

    def test_Positionclass_vectorinput(self):
        pos = core.Position(self.vectorpos)
        self.assertEqual(
            pos.index, self.indexpos,
            errormessage(pos.index, self.indexpos)
        )
        self.assertEqual(
            pos.coordinate, self.tuplepos,
            errormessage(pos.coordinate, self.tuplepos)
        )
        self.assertEqual(
            pos.vector, self.vectorpos,
            errormessage(pos.vector, self.vectorpos)
        )
        return None


if __name__ == '__main__':
    unittest.main(verbosity=2)
