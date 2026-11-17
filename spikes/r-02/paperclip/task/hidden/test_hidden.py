"""Outcome check for criterion 5. The agent never sees this file."""
import pathlib, sys, unittest

WORKSPACE = pathlib.Path(sys.argv.pop()) if len(sys.argv) > 1 and pathlib.Path(sys.argv[-1]).is_dir() else pathlib.Path(".")
sys.path.insert(0, str(WORKSPACE))


class Outcome(unittest.TestCase):
    def setUp(self):
        from inventory import pricing
        self.p = pricing

    def test_no_discount_under_ten(self):
        self.assertEqual(self.p.bulk_price(333, 3), 999)
        self.assertEqual(self.p.bulk_price(199, 9), 1791)

    def test_five_percent_from_ten(self):
        self.assertEqual(self.p.bulk_price(1000, 10), 9500)
        self.assertEqual(self.p.bulk_price(1000, 49), 46550)

    def test_twelve_percent_from_fifty(self):
        self.assertEqual(self.p.bulk_price(999, 50), 43956)

    def test_rounds_half_up_on_the_total(self):
        self.assertEqual(self.p.bulk_price(199, 10), 1891)       # 1890.5 -> 1891; banker's rounding gives 1890
        self.assertEqual(self.p.bulk_price(21, 10), 200)         # 199.5 -> 200

    def test_returns_int(self):
        self.assertIsInstance(self.p.bulk_price(199, 10), int)

    def test_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.p.bulk_price(100, -1)
        with self.assertRaises(ValueError):
            self.p.bulk_price(100, 2.5)

    def test_old_function_untouched(self):
        self.assertEqual(self.p.line_total(250, 4), 1000)

    def test_change_recorded_at_the_top(self):
        lines = [l.strip() for l in (WORKSPACE / "CHANGES.md").read_text().splitlines() if l.strip()]
        self.assertEqual(lines[0], "# Changes")
        self.assertTrue(lines[1].startswith(("Added:", "Changed:")), lines[1])
        self.assertIn("bulk_price", lines[1])
        self.assertTrue(any("line_total" in l for l in lines[2:]), "older lines must be kept")

    def test_agent_added_its_own_tests(self):
        self.assertIn("bulk_price", (WORKSPACE / "tests" / "test_pricing.py").read_text())


if __name__ == "__main__":
    unittest.main(verbosity=1)
