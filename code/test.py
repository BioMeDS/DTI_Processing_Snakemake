import unittest
from additional_scripts.helper_functions import get_similar_vectors

class TestHelperFunctions(unittest.TestCase):
	def test_get_similar_vectors(self):
		input = [
			[0, 1, 1, 1, 4, 4, 0, 7],
			[0, 2, 2, 2, 5, 5, 0, 8],
			[0, 3, 3, 3, 6, 6, 0, 9]
		]
		expected = ([0, 6], [[1, 2, 3], [4, 5], [7]])
		self.assertEqual(get_similar_vectors(input), expected)

if __name__ == '__main__':
	unittest.main()