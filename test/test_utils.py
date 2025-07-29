import unittest
from workflow.scripts.utils import get_b0s


class TestGetB0s(unittest.TestCase):
    def test_get_b0s(self):
        # assert equal 6
        self.assertEqual(get_b0s("test/data/simple.bval"), 6)
