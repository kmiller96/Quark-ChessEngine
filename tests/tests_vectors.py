# DESCRIPTION: Contains all of the unit tests for the vector class.

# 4920646f6e5c2774206361726520696620697420776f726b73206f6e20796f7572206d61636869
# 6e652120576520617265206e6f74207368697070696e6720796f7572206d616368696e6521

# DEVELOPMENT LOG:
#    02/01/17: Initialized the testing suite.
#    03/01/17: Wrote basic tests for the Vector class. TODO: add more tests for
# when there are bad inputs. For example, passing a string into intmultipleof
# or adding a vector with a tuple.


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~IMPORTS/GLOBALS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from time import time
import unittest
from random import randint, choice
from lib import core
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.:.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~TESTING~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class TestVectors(unittest.TestCase):
    """Contains all of the tests for the Vector class"""

    def setUp(self):
        self.vector = core.Vector(5, 8)
        return None

    def tearDown(self):
        self.vector = None
        return None

    def test_string_representation(self):
        self.assertEqual('(5, 8)', str(self.vector))
        return None

    def test_tupleform(self):
        self.assertEqual((5, 8), self.vector.tupleform())
        return None

    def test_intmultipleof(self):
        goodvector = core.Vector(10, 16)
        badvector = core.Vector(1, 1)

        self.assertTrue(goodvector.intmultipleof(self.vector))
        self.assertFalse(self.vector.intmultipleof(badvector))
        return None

    def unitvector(self):
        self.vector = core.Vector(5, 5)
        unitvec = core.Vector(1, 1)

        self.assertEqual(self.vector.unitvector(), unitvec)
        return None

    def test_equality(self):
        # TODO: Write up tests for when strings, lists etc. passed.
        goodvector = core.Vector(5, 8)
        badvector = core.Vector(5, 7)

        self.assertEqual(goodvector, self.vector)
        self.assertNotEqual(badvector, self.vector)
        return None

    def test_adding_operations(self):
        # TODO: Write up tests for when strings, lists etc. passed.
        self.assertEqual(core.Vector(4, 2),
            core.Vector(1, 1) + core.Vector(3, 1))

        definevector = core.Vector(8, -2); definevector += core.Vector(2, 2)
        self.assertEqual(core.Vector(10, 0), definevector)

    def test_subtracting_operations(self):
        # TODO: Write up tests for when strings, lists etc. passed.
        self.assertEqual(core.Vector(4, 2),
            core.Vector(7, 3) - core.Vector(3, 1))

        definevector = core.Vector(3, 10); definevector -= core.Vector(1, 5)
        self.assertEqual(core.Vector(2, 5), definevector)

    def test_multiplying_operations(self):
        # TODO: Write up tests for when strings, lists etc. passed.
        self.assertEqual(core.Vector(4, 2), core.Vector(2, 1)*2)
        self.assertEqual(core.Vector(4, 2), 2*core.Vector(2, 1))

        self.assertEqual(12, core.Vector(2, 1)*core.Vector(2, 8))

        definevector = core.Vector(3, -4); definevector *= 3
        self.assertEqual(core.Vector(9, -12), definevector)
        return None

    def test_absolute(self):
        self.assertEqual(5, abs(core.Vector(3, 4)))
        return None
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.:.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~FINAL EXECUTION~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':
    unittest.main(verbosity=2)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.:.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
