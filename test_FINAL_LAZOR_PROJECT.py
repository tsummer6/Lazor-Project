import unittest
import copy
import random
import FINAL_LAZOR_PROJECT

VALID = 0
INVALID = 1
REFRACT = 2
OPAQUE = 3
REFLECT = 4


class GameTest(unittest.TestCase):

    board, blocks, lasers_pos, lasers_dir, targets = FINAL_LAZOR_PROJECT.read_file("dark_1.bff")
    game = FINAL_LAZOR_PROJECT.Game(board, blocks, lasers_pos, lasers_dir, targets)

    def test_create_board(self):
        self.game.create_board()
        self.assertEqual(self.game.board, [[1, 0, 0], [0, 0, 0], [0, 0, 1]])

    def test_cardinal(self):
        grid = [[0, 1, 0], [0, 0, 0], [0, 0, 0]]
        grid_faces = copy.deepcopy(grid)
        self.game.cardinal(grid, grid_faces, 1, 1, 1)
        self.assertEqual(grid, [[0, 1, 0], [1, 1, 1], [0, 1, 0]])
        self.assertEqual(grid_faces, [[0, 1, 0], [2, 0, 2], [0, 1, 0]])

    def test_create_grid(self):
        self.game.create_grid()
        self.assertEqual(self.game.grid, [[0, 1, 0, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 1, 1, 1], [0, 0, 0, 0, 0, 1, 0]])
        self.assertEqual(self.game.grid_faces, [[0, 1, 0, 1, 0, 1, 0], [2, 0, 2, 0, 2, 0, 2], [0, 1, 0, 1, 0, 1, 0], [2, 0, 2, 0, 2, 0, 2], [0, 1, 0, 1, 0, 1, 0], [2, 0, 2, 0, 2, 0, 2], [0, 1, 0, 1, 0, 1, 0]])


    def test_put_block(self):
        block = FINAL_LAZOR_PROJECT.Block(REFRACT)
        self.game.put_block(block, 2, 0)
        self.assertEqual(self.game.board, [[1, 0, 2], [0, 0, 0], [0, 0, 1]])

        block = FINAL_LAZOR_PROJECT.Block(VALID)
        with self.assertRaises(Exception):
            self.game.put_block(block, 2, 1)

    def test_within_bounds(self):
        a = self.game.within_bounds(self.game.board, 0, 0)
        self.assertTrue(a)
        b = self.game.within_bounds(self.game.board, 4, 7)
        self.assertFalse(b)

    def test_get_block_face(self):
        a = self.game.get_block_face(6, 1)
        self.assertEqual(a, 1)
        b = self.game.get_block_face(6, 2)
        self.assertEqual(b, 0)
        c = self.game.get_block_face(1, 0)
        self.assertEqual(c, 2)

    def test_hit_all_targets(self):
        self.game.hit_all_targets()
        self.assertEqual(self.game.grid, )

    def test_shoot(self):
        self.game.shoot()
        self.assertEqual(self.game.grid, )



# class LazorProject(unittest.TestCase):
#   def test_read_file(self):
#       board, blocks, lasers_pos, lasers_dir, targets = read_file("dark_1.bff")

#   def test_solve_gameself(self):
#       pass

if __name__ == "__main__":
    unittest.main()
    # print("hello world")