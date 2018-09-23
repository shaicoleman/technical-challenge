import unittest
from solver import solver


class PaintshopTest(unittest.TestCase):


    def test_impossible(self):
        demands = [[1, 1, 0], [1, 1, 1]]
        self.assertEqual(solver(1, 2, demands), None)

    def test_no_matte(self):
        demands = [[1, 1, 0], [1, 2, 0]]
        self.assertEqual(solver(2, 2, demands), [0, 0])

    def test_all_matte(self):
        demands = [[1, 1, 1], [2, 1, 0, 2, 1], [3, 1, 0, 2, 0, 3, 1]]
        self.assertEqual(solver(3, 3, demands), [1, 1, 1])

    def test_color_not_requested(self):
        demands = [[1, 5, 1], [2, 1, 0, 2, 1]]
        self.assertEqual(solver(5, 2, demands), [0, 0, 0, 0, 1])

if __name__ == "__main__":
     unittest.main()
