# DESCRIPTION: Tests the vector class.

# 4920646f6e5c2774206361726520696620697420776f726b73206f6e20796f7572206d61636869
# 6e652120576520617265206e6f74207368697070696e6720796f7572206d616368696e6521

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import unittest
from lib import chessvectors as vectors

def errormessage(resultstring, expectedstring):
    """Does the formatting for the error message"""
    return "\n\nRESULT: %s.\nEXPECTED: %s." % (resultstring, expectedstring)


class MiscellaneousVectorCalls(unittest.TestCase):
    """These tests are for the random methods that lie around in the class."""

    def setUp(self):
        self.vector = vectors.Vector(1, 2)

    def test_init(self):
        self.assertEqual(
            self.vector.vector, (1, 2)
        )
        return None

    def test_str(self):
        self.assertEqual(
            str(self.vector), "(1, 2)"
        )
        return None

    def test_equality(self):
        self.assertTrue(self.vector == vectors.Vector(1, 2))
        self.assertFalse(self.vector == vectors.Vector(0, 5))
        return None

    def test_inequality(self):
        self.assertTrue(self.vector != vectors.Vector(0, 9))
        self.assertFalse(self.vector != vectors.Vector(1, 2))


class BadInputVectorTests(unittest.TestCase):
    """Use bad inputs on the methods and see if they fail appropriately."""

    def setUp(self):
        self.vector = vectors.Vector(2, 3)
        self.stringinput = ("2", "3")
        self.floatinput = (2.1, 3.0)
        return None

    def test_initparametersarestrings(self):
        with self.assertRaises(TypeError):
            vectors.Vector(*self.stringinput)
        return None

    def test_initparametersarefloats(self):
        with self.assertRaises(TypeError):
            vectors.Vector(*self.floatinput)
        return None

    def test_addnonvector(self):
        with self.assertRaises(TypeError):
            self.vector + (1, 5)
        return None

    def test_subtractnonvector(self):
        with self.assertRaises(TypeError):
            self.vector - "(-3, 5)"
        return None

    def test_multiplybadscalar(self):
        with self.assertRaises(TypeError):
            self.vector * 9.1
        return None

    def test_multiplybadvector(self):
        with self.assertRaises(TypeError):
            self.vector * (1, 5)
        return None

    def test_equalitynonvector(self):
        with self.assertRaises(TypeError):
            self.vector == (1, 2)
        return None


class BasicVectorPlusOperator(unittest.TestCase):
    """Tests the plus operator for the Vector class."""

    def setUp(self):
        self.vector1 = vectors.Vector(3, 3)
        self.vector2 = vectors.Vector(5, 5)
        self.ans = (8, 8)
        return None

    def test_privatemethod_add(self):
        self.assertEqual(
            tuple(self.vector1._add(self.vector2)), self.ans,
            errormessage(
                str(tuple(self.vector1._add(self.vector2))),
                str(self.ans)
            )
        )
        return None

    def test_addvectors(self):
        resultant1 = self.vector1 + self.vector2
        resultant2 = self.vector2 + self.vector1

        self.assertEqual(
            resultant1.vector, self.ans,
            errormessage(
                "%s + %s = %s" % (self.vector1, self.vector2, resultant1),
                "%s + %s = %s" % (self.vector1, self.vector2, self.ans)
            )
        )
        self.assertEqual(
            resultant2.vector, self.ans,
            errormessage(
                "%s + %s = %s" % (self.vector1, self.vector2, resultant2),
                "%s + %s = %s" % (self.vector1, self.vector2, self.ans)
            )
        )
        return None

    def test_plusequaloperator(self):
        resultant = self.vector1
        resultant += self.vector2
        ans = (8, 8)
        self.assertEqual(
            resultant.vector, self.ans,
            errormessage(
                "%s += %s -> %s" % (self.vector1, self.vector2, resultant),
                "%s += %s -> %s" % (self.vector1, self.vector2, self.ans)
            )
        )
        return None


class BasicVectorMinusOperator(unittest.TestCase):
    """Tests the overloaded minus operator."""

    def setUp(self):
        self.vector1 = vectors.Vector(3, 3)
        self.vector2 = vectors.Vector(5, 5)
        self.ans1 = (-2, -2)
        self.ans2 = (2, 2)
        return None

    def test_subtractvectors(self):
        resultant1 = self.vector1 - self.vector2
        resultant2 = self.vector2 - self.vector1

        self.assertEqual(
            resultant1.vector, self.ans1,
            errormessage(
                "%s - %s = %s" % (self.vector1, self.vector2, resultant1),
                "%s - %s = %s" % (self.vector1, self.vector2, self.ans1)
            )
        )
        self.assertEqual(
            resultant2.vector, self.ans2,
            errormessage(
                "%s - %s = %s" % (self.vector1, self.vector2, resultant2),
                "%s - %s = %s" % (self.vector1, self.vector2, self.ans2)
            )
        )
        return None

    def test_minusequaloperator(self):
        resultant = self.vector1
        resultant -= self.vector2
        self.assertEqual(
            resultant.vector, self.ans1,
            errormessage(
                "%s -= %s -> %s" % (self.vector1, self.vector2, resultant),
                "%s -= %s -> %s" % (self.vector1, self.vector2, self.ans1)
            )
        )
        return None

if __name__ == '__main__':
    unittest.main(verbosity=2)
