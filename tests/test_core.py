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


class TestConversionBetweenIntTupleAndVector(unittest.TestCase):
    """This suite, obviously, tests the way the script converts between ints,
    tuples and vectors."""


if __name__ == '__main__':
    unittest.main(verbosity=2)
