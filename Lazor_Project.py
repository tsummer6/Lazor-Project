
def read_file(filename):
    '''
    This function reads in a .bff file and returns the information on the board to be constructed.

    **Parameters**

        filename: *str*
            name of the file to be read with its extension


    **Returns**
        
        grid_str: *list of str*
            a list of strings describing the grid to be constructed. Each character is a cell in the board. 
        num_blocks: *list of ints*
            list containing the number of reflective, opaque and refractive blocks (in that order) that are available to use to solve the board
        laser_pos: *tuple of ints*
            (x, y) coordinates for the position of the laser
        laser_dir: *tuple of ints*
            (x, y) directions of where the laser is pointing to



    '''

    raw_string_of_text = open(filename, 'r').read()

    file_by_lines = raw_string_of_text.strip().splitlines()

    keep = []
    discard = []
    for idx, line in enumerate(file_by_lines):
        if len(file_by_lines[idx]) == 0:
            continue
        if file_by_lines[idx][0] == '#':
            discard.append(file_by_lines[idx])
        else:
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
        if line[0] =='B':
            opaque = line
        if line[0] == 'C':
            refract = line
        if line[0] == 'P':
            points.append(line)
        if line[0] == 'L':
            laser = line


    #get data on grid
    grid_str = keep[start_idx+1:stop_idx]
    for i in range(len(grid_str)):
        string = grid_str[i]
        string2 = string.replace(' ','')
        grid_str[i] = string2

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

# def create_grid(grid_str):
#     '''
#     creates a class object of the board to be played.
#     x = no block allowed
#     o = blocks allowed
#     A = fixed reflect block
#     B = fixed opaque block
#     C = fixed refract block
#     '''
#     w_blocks = len(grid_str[0])
#     h_blocks = len(grid_str)

#     game =  Game(w_blocks*2, h_blocks*2)
#     return game


VALID = 0
INVALID = 1
REFLECT = 2
OPAQUE = 3
REFRACT = 4

def solve_game(game):
    '''
    Function that solves the game. This function takes a game as an input (this game object already has all the blocks available placed in a specific arrangement) and turns on all the lasers (shoot()). It will then calculate/obtain all the path trajectories from each laser and compare the points in the trajectories to the points that we are targetting. If all the target points are included in the trajectories then the game is solved and the function returns an image representation (or text to simplify) showing which block arrangement solves the puzzle. If any of the target points is missing in the trajectories then the puzzle is not solved, the function will regenerate the game() object and check to see if this new arrangement solves the board.
    '''
    pass

class Game():
    '''
    game class is basically one possible arrangement of the available blocks in the grid. It might be a solution or it might not be (this will be determined by the solve method).
    Methods included in the class are:
    - put_block: puts a block of type type in the x and y positions specified
    - solve: generates a new game() instance with the blocks put in a random arrangement and checks to see if all the points are covered

    - Game will create instances of the block types and lasers according to input parameters
    '''

    def __init__(self, grid_list_of_str, n_reflect=0, n_opaque=0, n_refract=0, laser_pos=[]):
        '''
        laser_pos: *list of tuples specifyng the position of all lasers
        laser_dir: *list of tuples specifying the direction of each laser. Same order as laser_pos. 
        '''
        w_blocks = len(grid_list_of_str[0])
        h_blocks = len(grid_list_of_str)

        self.width = w_blocks*2
        self.height = h_blocks*2
        self.n_reflect = n_reflect
        self.n_opaque = n_opaque
        self.n_refract = n_refract

    def create_board(self, board_from_file):
        # initialize board with all valid placements
        board = [[VALID for _ in range(self.width)] for _ in range(self.height)]
        # read in file and change the existing board list to match the available positions in the file.


        return board
        # return [h[w]==0 for h in range(self.height) for w in range(self.width)]

    def put_block(self, type, x, y):
        pass



class Block():

    def __init__(self, block_type, size=2, fixed=False):
        self.block_type = block_type
        self.fixed = fixed
        self.size = 2

    def isfixed(self):
        return self.fixed

    def reflect(self, incoming_dir):
        pass

    def refract(self, incoming_dir):
        pass

    def opaque(self, incoming_dir):
        pass



class Laser():

    def __init__(self, x, y, xdir, ydir):
        self.x = x
        self.y = y
        self.xdir = xdir
        self.ydir = ydir
        self.path = [(x, y)] #initiate the path with the starting position

    def position(self):
        return [self.x, self.y]

    def add_to_path(self, list_of_steps):
        self.path.append(list_of_steps)

    def get_trajectory(self):
        return self.path

    def shoot(self):
        '''
        shoots laser, i.e. calculates all the points in the trajectory after the blocks have been placed.
        '''
        pass

    def reflect(self):
        '''
        what happens when the laser beam is reflected
        '''
        pass

    def absorb(self):
        '''
        what happens when the laser beam is absorbed by an opaque block
        '''
        pass

    def refract(self):
        '''
        what happens when the laser beam is refracted by a transparent block
        '''
        pass





if __name__ == "__main__":
    grid_str, num_blocks, laser_pos, laser_dir = read_file("mad_1.bff")

    game1 = create_grid(grid_str)

    game1.board(grid_str)
    game1.

