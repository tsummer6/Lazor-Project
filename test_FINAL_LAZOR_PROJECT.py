import unittest
import copy
import FINAL_LAZOR_PROJECT

VALID = 0
INVALID = 1
REFRACT = 2
OPAQUE = 3
REFLECT = 4


class GameTest(unittest.TestCase):

    board, blocks, lasers_pos, lasers_dir, targets =\
        FINAL_LAZOR_PROJECT.read_file("dark_1.bff")
    game = FINAL_LAZOR_PROJECT.Game(
        board, blocks, lasers_pos, lasers_dir, targets)
    laser = FINAL_LAZOR_PROJECT.Laser(
        game.lasers_pos[0][0], game.lasers_pos[0][1],
        game.lasers_dir[0][0], game.lasers_dir[0][1])

    def test_create_board(self):
        # Testing to see if the board will be created from
        # the file dark1
        self.game.create_board()
        self.assertEqual(self.game.board, [[1, 0, 0], [0, 0, 0], [0, 0, 1]])

    def test_cardinal(self):
        grid = [[0, 1, 0], [0, 0, 0], [0, 0, 0]]
        grid_faces = copy.deepcopy(grid)
        # Testing the cardinal function
        # This function will give a specified value to a center point and
        # its cardinal points associated (up, down, left and right).
        # It is used to add blocks into the grid space.
        self.game.cardinal(grid, grid_faces, 1, 1, 1)
        self.assertEqual(grid, [[0, 1, 0], [1, 1, 1], [0, 1, 0]])
        self.assertEqual(grid_faces, [[0, 1, 0], [2, 0, 2], [0, 1, 0]])

    def test_create_grid(self):
        # Testing the create_grid function
        # Futher testing the cardinal and create grid functions
        # to see if the grid will convert each block into
        # cross like shape and increase the size of the grid
        self.game.create_grid()
        self.assertEqual(self.game.grid, [
            [0, 1, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1, 1, 1],
            [0, 0, 0, 0, 0, 1, 0]])
        self.assertEqual(self.game.grid_faces, [
            [0, 1, 0, 1, 0, 1, 0],
            [2, 0, 2, 0, 2, 0, 2],
            [0, 1, 0, 1, 0, 1, 0],
            [2, 0, 2, 0, 2, 0, 2],
            [0, 1, 0, 1, 0, 1, 0],
            [2, 0, 2, 0, 2, 0, 2],
            [0, 1, 0, 1, 0, 1, 0]])

    def test_put_block(self):
        # Testing the put_block function
        # This function puts a block of a certain type into the board of the
        # game, and saves the updated board as the self.board variable in
        # the Game() instance.

        block = FINAL_LAZOR_PROJECT.Block(REFRACT)
        self.game.put_block(block, 2, 0)
        self.assertEqual(self.game.board, [[1, 0, 2], [0, 0, 0], [0, 0, 1]])

        # Expects to raise an exception due to adding an VALID block
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

    def test_get_position(self):
        x, y = self.laser.get_position()
        self.assertEqual(x, 3)
        self.assertEqual(y, 0)

    def test_get_direction(self):
        x, y = self.laser.get_direction()
        self.assertEqual(x, -1)
        self.assertEqual(y, 1)

    def test_add_to_path(self):
        xpos, ypos = self.laser.get_position()
        xdir, ydir = self.laser.get_direction()
        nextx = xpos + xdir
        nexty = ypos + ydir
        next_step = [nextx, nexty]
        self.laser.add_to_path(next_step)

        self.assertIn([2, 1], self.laser.path)

    def test_get_trajectory(self):
        trajectory = self.laser.get_trajectory()
        self.assertEqual(trajectory, [[3, 0], [2, 1]])

    def test_reflect_refract_opaque(self):
        xdir, ydir = self.laser.get_direction()
        print(xdir, ydir)
        self.laser.refract(xdir, ydir, 1)
        self.assertEqual(xdir, -1)
        self.assertEqual(ydir, -1)

        xdir, ydir = self.laser.get_direction()
        self.laser.reflect(xdir, ydir, 1)
        xdir, ydir = self.laser.get_direction()
        self.assertEqual(xdir, -1)
        self.assertEqual(ydir, -1)

        self.laser.reflect(xdir, ydir, 2)
        xdir, ydir = self.laser.get_direction()
        self.assertEqual(xdir, 1)
        self.assertEqual(ydir, -1)

        self.laser.absorb(xdir, ydir, 1)
        xdir, ydir = self.laser.get_direction()
        self.assertEqual(xdir, 0)
        self.assertEqual(ydir, 0)
        self.assertIn([-2, -2], self.laser.path)


if __name__ == "__main__":
    unittest.main()
