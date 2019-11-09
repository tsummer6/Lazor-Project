import copy 

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
    board_str = keep[start_idx+1:stop_idx]
    for i in range(len(board_str)):
        string = board_str[i]
        string2 = string.replace(' ','')
        board_str[i] = string2

    # now get the number of blocks for each block type
    reflect = reflect[1:].strip()
    opaque = opaque[1:].strip()
    refract = refract[1:].strip()

    num_blocks = [reflect, opaque, refract]

    # now get info on the laser (position and direction of beam)
    laser = laser[1:].strip().split()
    laser_dir = (int(laser[2]), int(laser[3]))
    laser_pos = (int(laser[0]), int(laser[1]))

    print(board_str)
    return board_str, num_blocks, laser_pos, laser_dir

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

def solve_game(filename):
    '''
    Function that solves the game. This function takes a game as an input (this game object already has all the blocks available placed in a specific arrangement) and turns on all the lasers (shoot()). It will then calculate/obtain all the path trajectories from each laser and compare the points in the trajectories to the points that we are targetting. If all the target points are included in the trajectories then the game is solved and the function returns an image representation (or text to simplify) showing which block arrangement solves the puzzle. If any of the target points is missing in the trajectories then the puzzle is not solved, the function will regenerate the game() object and check to see if this new arrangement solves the board.
    '''
    board_str, num_blocks, laser_pos, laser_dir = read_file(filename)

    # board_str2 = ['xoo', 'ooo', 'oox']
    game1 = Game(board_str)
    board1 = game1.create_board()
    grid1, gridfaces1 = game1.create_grid(board1)

    print("num_blocks")
    print(num_blocks)
    print("laser position")
    print(laser_pos)
    print("laser dir")
    print(laser_dir)

    for i in range(len(board1)):
        print(board1[i])

    for i in range(len(grid1)):
        print(grid1[i])

    print("jhdfhjdsfb")
    for j in range(len(gridfaces1)):
        print(gridfaces1[j])

    num_reflect = num_blocks[0]
    num_opaque = num_blocks[1]
    num_refract = num_blocks[2]
    total_blocks = num_refract + num_opaque + num_reflect


    pass

def shoot(laser):
        '''
        shoots laser, i.e. calculates all the points in the trajectory after the blocks have been placed.
        '''

        current_x, current_y = get_position(laser)
        xdir, ydri = get_direction(laser)
        next_x = current_x + xdir
        next_y = current_y + ydir





        #  something along the lines of:
        # if not within_board:
        # dont do anything, we dont care anymore about this path
        # if board[next_y][next_x] == REFLECT:
        #     self.reflect(next_x, next_y, xdir, ydir)
        # same for OPAQUE and REFRACT





        pass

class Game():
    '''
    game class is basically one possible arrangement of the available blocks in the grid. It might be a solution or it might not be (this will be determined by the solve method).
    Methods included in the class are:
    - put_block: puts a block of type type in the x and y positions specified
    - solve: generates a new game() instance with the blocks put in a random arrangement and checks to see if all the points are covered

    - Game will create instances of the block types and lasers according to input parameters
    '''

    def __init__(self, board_list_of_str, n_reflect=0, n_opaque=0, n_refract=0, laser_pos=[]): 
        '''
        laser_pos: *list of tuples specifyng the position of all lasers
        laser_dir: *list of tuples specifying the direction of each laser. Same order as laser_pos. 
        '''
        w_blocks = len(board_list_of_str[0])
        h_blocks = len(board_list_of_str)

        self.b_width = w_blocks
        self.b_height = h_blocks
        self.g_width = w_blocks*2+1
        self.g_height = h_blocks*2+1
        self.n_reflect = n_reflect
        self.n_opaque = n_opaque
        self.n_refract = n_refract
        self.board_str = board_list_of_str

    def create_board(self):
        # read in file and change the existing board list to match the available positions in the file.
        board = [[VALID for _ in range(self.b_width)] for _ in range(self.b_height)]

        for w in range(self.b_width):
            for h in range(self.b_height):
                if self.board_str[h][w] == 'o':
                    # print("valid")
                    board[h][w] = VALID
                    # grid[2*h+1][2*w+1] = VALID
                    # grid = self.cardinal(grid,2*w+1, 2*h+1, VALID)
                if self.board_str[h][w] == 'x':
                    # print("invalid")
                    board[h][w] = INVALID
                    # grid[2*h+1][2*w+1] = INVALID
                    # grid = self.cardinal(grid,2*w+1, 2*h+1, INVALID)
                if self.board_str[h][w] == 'A':
                    # print("reflect")
                    board[h][w] = REFLECT
                    # grid[2*h+1][2*w+1] = REFLECT
                    # grid = self.cardinal(grid,2*w+1, 2*h+1, REFLECT)
                if self.board_str[h][w] == 'B':
                    # print("opaque")
                    board[h][w] = OPAQUE
                    # grid[2*h+1][2*w+1] = OPAQUE
                    # grid = self.cardinal(grid,2*w+1, 2*h+1, OPAQUE)
                if self.board_str[h][w] == 'C':
                    # print("refract")
                    board[h][w] = REFRACT
                    # grid[2*h+1][2*w+1] = REFRACT
                    # grid = self.cardinal(grid,2*w+1, 2*h+1, REFRACT)

        return board

    def create_grid(self, board):
        '''
        '''
        grid = [[VALID for _ in range(self.g_height)] for _ in range(self.g_width)]
        grid_faces = copy.deepcopy(grid)

        for w in range(self.b_width):
            for h in range(self.b_height):
                if board[h][w] == VALID:
                    # grid[2*h+1][2*w+1] = VALID
                    # grid = self.cardinal(grid,2*w+1, 2*h+1, VALID)
                    continue
                if board[h][w] == INVALID:
                    grid[2*h+1][2*w+1] = INVALID
                    grid, grid_faces = self.cardinal(grid, grid_faces, 2*w+1, 2*h+1, INVALID)
                if board[h][w] == REFLECT:
                    grid[2*h+1][2*w+1] = REFLECT
                    grid, grid_faces = self.cardinal(grid, grid_faces, 2*w+1, 2*h+1, REFLECT)
                if board[h][w] == OPAQUE:
                    grid[2*h+1][2*w+1] = OPAQUE
                    grid, grid_faces = self.cardinal(grid, grid_faces, 2*w+1, 2*h+1, OPAQUE)
                if board[h][w] == REFRACT:
                    grid[2*h+1][2*w+1] = REFRACT
                    grid, grid_faces = self.cardinal(grid, grid_faces, 2*w+1, 2*h+1, REFRACT)

        return grid, grid_faces


    def cardinal(self, grid, grid_faces, x, y, value):
        '''
        This function will give a specified value to a center point and its cardinal points associated. It is used to add blocks into the grid space.

        **Parameters**
            grid: *list of list*
                game grid
            grid_faces: *list of list*
                grid with numbers corresponding to the face of the blocks in the board
            x: *int*
                x coordinate of the center point in the grid that corresponds to the block to be added
            y: *int*
                y coordinate of the center point in the grid that corresponds to the block to be added
            value: *int or codeword (see above)*
                value of the board block that we want to give to the grid positions. Can be valid (0), invalid (1), reflective block (2), opaque block (3), refractive block (4) 


        **Returns**
            grid: *list of list*
                the grid with the new block added

        '''
        current = [x, y]
        up = [current[0], current[1]-1]
        down = [current[0], current[1]+1]
        left = [current[0]-1, current[1]]
        right = [current[0]+1, current[1]]
        dirs = [up, down, left, right] #list of lists


        grid[y][x] = value
        grid_faces[y][x] = 0
        i = 1
        for d in dirs:
            if self.within_bounds(grid, d[0],d[1]):
                # print(i)
                grid[d[1]][d[0]] = value
                grid_faces[d[1]][d[0]] = i
                i += 1

        return grid, grid_faces



    def put_block(self, board, block_type, x, y):
        '''
        This function puts a block of a certain type into the board of the game

        **Parameters**
            board: *list of list of ints*
                board to be modified
            type: *int or codeword (see above)*:
                type of block to be added. REFLECT (2), OPAQUE (3) or REFRACT (4). Could also be a free open block space VALID (0) or a tile with no space for a block INVALID (1).
            x: *int*
                x position of the board block
            y: *int*
                y position of the board block

        **Returns**
            board: *list of list of ints*
                modified board with the added block
        '''
        if block_type == 0 or 1 or 2 or 3 or 4 or 5:
            board[y][x] == block_type
        else:
            raise Exception("Block type input is not valid")
        return board
        

    def within_bounds(self, matrix, x, y):
        '''
        function that checks if a given x and y coordinate is within the bounds of a given matrix type object or not. Returns True/False. 

        For laser beams, if it is not anymore then disregard that path. If it is in the board take the next step and see if it bumps into anything. 

        **Parameters**

            matrix: *list of lists*
                List of lists representing the matrix (board, grid)
            x: *int*
                x coordinate of the position in question
            y: *int*
                y coordinate of the position in question

        **Returns**

            TRUE if (x, y) is within the matrix bounds
            FALSE if (x, y) is outside the matrix bounds
        '''
        lengthx = len(matrix[0])
        lengthy = len(matrix)

        if x<0 or x > (lengthx-1) or y < 0 or y > (lengthy-1):
            return False
        return True

    def check_block_face(self, grid_faces, x, y, value):
        
        pass

class Block():

    def __init__(self, block_type, size=2, fixed=False):
        self.block_type = block_type
        self.fixed = fixed
        self.size = 2

    def isfixed(self):
        return self.fixed

    # def reflect(self, incoming_dir):
    #     pass

    # def refract(self, incoming_dir):
    #     pass

    # def opaque(self, incoming_dir):
    #     pass



class Laser():

    def __init__(self, x, y, xdir, ydir):
        self.x = x
        self.y = y
        self.xdir = xdir
        self.ydir = ydir
        self.path = [(x, y)] #initiate the path with the starting position

    def get_position(self):
        '''
        Returns the position of a given laser.

        '''
        return self.x, self.y

    def get_direction(self):
        return self.xdir, self.ydir

    def add_to_path(self, path_number, next_step):
        self.path[path_number].append(next_step)

    def get_trajectory(self):
        '''
        Returns the path or paths of that laser as a list of tuples with each position the laser goes through

        **Returns** 
            path: *list of tuples*
                list with every position tuple (x,y) that the beam has gone through.
        '''
        return self.path

    # def new_path(self):
    #     '''
        # '''

    def check_block_face(self, grid_faces, x, y, value):

        pass


    def reflect(self, x, y, xdir, ydir):
        '''
        what happens when the laser beam is reflected. Takes in a xdir and a ydir as well as and x and y position where the reflection happens, and returns a new laser direction and the same x and y positions.

        Function reflects the direction of the laser coming in

        **Parameters**

            x: *int*
                current path position x coordinate where the reflection occurs
            y: *int*
                current path position y coordinate where the reflection occurs
            xdir: *int*
                incoming direction (x component) of the path to be reflected
            ydir: *int*
                incoming direction (y component) of the path to be reflected


        **Returns**
            new_xdir: *int*
                outbound laser direction (x component)
            new_ydir: *int*
                outbound laser direction (y component)
            x: *int*
                current x coordinate where reflection took place
            y: *int*
                current y coordinate where reflection took place

        '''
        if check_block_face(grid_faces, x, y, 1) or check_block_face(grid_faces, x, y, 2):

            new_xdir = xdir
            new_ydir = - ydir

        if check_block_face(grid_faces, x, y, 3) or check_block_face(grid_faces, x, y, 4):

            new_xdir = - xdir
            new_ydir = ydir

        return new_xdir, new_ydir, x, y 

        

    def absorb(self, x, y, xdir, ydir):
        '''
        Function the describes what happens when a laser beam hits an opaque block: light is absorbed.

        **Parameters**

            x: *int*
                current path position x coordinate where the absorption occurs
            y: *int*
                current path position y coordinate where the absorption occurs
            xdir: *int*
                incoming direction (x component) of the path to be absorbed
            ydir: *int*
                incoming direction (y component) of the path to be absorbed


        **Returns**
            new_xdir: *int*
                Outbound laser direction. Set to zero because the laser doesnt have any direction past this point
            new_ydir: *int*
                outbound laser direction. Set to zero because the laser doesnt have any direction past this point
            x: *int*
                current x coordinate where absorption took place
            y: *int*
                current y coordinate where absorption took place

        '''
        new_xdir = 0
        new_ydir = 0

        return new_xdir, new_ydir, x, y  
        

    def refract(self, x, y, xdir, ydir):
        '''
        Function the describes what happens when a laser beam hits an transparent block: light is refracted AND reflected. The function creates a new pseudo laser object at the point where the refraction occurs to account of the new path being created. 

        **Parameters**

            x: *int*
                current path position x coordinate where the refraction occurs
            y: *int*
                current path position y coordinate where the refraction occurs
            xdir: *int*
                incoming direction (x component) of the path to be refracted
            ydir: *int*
                incoming direction (y component) of the path to be refracted


        **Returns**
            second_xdir: *int*
                Outbound reflected beam x direction.
            second_ydir: *int*
                Outbound reflected laser y direction.
            refracted_laser: *Laser class object*
                Laser object with the same direction as original laser. This returned laser has x,y coordinates at the point of refraction.
        '''
        refracted_laser = Laser(x, y, xdir, ydir) #creates a second laser from the refracting point, that continues the same path as previously
        if check_block_face(grid_faces, x, y, 1) or check_block_face(grid_faces, x, y, 2):

            second_xdir = xdir
            second_ydir = - ydir

        if check_block_face(grid_faces, x, y, 3) or check_block_face(grid_faces, x, y, 4):

            second_xdir = - xdir
            second_ydir = ydir

        return second_xdir, second_ydir, refracted_laser



if __name__ == "__main__":

    solved = solve_game("mad_1.bff")
    # board_str, num_blocks, laser_pos, laser_dir = read_file("dark_1.bff")

    # board_str2 = ['xoo', 'ooo', 'oox']
    # game1 = Game(board_str2)
    # board1 = game1.create_board()
    # grid1, gridfaces1 = game1.create_grid(board1)
    # print(board1)

    # for i in range(len(grid1)):
    #     print(grid1[i])

    # print("jhdfhjdsfb")
    # for j in range(len(gridfaces1)):
    #     print(gridfaces1[j])

    # game1 = create_grid(grid_str)

    # game1.board(grid_str)
    # game1.

