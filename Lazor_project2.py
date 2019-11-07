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
COLORS = {
    # Color VAILD White
    VALID: (255, 255, 255),
    # Color INVALID BLACK
    INVALID: (0, 0, 0),
    # Color LAZOR Red
    LAZOR: (255, 0, 0),


    FIXED_REFLECT : (255, 0, 0),
    FIXED_OPAQUE : (255, 0, 0),
    FIXED_REFRACT : (255, 0, 0),


    REFLECT : (255, 0, 0),
    OPAQUE : (255, 0, 0),
    REFRACT : (255, 0, 0),
    # Color ENDPOINT Blue
    ENDPOINT: (0, 0, 255),
    # Color Lazor contact with Endpoint Purple
    HIT : (0, 0, 255)
}

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
    laser = ''
    points = []
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
            laser = line


    # Get data on grid
    grid_str = keep[start_idx + 1:stop_idx]
    for i in range(len(grid_str)):
        grid_str[i] = grid_str[i].replace(' ','')
        arr.append(list(grid_str[i]))

    print(arr)

    for i in range(0, len(arr)):
        for j in range(0, len(arr[i])):
            if arr[i][j] == 'o':
                arr[i][j] = int(arr[i][j].replace('o', '0'))
            if arr[i][j] == 'x':
                arr[i][j] = int(arr[i][j].replace('x', '1'))
            if arr[i][j] == 'B':
                arr[i][j] = int(arr[i][j].replace('B', '3'))
            if arr[i][j] == 'A':
                arr[i][j] = int(arr[i][j].replace('A', '4'))
            if arr[i][j] == 'C':
                arr[i][j] = int(arr[i][j].replace('x', '5'))

    blockSize = 2
    # print(arr)

    arr = increaseSize(arr, blockSize)

    for i in range(0, len(arr)):
        arr[i] = increaseSize(arr[i], blockSize)

    for i in range(0, len(points)):
        T = list(points[i].replace(" ", ""))
        x = int(int(T[1]))
        y = int(int(T[2]))
        if x >= len(arr):
            x = x - 1
        if y >= len(arr):
            y = y - 1
        arr[y][x] = 9

    # # print(arr)
    width = len(arr[0])
    length = len(arr)
    basename = "lazor"
    SIZE = (width, length)
    # Creating the image file
    # Note that the image is all black
    img = Image.new("RGB", SIZE, color=COLORS[VALID])


    for y, row in enumerate(arr):
        for x, block_ID in enumerate(row):
            # Change the color of the specified pixel
            img.putpixel((x, y), COLORS[block_ID])

    # Saving the image
    img.save("%s_%d_%d_%d.png"
             % (basename, width, length, blockSize))



    # now get the number of blocks for each block type
    reflect = reflect[1:].strip()
    opaque = opaque[1:].strip()
    refract = refract[1:].strip()

    num_blocks = [reflect, opaque, refract]

    # now get info on the laser (position and direction of beam)
    laser = laser[1:].strip().split()
    laser_dir = (int(laser[2]), int(laser[3]))
    laser_pos = (int(laser[0]), int(laser[1]))

    return grid_str, num_blocks, laser_pos, laser_dir

if __name__ == "__main__":
    grid_str, num_blocks, laser_pos, laser_dir = read_file("mad_1.bff")
    # print(grid_str)
    # game1 = create_grid(grid_str)

    # game1.board(grid_str)
    # game1.