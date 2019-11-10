import time
import random
import numpy as np
from PIL import Image

# DEFINE THINGS
VALID = 0
INVALID = 1
LAZOR = 2

FIXED_REFLECT = 3
FIXED_OPAQUE = 4
FIXED_REFRACT = 5


REFLECT = 6
OPAQUE = 7
REFRACT = 8

ENDPOINT = 9

HIT = 10
# COLORS = {
#     # Color VAILD White
#     VALID: (255, 255, 255),
#     # Color INVALID BLACK
#     INVALID: (0, 0, 0),
#     # Color LAZOR Red
#     LAZOR: (255, 0, 0),


#     FIXED_REFLECT : (255, 0, 0),
#     FIXED_OPAQUE : (255, 0, 0),
#     FIXED_REFRACT : (255, 0, 0),


#     REFLECT : (255, 0, 0),
#     OPAQUE : (255, 0, 0),
#     REFRACT : (255, 0, 0),
#     # Color ENDPOINT Blue
#     ENDPOINT: (0, 0, 255),
#     # Color Lazor contact with Endpoint Purple
#     HIT : (0, 0, 255)
# }

def set_color(img, x0, y0, dim, color):
    '''
    Seeting the color of the image pixels

    **Parameters**

        img: *JPG file*
            Image file, with its extension
            (ex. spring.jpg, cat.png).
        x0: *int*
            X coordinate for width
        y0: *int*
            Y coordinate for height
        dim: *int*
            Size of the block.
        color: *int*
            Color for the maze. During maze generation it will
            be WALL(black) or PATH(white). During the solution it will
            turn the PATH into a VALID_PATH(green), INVALID_PATH(red), and
            an ENDPOINT(blue) with the save_maze function

    **Returns**

        None
    '''

    for x in range(dim):
        for y in range(dim):
            # Change the color of the specified pixel
            img.putpixel(
                (dim * x0 + x, dim * y0 + y),
                color
            )

def save_board(maze, blockSize=2, basename="lazor"):
    '''
    Purpose is to take the 2D array of pixel values
    and save them into a maze as a PNG file

    **Parameters**

        maze: *2D array int*
            A 2 dimensional array of pixel values
            to draw the image
        blockSize: *int optional*
            How much we want to increase the dimensions
            of the image by
        basename: *String optional*
            String used as the first part of the image
            name

    **Returns**

        None
    '''
    # Width of the image
    w_blocks = len(maze[0])
    # Height of the image
    h_blocks = len(maze)
    # Tuple containing the width and length of the image
    # uses the block size to increase the dimensions of the image
    SIZE = (w_blocks * blockSize, h_blocks * blockSize)
    # Creating the image file
    # Note that the image is all black
    img = Image.new("RGB", SIZE, color=COLORS[VALID])
    # Nested for loop to go through the the newly
    # created image file and set different color
    # i.e. the PATH
    for y, row in enumerate(maze):
        for x, block_ID in enumerate(row):
            set_color(img, x, y, blockSize, COLORS[block_ID])
    # Saving the image
    img.save("%s_%d_%d_%d.png"
             % (basename, w_blocks, h_blocks, blockSize))
    return w_blocks, h_blocks


def increaseSize(lst, N):
    return [el for el in lst for _ in range(N)]


def read_file(filename):
    '''
    This function reads in a .bff file and returns the information on
    the board to be constructed.

    **Parameters**

        filename: *str*
            name of the file to be read with its extension


    **Returns**

        grid_str: *list of str*
            a list of strings describing the grid to be constructed. 
            Each character is a cell in the board. 
        num_blocks: *list of ints*
            list containing the number of reflective, opaque and refractive 
            blocks (in that order) that are available to use to solve the board
        laser_pos: *tuple of ints*
            (x, y) coordinates for the position of the laser
        laser_dir: *tuple of ints*
            (x, y) directions of where the laser is pointing to

    '''

    raw_string_of_text = open(filename, 'r').read()

    file_by_lines = raw_string_of_text.strip().splitlines()

    keep = []
    arr = []
    laser_posList = []
    laser_dirList = []
    laser_List = []
    points = []
    points_List = []

    for idx, line in enumerate(file_by_lines):
        if len(file_by_lines[idx]) == 0:
            continue
        if file_by_lines[idx][0] != '#':
            keep.append(file_by_lines[idx])

    start_idx = 0
    stop_idx = 1
    reflect = ''
    refract = ''
    opaque = ''

    for idx, line in enumerate(keep):
        if line == "GRID START":
            start_idx = idx
        if line == "GRID STOP":
            stop_idx = idx
        if line[0] == 'A':
            reflect = line
        if line[0] == 'B':
            opaque = line
        if line[0] == 'C':
            refract = line
        if line[0] == 'P':
            points.append(line)
        if line[0] == 'L':
            laser_List.append(line)


    # Get data on grid
    grid_str = keep[start_idx + 1:stop_idx]
    for i in range(len(grid_str)):
        grid_str[i] = grid_str[i].replace(' ','')
        arr.append(list(grid_str[i]))

    # for i in range(0, len(arr)):
    #     for j in range(0, len(arr[i])):
    #         if arr[i][j] == 'o':
    #             arr[i][j] = int(arr[i][j].replace('o', '0'))
    #         if arr[i][j] == 'x':
    #             arr[i][j] = int(arr[i][j].replace('x', '1'))
    #         if arr[i][j] == 'B':
    #             arr[i][j] = int(arr[i][j].replace('B', '3'))
    #         if arr[i][j] == 'A':
    #             arr[i][j] = int(arr[i][j].replace('A', '4'))
    #         if arr[i][j] == 'C':
    #             arr[i][j] = int(arr[i][j].replace('x', '5'))

    # arr = increaseSize(arr, blockSize)

    # for i in range(0, len(arr)):
    #     arr[i] = increaseSize(arr[i], blockSize)

    # for i in range(0, len(points)):
    #     T = list(points[i].replace(" ", ""))
    #     x = int(int(T[1]))
    #     y = int(int(T[2]))
    #     if x >= len(arr):
    #         x = x - 1
    #     if y >= len(arr):
    #         y = y - 1
    #     arr[y][x] = 9

    # # print(arr)
    width = len(arr[0])
    length = len(arr)
    # basename = "lazor"
    # SIZE = (width, length)
    # # Creating the image file
    # # Note that the image is all black
    # img = Image.new("RGB", SIZE, color=COLORS[VALID])


    # for y, row in enumerate(arr):
    #     for x, block_ID in enumerate(row):
    #         # Change the color of the specified pixel
    #         img.putpixel((x, y), COLORS[block_ID])

    # # Saving the image
    # img.save("%s_%d_%d_%d.png"
    #          % (basename, width, length, blockSize))



    # now get the number of blocks for each block type
    reflect = reflect[1:].strip()
    opaque = opaque[1:].strip()
    refract = refract[1:].strip()

    num_blocks = [reflect, opaque, refract]
    for i in range(0, len(num_blocks)):
        if num_blocks[i] == '':
            num_blocks[i] = '0'

    # now get info on the laser (position and direction of beam)
    for i in range(0, len(laser_List)):
        laser_List[i] = laser_List[i].strip().split()
        p1 = laser_List[i][1]
        p2 = laser_List[i][2]
        p3 = laser_List[i][3]
        p4 = laser_List[i][4]
        laser_posList.append((int(p1), int(p2)))
        laser_dirList.append((int(p3), int(p4)))

    # now get info on the endpoints
    for i in range(0, len(points)):
        points[i] = points[i].strip().split()
        p1 = points[i][1]
        p2 = points[i][2]
        points_List.append([int(p1), int(p2)])

    return grid_str, num_blocks, laser_posList, laser_dirList, points_List

class Game():
    '''
    game class is basically one possible arrangement of the available
    blocks in the grid. It might be a solution or it might not be (this will be
    determined by the solve method). Methods included in the class are:
        - put_block: puts a block of type type in the x and
        y positions specified
        - solve: generates a new game() instance with the
        blocks put in a random
    arrangement and checks to see if all the points are covered

    - Game will create instances of the block types and
    lasers according to input parameters
    '''

    def __init__(self, board_list_of_str, n_blocks, laser_pos=[]):
        '''
        laser_pos: *list of tuples specifyng the position of all lasers
        laser_dir: *list of tuples specifying the direction of each
        laser. Same order as laser_pos.
        '''

        w_blocks = len(board_list_of_str[0])
        h_blocks = len(board_list_of_str)

        self.b_width = w_blocks
        self.b_height = h_blocks
        self.n_blocks = n_blocks
        self.board_str = board_list_of_str

    def create_board(self, board_from_file):
        # initialize board with all valid placements
        board = []

        for i in range(len(board_from_file)):
            board.append(list(grid_str[i]))

        for i in range(0, len(board)):
            for j in range(0, len(board[i])):
                if board[i][j] == 'o':
                    board[i][j] = VALID
                if board[i][j] == 'x':
                    board[i][j] = INVALID
                if board[i][j] == 'B':
                    board[i][j] = FIXED_OPAQUE
                if board[i][j] == 'A':
                    board[i][j] = FIXED_REFLECT
                if board[i][j] == 'C':
                    board[i][j] = FIXED_REFRACT

        return board

    def gen_coordinates(self, board_from_file):
        w_blocks = len(board_from_file[0])
        h_blocks = len(board_from_file)
        while True:
            i = random.randint(0, w_blocks - 1)
            j = random.randint(0, h_blocks - 1)
            if(i - j == 1 or 1 - j == -1 or i - j == 0):
                break
        return i, j

    def add_blocks(self, board_from_file, num_blocks):
        # # initialize board with all valid placements
        n_reflect = num_blocks[0]
        n_opaque = num_blocks[1]
        n_refract = num_blocks[2]

        if(n_reflect != 0):
            for i in range(0, int(n_reflect)):
                while True:
                    i, j = self.gen_coordinates(board_from_file)

                    if board_from_file[i][j] == VALID:
                        board_from_file[i][j] = REFLECT
                        break

        if(n_opaque != 0):
            for i in range(0, int(n_opaque)):
                while True:
                    i, j = self.gen_coordinates(board_from_file)

                    if board_from_file[i][j] == VALID:
                        board_from_file[i][j] = OPAQUE
                        break

        if(n_refract != 0):
            for i in range(0, int(n_refract)):
                while True:
                    i, j = self.gen_coordinates(board_from_file)
                    if board_from_file[i][j] == VALID:
                        board_from_file[i][j] = REFRACT
                        break

        return board_from_file

    def add_points(self, board, ptList, posList):

        n_board = increaseSize(board, 3)
        x = 0
        y = 0
        n_lazorPts = []
        for i in range(0, len(n_board)):
            n_board[i] = increaseSize(n_board[i], 3)

        for i in range(0, len(ptList)):
            for j in range(0, len(ptList[i])):
                if(ptList[i][0] - 3 < 0):
                    x = ptList[i][0]
                    if(ptList[i][1] - 3 < 0):
                        y = ptList[i][1]
                        n_board[y][x] = ENDPOINT
                    if(ptList[i][1] - 3 == 0):
                        y = ptList[i][1] + 1
                        n_board[y][x] = ENDPOINT
                    if(ptList[i][1] - 3 > 0):
                        if(ptList[i][1] == len(board) * 2):
                            y = len(n_board) - 2
                        else:
                            if(ptList[i][1] == 4):
                                y = ptList[i][1] + 1
                            if(ptList[i][1] == 5):
                                y = ptList[i][1] + 2
                            if(ptList[i][1] == 7 or ptList[i][1] == 8):
                                y = ptList[i][1] + 3
                        n_board[y][x] = ENDPOINT
                if(ptList[i][0] - 3 == 0):
                    x = ptList[i][0] + 1
                    if(ptList[i][1] - 3 < 0):
                        y = ptList[i][1]
                        n_board[y][x] = ENDPOINT
                    if(ptList[i][1] - 3 == 0):
                        y = ptList[i][1] + 1
                        n_board[y][x] = ENDPOINT
                    if(ptList[i][1] - 3 > 0):
                        if(ptList[i][1] == len(board) * 2):
                            y = len(n_board) - 2
                        else:
                            if(ptList[i][1] == 4):
                                y = ptList[i][1] + 1
                            if(ptList[i][1] == 5):
                                y = ptList[i][1] + 2
                            if(ptList[i][1] == 7 or ptList[i][1] == 8):
                                y = ptList[i][1] + 3
                    n_board[y][x] = ENDPOINT
                if(ptList[i][0] - 3 > 0):
                    if(ptList[i][0] == len(board) * 2):
                        x = len(n_board) - 1
                    else:
                        x = ptList[i][0] + int(ptList[i][0] / 3) + 1
                    if(ptList[i][1] - 3 < 0):
                        y = ptList[i][1]
                        n_board[y][x] = ENDPOINT
                    if(ptList[i][1] - 3 == 0):
                        y = ptList[i][1] + 1
                        n_board[y][x] = ENDPOINT
                    if(ptList[i][1] - 3 > 0):
                        if(ptList[i][1] == len(board) * 2):
                            y = len(n_board) - 2
                        else:
                            if(ptList[i][1] == 4):
                                y = ptList[i][1] + 1
                            if(ptList[i][1] == 5):
                                y = ptList[i][1] + 2
                            if(ptList[i][1] == 7 or ptList[i][1] == 8):
                                y = ptList[i][1] + 3
                        n_board[y][x] = ENDPOINT

        for i in range(0, len(posList)):
            for j in range(0, len(posList[i])):
                if(posList[i][0] - 3 < 0):
                    x = posList[i][0]
                    if(posList[i][1] - 3 < 0):
                        y = posList[i][1]
                    if(posList[i][1] - 3 == 0):
                        y = posList[i][1] + 1
                    if(posList[i][1] - 3 > 0):
                        if(posList[i][1] == len(board) * 2):
                            y = len(n_board) - 1
                        else:
                            y = len(n_board) - 2
                    n_board[y][x] = LAZOR
                    n_lazorPts.append((x, y))
                if(posList[i][0] - 3 == 0):
                    x = posList[i][0] + 1
                    if(posList[i][1] - 3 < 0):
                        y = posList[i][1]
                    if(posList[i][1] - 3 == 0):
                        y = posList[i][1] + 1
                    if(posList[i][1] - 3 > 0):
                        if(posList[i][1] == len(board) * 2):
                            y = len(n_board) - 1
                        else:
                            y = len(n_board) - 2
                    n_board[y][x] = LAZOR
                    n_lazorPts.append((x, y))
                if(posList[i][0] - 3 > 0):
                    x = posList[i][0] + int(posList[i][0] / 3) + 1
                    if(posList[i][1] - 3 < 0):
                        y = posList[i][1]
                    if(posList[i][1] - 3 == 0):
                        y = posList[i][1] + 1
                    if(posList[i][1] - 3 > 0):
                        if(posList[i][1] == len(board) * 2):
                            y = len(n_board) - 1
                        else:
                            y = len(n_board) - 2
                    n_board[y][x] = LAZOR
                    n_lazorPts.append((x, y))

        new_k = []
        for elem in n_lazorPts:
            if elem not in new_k:
                new_k.append(elem)
        n_lazorPts = new_k

        return n_board, n_lazorPts


    def solve_game(self, n_board, posList, dirList, slow=False):
        w_blocks = len(n_board[0])
        h_blocks = len(n_board)

        for i in range(0, len(posList)):
                dirx, diry = dirList[i]
                x, y = posList[i]
                nx = x
                ny = y
                while True:
                    nx = nx + dirx
                    ny = ny + diry

                    if(nx == 0 or ny == 0):
                        break
                    elif(nx == w_blocks or ny == h_blocks):
                        break
                    else:
                        if(n_board[ny][nx] == OPAQUE or n_board[ny][nx] == FIXED_OPAQUE):
                            break
                        else:
                            n_board[ny][nx] = LAZOR
                            if(n_board[ny][nx] == REFLECT or n_board[ny][nx] == FIXED_REFLECT):
                            if(n_board[ny][nx] == REFRACT or n_board[ny][nx] == FIXED_REFRACT):
                            if(n_board[ny][nx] == ENDPOINT):

        return n_board


if __name__ == "__main__":

    grid_str, num_blocks, posList, dirList, ptList = read_file("tiny_5.bff")
    # grid_str, num_blocks, posList, dirList, ptList = read_file("dark_1.bff")
    game = Game(grid_str, num_blocks)
    board = game.create_board(grid_str)
    board = game.add_blocks(board, num_blocks)
    n_board, newLazPts = game.add_points(board, ptList, posList)

    # for i in range(0, len(n_board)):
    #     print(n_board[i])
    n_board = game.solve_game(n_board, newLazPts, dirList)

    for i in range(0, len(n_board)):
        print(n_board[i])
 