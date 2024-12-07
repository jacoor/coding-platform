import unittest

# Test class
class TestMathFunctions(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5) # noqa F821 (undefined name 'add')
        self.assertEqual(add(-1, 1), 0) # noqa F821 (undefined name 'add')
        self.assertEqual(add(-1, -1), -2) # noqa F821 (undefined name 'add')
        self.assertEqual(add(-1, -1), -3) # noqa F821 (undefined name 'add')

    def test_subtract(self):
        self.assertEqual(subtract(5, 3), 2) # noqa F821 (undefined name 'subtract')
        self.assertEqual(subtract(1, 1), 0) # noqa F821 (undefined name 'subtract')
        self.assertEqual(subtract(-1, -1), 0) # noqa F821 (undefined name 'subtract')
