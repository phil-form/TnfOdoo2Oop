import unittest
from calculs import addition
from calculs import division

class TestMath(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(addition(2, 3), 5)

    def test_division_by_zero(self):
        with self.assertRaises(ValueError):
            division(50, 0)

if __name__ == "__main__":
    unittest.main()