import unittest

from inventory.pricing import line_total


class LineTotal(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(line_total(250, 4), 1000)

    def test_negative_quantity(self):
        with self.assertRaises(ValueError):
            line_total(250, -1)


if __name__ == "__main__":
    unittest.main()
