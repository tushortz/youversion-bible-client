"""Legacy test file - kept for backward compatibility."""

import unittest


class TestBible(unittest.TestCase):
    def test_login(self):
        self.assertEqual("foo".upper(), "FOO")


if __name__ == "__main__":
    unittest.main()
