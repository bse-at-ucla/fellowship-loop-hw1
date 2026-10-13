import unittest

from auth import is_expired


class TestExpiry(unittest.TestCase):
    def test_future_token_is_valid(self):
        self.assertFalse(is_expired(200, 100))

    def test_past_token_is_expired(self):
        self.assertTrue(is_expired(50, 100))

    def test_token_expiring_right_now_is_expired(self):
        self.assertTrue(is_expired(100, 100))


if __name__ == "__main__":
    unittest.main()
