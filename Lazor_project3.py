import copy 
import random
import time
from itertools import chain 


VALID = 0
INVALID = 1
REFRACT = 2
OPAQUE = 3
REFLECT = 4

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

    # We can open image the image file for the maze
    try:
        raw_string_of_text = open(filename, 'r').read()
    except IOError:
        # Prints this error message if the file does not exist
        print("Error: File does not appear to exist.")
    

    file_by_lines = raw_string_of_text.strip().splitlines()

    keep = []
    start_idx = 0
    stop_idx = 1
    reflect = ''
    refract = ''
    opaque = ''
    lasers_pos = []
    lasers_dir = []
    targets = []

    for idx, line in enumerate(file_by_lines):
        if len(file_by_lines[idx]) == 0:
            continue
        if file_by_lines[idx][0] != '#':
            keep.append(file_by_lines[idx])
  
    for idx, line in enumerate(keep):
        if line == "GRID START":
            start_idx = idx
        if line == "GRID STOP":
            stop_idx = idx
        if line[0] == 'A':
            if "o" not in line: 
                reflect = line
        if line[0] == 'B':
            if "o" not in line: 
                opaque = line
        if line[0] == 'C':
            if "o" not in line: 
                refract = line
        if line[0] == 'P':
            line = line.strip('P').replace(' ','')
            point = [int(line[0]), int(line[1])]
            targets.append(point)
        if line[0] == 'L':
            line = line.strip('L').strip().split(' ')
            # print('yuhu')
            # print(line[2])
            laser_dir = [int(line[2]), int(line[3])]
            laser_pos = [int(line[0]), int(line[1])]

            lasers_pos.append(laser_pos)
            lasers_dir.append(laser_dir)


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
    # laser = laser[1:].strip().split()
    # laser_dir = (int(laser[2]), int(laser[3]))
    # laser_pos = (int(laser[0]), int(laser[1]))

    # print('laserssss')
    # print(lasers_pos)
    # print('didirs')
    # print(lasers_dir)

    # print(board_str)
    # print(targets)
    return board_str, num_blocks, lasers_pos, lasers_dir, targets

def solve_game(filename):
    '''
    Function that solves the game. This function takes a game as an input (this game object already has all the blocks available placed in a specific arrangement) and turns on all the lasers (shoot()). It will then calculate/obtain all the path trajectories from each laser and compare the points in the trajectories to the points that we are targetting. If all the target points are included in the trajectories then the game is solved and the function returns an image representation (or text to simplify) showing which block arrangement solves the puzzle. If any of the target points is missing in the trajectories then the puzzle is not solved, the function will regenerate the game() object and check to see if this new arrangement solves the board.
    '''

    # read data from file
    board_str, num_blocks, lasers_pos, lasers_dir, targets = read_file(filename)
    # print('from read_file output: lasers_pos')
    # print(lasers_pos)
    # print(len(lasers_pos))
    # print(lasers_pos[2])
    # print(lasers_pos[2][0])
    # print('from read_file output: lasers_dir')
    # print(lasers_dir)
    # print('from read_file output: targets')
    # print(targets)

    # initialize Game() instance. Create the initial board. 

    # board_str2 = ['xoo', 'ooo', 'oox']
    # game1 = Game(board_str, num_blocks, lasers_pos, lasers_dir, targets)
    # game1.create_board()
    solved = False
    iterations = 1
    MAX_ITERATIONS = 100000

    grid_List = []
    while solved == False and iterations <= MAX_ITERATIONS:
        game1 = Game(board_str, num_blocks, lasers_pos, lasers_dir, targets)
        game1.create_board()
        game1.create_grid()
        # print('available blocks in solve_game:')
        # for i in range(len(game1.available_blocks)):
        #     print(game1.available_blocks[i].block_type)

        # print('available lasers in solve_game:')
        # for i in range(len(game1.available_lasers)):
        #     print(game1.available_lasers[i].x, game1.available_lasers[i].y)
            # print('with direction:')
            # print(game1.available_lasers[i].xdir, game1.available_lasers[i].ydir)

        # put the blocks available at particular positions.
        # This is the logic that we need to figure out.
        # put transparent blocks first, then reflective ones.
        # Idk in what order the opaques should go (after transparent). 
        # The blocks should be in this order in the available_blocks list.

        # RANDOM LOGIC
        # for each block available get a x and y value within the board list. 
        rand_x = random.randint(0, len(game1.board[0])-1)
        rand_y = random.randint(0, len(game1.board)-1)
        next_rand = [[rand_x, rand_y]]
        print('next_rand:')
        print(next_rand)

        # if the block at rand_x, rand_y is available put block there. Else get another random number for x and y 
        # if the block is adjacent to a target it becomes invalid for reflect and opaque blocks

        all_invalid_adj_blocks = []
        print('printing all targets')
        print(targets)

        for i in targets:
            print(i)
            face = game1.grid_faces[i[1]][i[0]]
            grid_points = []
            if face == 1:
                grid_points = [[i[0],i[1]+1], [i[0],i[1]-1]]
            if face == 2:
                grid_points = [[i[0]+1,i[1]], [i[0]-1,i[1]]]
            # board to grid: m=2n+1
            # grid to board: n=(m-1)/2 (*use this one for this case*)
            # where m and n are the corresponding coordinates in the grid and board respectively
            converted_to_blocks = [[int((grid_points[0][0]-1)/2), int((grid_points[0][1]-1)/2) ], [int((grid_points[1][0]-1)/2), int((grid_points[1][1]-1)/2) ]]
            all_invalid_adj_blocks.extend(converted_to_blocks)
            print('all_invalid_adj_blocks:')
            print(all_invalid_adj_blocks)

        # print('random coords')
        # print(rand_x, rand_y)
        # for i in range(len(game1.board)):
        #     print(game1.board[i])
        # print('looking at value:')
        # print(game1.board[rand_y][rand_x])

        # conditions to place a block in a board position:
        # 1. board position must be valid
        # 2. if block is OPAQUE or REFLECT, board position must not be adjacent to target

        # print('lelele')
        # print(any(elem in all_invalid_adj_blocks for elem in next_rand))

        while True:

            for i in range(len(game1.available_blocks)):
                next_block = game1.available_blocks[i]
                is_placed = False
                # print('current block is:')
                # print(game1.available_blocks[i].block_type)
                # print('current board position being considered:')
                # print()
                print('outside loop')
                while is_placed is False:
                    next_rand = [[rand_x, rand_y]]
                    print('while loop')
                    # print('current block is:')
                    # print(game1.available_blocks[i].block_type)
                    # print('current board position being considered:')
                    # print(next_rand)
                    if game1.board[rand_y][rand_x] is not VALID:
                        print('if game is not valid')
                        rand_x = random.randint(0, len(game1.board[0]) - 1)
                        rand_y = random.randint(0, len(game1.board) - 1)
                        is_placed = False
                    elif game1.board[rand_y][rand_x] is VALID:
                        print('elif')
                        if next_block.block_type == OPAQUE or next_block.block_type == REFLECT:
                            print('if OPAQUE or REFLECT')
                            if any(elem in all_invalid_adj_blocks for elem in next_rand) == True:
                                print('if any position is invalid adj')
                                rand_x = random.randint(0, len(game1.board[0]) - 1)
                                rand_y = random.randint(0, len(game1.board) - 1)
                                is_placed = False
                            else:
                                print('else if no pos is invalid adj')
                                game1.put_block(next_block, rand_x, rand_y)
                                is_placed = True
                        else:
                            print('else if block is not REF or OPAQUE')
                            game1.put_block(next_block, rand_x, rand_y)
                            is_placed = True

            # create grids from the blocks you put
            game1.create_grid()
            check = 0

            if(len(grid_List) != 0):
                for i in range(0, len(grid_List)):
                    if(list(chain.from_iterable(game1.board)) == grid_List[i]):
                        # print(list(chain.from_iterable(game1.board)))
                        # print(grid_List[i])
                        # time.sleep(500)
                        check = 1
            else:
                break

            if check == 0:
                break


        print('board')
        for i in range(len(game1.board)):
            print(game1.board[i])

        # print('grid')
        # for i in range(len(game1.grid)):
        #     print(game1.grid[i])

        # print("grid faces")
        # for j in range(len(game1.grid_faces)):
        #     print(game1.grid_faces[j])

        # print('lasers:')
     
        # for i in range(len(game1.available_lasers)):
        #     # print(game1.available_lasers[i])
        #     print(game1.available_lasers[i])
        # time.sleep(1000)

        for i in range(len(game1.available_lasers)):
            # print(game1.available_lasers[i])
            game1.shoot(game1.available_lasers[i])


        # while loop: while there are lasers that have not been shot do a for loop to shoot all lasers

        all_shot = False
        for i in range(len(game1.available_lasers)):
            if not game1.available_lasers[i].was_shot:
                game1.shoot(game1.available_lasers[i])
            else: 
                print('you shot all your shots')
                all_shot = True


        # once all lasers have been shot, re-check that and then check
        # to see if the targets have been hit.

        # if all the targets have been hit then success you win, return
        # self.board w the winning blocks position. Else: you lost,
        # re-generate another game with a different position for the
        # blocks (assuming it is random)

        if game1.hit_all_targets() == True:
            solved = True
            print(iterations)
            max_iters = iterations + 1
            print("you solved it in %i iterations!" % max_iters)
            print('the winning board is:')
            for i in range(len(game1.board)):
                print(game1.board[i])

        else:
            print("loser")
            print('the board could not be solved under the max specified iterations. Try running it again or increase the max allowed iterations per run')
            solved = False
            grid_List.append(list(chain.from_iterable(game1.board)))
            iterations += iterations
        print(grid_List)



class Game():
    '''

    game class is basically one possible arrangement of the available blocks 
    in the grid. It might be a solution or it might not be (this will
    be determined by the solve method).
    Methods included in the class are:
    - put_block: puts a block of type type in the x and y positions specified
    - solve: generates a new game() instance with the blocks put in a random
    arrangement and checks to see if all the points are covered

    - Game will create instances of the block types and lasers according to input parameters
    
    '''

    def __init__(self, board_list_of_str, num_blocks, lasers_pos, lasers_dir, targets):
        '''
        laser_pos: *list of tuples specifyng the position of all lasers
        laser_dir: *list of tuples specifying the direction of each laser.
        Same order as laser_pos.
        '''
        w_blocks = len(board_list_of_str[0])
        h_blocks = len(board_list_of_str)

        for i in range(len(num_blocks)):
            if num_blocks[i] == '':
                num_blocks[i] = '0'

        self.b_width = w_blocks
        self.b_height = h_blocks
        self.g_width = w_blocks*2+1
        self.g_height = h_blocks*2+1
        self.n_reflect = int(num_blocks[0])
        self.n_opaque = int(num_blocks[1])
        self.n_refract = int(num_blocks[2])
        self.board_str = board_list_of_str
        self.lasers_pos = lasers_pos
        self.lasers_dir = lasers_dir
        self.targets = targets
        self.board = []
        self.grid = []
        self.grid_faces = []


        # Create blocks and lasers available for the game, based on file info
        self.available_blocks = []

        for i in range(self.n_refract):
            block = Block(REFRACT)
            self.available_blocks.append(block) 
        for i in range(self.n_reflect):
            block = Block(REFLECT)
            self.available_blocks.append(block)
        for i in range(self.n_opaque):
            block = Block(OPAQUE)
            self.available_blocks.append(block)


        self.available_lasers = []

        for i in range(len(self.lasers_pos)):
            laser = Laser(self.lasers_pos[i][0], self.lasers_pos[i][1], self.lasers_dir[i][0], self.lasers_dir[i][1])
            self.available_lasers.append(laser)



    def create_board(self):
        # read in file and change the existing board list to match the available positions in the file.
        board = [[VALID for _ in range(self.b_width)] for _ in range(self.b_height)]

        for w in range(self.b_width):
            for h in range(self.b_height):
                if self.board_str[h][w] == 'o':
                    board[h][w] = VALID
                if self.board_str[h][w] == 'x':
                    board[h][w] = INVALID
                if self.board_str[h][w] == 'A':
                    board[h][w] = REFLECT
                if self.board_str[h][w] == 'B':
                    board[h][w] = OPAQUE
                if self.board_str[h][w] == 'C':
                    board[h][w] = REFRACT

        self.board = board

    def create_grid(self):
        '''
        '''
        grid = [[VALID for _ in range(self.g_width)] for _ in range(self.g_height)]

        # for i in range(0, len(grid)):
        #     print(grid[i])
 
        # print(self.g_height)
        # print(self.g_width)
        # print(len(grid))
        grid_faces = copy.deepcopy(grid)

        # for i in range(0, len(grid_faces)):
        #     print(grid_faces[i])

        for w in range(self.b_width):
            for h in range(self.b_height):
                if self.board[h][w] == VALID:
                    # grid[2*h+1][2*w+1] = VALID
                    uselessgrid, grid_faces = self.cardinal(grid, grid_faces, 2*w+1, 2*h+1, VALID)
                    continue
                if self.board[h][w] == INVALID:
                    grid[2*h+1][2*w+1] = INVALID
                    grid, grid_faces = self.cardinal(grid, grid_faces, 2*w+1, 2*h+1, INVALID)
                if self.board[h][w] == REFLECT: # or self.board[h][w].block_type == REFLECT:
                    grid[2*h+1][2*w+1] = REFLECT
                    grid, grid_faces = self.cardinal(grid, grid_faces, 2*w+1, 2*h+1, REFLECT)
                if self.board[h][w] == OPAQUE: # or self.board[h][w].block_type == OPAQUE:
                    grid[2*h+1][2*w+1] = OPAQUE
                    grid, grid_faces = self.cardinal(grid, grid_faces, 2*w+1, 2*h+1, OPAQUE)
                if self.board[h][w] == REFRACT: # or self.board[h][w].block_type == REFRACT:
                    grid[2*h+1][2*w+1] = REFRACT
                    grid, grid_faces = self.cardinal(grid, grid_faces, 2*w+1, 2*h+1, REFRACT)

        self.grid =  grid
        self.grid_faces = grid_faces


    def cardinal(self, grid, grid_faces, x, y, value):
        '''
        This function will give a specified value to a center point 
        and its cardinal 
        points associated. It is used to add blocks into the grid space.

        **Parameters**
            grid: *list of list*
                game grid
            grid_faces: *list of list*
                grid with numbers corresponding to the face of the
                blocks in the board
            x: *int*
                x coordinate of the center point in the grid that corresponds
                to the block to be added
            y: *int*
                y coordinate of the center point in the grid that corresponds
                to the block to be added
            value: *int or codeword (see above)*
                value of the board block that we want to give to the grid positions. 
                Can be valid (0), invalid (1), reflective block (4), opaque block (3),
                refractive block (2) 


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

        # print(len(grid))
        # print(x, y)
        grid[y][x] = value
        grid_faces[y][x] = 0
        i = 1
        for d in dirs:
            if self.within_bounds(grid, d[0],d[1]):
                # print(i)
                local_value = grid[d[1]][d[0]]
                if local_value < value:
                    grid[d[1]][d[0]] = value
                if i == 1 or i == 2:
                    grid_faces[d[1]][d[0]] = 1
                if i == 3 or i == 4:
                    grid_faces[d[1]][d[0]] = 2
                i += 1

        return grid, grid_faces



    def put_block(self, block, x, y):
        '''
        This function puts a block of a certain type into the board of the game

        **Parameters**
            board: *list of list of ints*
                board to be modified
            block: *Block() object*:
                block that you want to put
            x: *int*
                x position of the board block
            y: *int*
                y position of the board block

        **Returns**
            board: *list of list of ints*
                modified board with the added block
        '''
        if block.block_type ==2 or block.block_type ==3 or block.block_type ==4:
            self.board[y][x] = block.block_type
        else:
            raise Exception("Block type input is not valid")
        return self.board


    def within_bounds(self, matrix, x, y):
        '''
        function that checks if a given x and y coordinate is within
        the bounds of a given matrix type object or not. Returns True/False. 

        For laser beams, if it is not anymore then disregard that path.
        If it is in the board take the next step and see if it bumps into anything. 

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

    def get_block_face(self, x, y):
        return self.grid_faces[x][y]

    def hit_all_targets(self):
        total_trajectories = []

        for i in range(len(self.available_lasers)):
            # print('now i am within hit_all_targets')
            # print(self.available_lasers[i])
            # print(self.available_lasers[i].get_trajectory())
            traj = list(self.available_lasers[i].get_trajectory())
            # print('this is traj')
            # print(traj)
            total_trajectories.extend(traj)
            # print('now i extended total_trajectories by traj ')
            # print(total_trajectories)
        print('lfgkhg total trajertories are:')
        print(total_trajectories)
        print('this is self.targets')
        print(self.targets)

        result = all(elem in total_trajectories for elem in self.targets)
        return result

        # for t in self.targets:
        #     print(t)
        #     if t not in total_trajectories:
        #         return False
        #     else:
        #         return True


    def shoot(self, laser):
        '''
        shoots laser, i.e. calculates all the points in the trajectory
        after the blocks have been placed.
        '''

        current_x, current_y = laser.get_position()
        xdir, ydir = laser.get_direction()

        print('current position is:')
        print(current_x, current_y)
        print('grid value at current pos')
        print(self.grid[current_y][current_x])

        lengthx = len(self.grid[0])
        lengthy = len(self.grid)

        # check to see if any block is adjacent to the laser origin
        if self.grid[current_y][current_x] == REFLECT:
            if (self.grid_faces[current_y][current_x] == 2 and self.grid[current_y][current_x+xdir] == REFLECT) or (self.grid_faces[current_y][current_x] == 1 and self.grid[current_y+ydir][current_x] == REFLECT):
                face_number = self.get_block_face(current_x, current_y)
                laser.reflect(xdir, ydir, face_number)
        if self.grid[current_y][current_x] == OPAQUE:
            if (self.grid_faces[current_y][current_x] == 2 and self.grid[current_y][current_x+xdir] == OPAQUE) or (self.grid_faces[current_y][current_x] == 1 and self.grid[current_y+ydir][current_x] == OPAQUE):
            # print('lalalala')
                face_number = self.get_block_face(current_x, current_y)
                laser.absorb(xdir, ydir, face_number)
        if self.grid[current_y][current_x] == REFRACT:
            if (self.grid_faces[current_y][current_x] == 2 and self.grid[current_y][current_x+xdir] == REFRACT) or (self.grid_faces[current_y][current_x] == 1 and self.grid[current_y+ydir][current_x] == REFRACT):
                face_number = self.get_block_face(current_x, current_y)
                laser2 = laser.refract(xdir, ydir, face_number)
                self.available_lasers.append(laser2)

        if laser.get_trajectory()[-1] != [-2,-2]:
            next_x = current_x + xdir
            next_y = current_y + ydir

            print('printing shot laser trajectory before while loop')
            print(laser.get_trajectory())
            while self.within_bounds(self.grid, next_x, next_y) and laser.get_trajectory()[-1] != [-2,-2]:
                print(xdir)
                print(ydir)

                current_x = next_x
                current_y = next_y
                laser.add_to_path([next_x, next_y])

                if self.grid[current_y][current_x] == REFLECT:
                    # time.sleep(2000)
                    #if (self.grid_faces[current_y][current_x] == 2) or (self.grid_faces[current_y][current_x] == 1):
                        # time.sleep(100)
                    # print(current_y)
                    # print(current_x)
                    print(xdir)
                    print(ydir)
                    # print(len(self.grid))
                    # print("This")
                    # print(laser.get_trajectory())
                    # print(self.grid[current_y][current_x+xdir])
                    # print(self.grid[current_y+ydir][current_x])
                    # if (current_x + xdir == lengthx):
                    #     xdir = 0
                    # if (current_y + ydir == lengthy):
                    #     ydir = 0
                    try:
                        if (self.grid_faces[current_y][current_x] == 2 and self.grid[current_y][current_x+xdir] == REFLECT) or (self.grid_faces[current_y][current_x] == 1 and self.grid[current_y+ydir][current_x] == REFLECT):
                            face_number = self.get_block_face(current_x, current_y)
                            laser.reflect(xdir, ydir, face_number)
                            print(current_y, current_x)
                    except IndexError:
                        print("Out of Bounds")
                    
                if self.grid[current_y][current_x] == OPAQUE:
                    if (self.grid_faces[current_y][current_x] == 2 and self.grid[current_y][current_x+xdir] == OPAQUE) or (self.grid_faces[current_y][current_x] == 1 and self.grid[current_y+ydir][current_x] == OPAQUE):
                    # # print('lalalala')
                        face_number = self.get_block_face(current_x,current_y)
                        laser.absorb(xdir, ydir, face_number)
                if self.grid[current_y][current_x] == REFRACT:
                    # print(current_y)
                    # print(current_x)
                    print(xdir)
                    print(ydir)
                    # print(len(self.grid))
                    # print("This")
                    # print(laser.get_trajectory())
                    # print(self.grid[current_y][current_x+xdir])
                    # print(self.grid[current_y+ydir][current_x])
                    # time.sleep(2000)
                    # #if (self.grid_faces[current_y][current_x] == 2) or (self.grid_faces[current_y][current_x] == 1):
                    # if (current_x + xdir == lengthx and ):
                    #     xdir = 0
                    # if (current_y + ydir == lengthy and ):
                    #     ydir = 0

                    try:
                        if (self.grid_faces[current_y][current_x] == 2 and self.grid[current_y][current_x+xdir] == REFRACT) or (self.grid_faces[current_y][current_x] == 1 and self.grid[current_y+ydir][current_x] == REFRACT):
                            face_number = self.get_block_face(current_x,current_y)
                            laser2 = laser.refract(xdir, ydir, face_number)
                            self.available_lasers.append(laser2)
                    except IndexError:
                        print("out of bounds")

                # if self.grid[current_y][current_x] == REFLECT:
                #     face_number = self.get_block_face(current_x,current_y)
                #     laser.reflect(xdir, ydir, face_number)
                # if self.grid[current_y][current_x] == OPAQUE:
                #     face_number = self.get_block_face(current_x,current_y)
                #     laser.absorb(xdir, ydir, face_number)
                # if self.grid[current_y][current_x] == REFRACT:
                #     face_number = self.get_block_face(current_x,current_y)
                #     laser2 = laser.refract(xdir, ydir, face_number)
                #     self.available_lasers.append(laser2)

                next_x = current_x + xdir
                next_y = current_y + ydir

            laser.was_shot = True
            laser.path.append([-1,-1])
            print('printing shot laser trajectory')
            print(laser.get_trajectory())


class Block():

    def __init__(self, block_type, size=2, fixed=False):
        self.block_type = block_type # codeword
        self.fixed = fixed
        self.size = 2

    def isfixed(self):
        return self.fixed



class Laser():

    def __init__(self, x, y, xdir, ydir):
        self.x = x
        self.y = y
        self.xdir = xdir
        self.ydir = ydir
        self.path = [[x, y]] #initiate the path with the starting position
        self.was_shot = False

    def get_position(self):
        '''
        Returns the position of a given laser.
        '''
        return self.x, self.y

    def get_direction(self):
        '''
        Returns x and y directions of laser
        '''
        return self.xdir, self.ydir

    def add_to_path(self, next_step):
        '''
        Appends a step to the laser beam path
        '''
        self.path.append(next_step)

    def get_trajectory(self):
        '''
        Returns the path or paths of that laser as a list of
        tuples with each position the laser goes through

        **Returns** 
            path: *list of tuples*
                list with every position tuple (x,y) that the beam has gone through.
        '''
        return self.path

    def was_shot(self):
        return self.was_shot


    def reflect(self, xdir, ydir, face_number):
        '''
        what happens when the laser beam is reflected.
        Takes in a xdir and a ydir as well as and x and y position
        where the reflection happens, and returns a new laser
        direction and the same x and y positions.

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
        if face_number==1:

            new_xdir = xdir
            new_ydir = - ydir

        if face_number==2:

            new_xdir = - xdir
            new_ydir = ydir

        self.xdir = new_xdir
        self.ydir = new_ydir

        

    def absorb(self, xdir, ydir, face_number):
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

        self.xdir = 0
        self.ydir = 0
        self.path.append([-2,-2])


    def refract(self, xdir, ydir, face_number):
        '''
        Function the describes what happens when a laser beam hits an
        transparent block: light is refracted AND reflected. The function
        creates a new pseudo laser object at the point where the refraction
        occurs to account of the new path being created.

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
                Laser object with the same direction as original laser.
                This returned laser has x,y coordinates at the
                point of refraction.

        '''
        # Creates a second laser from the refracting point, that
        # continues the same path as previously
        refracted_laser = Laser(self.x, self.y, xdir, ydir)
        if face_number == 1:

            second_xdir = xdir
            second_ydir = - ydir

        if face_number==2:

            second_xdir = - xdir
            second_ydir = ydir

        self.xdir = second_xdir
        self.ydir = second_ydir, 
        return refracted_laser


if __name__ == "__main__":

    # solved = solve_game("dark_1.bff")
    solved = solve_game("mad_1.bff")
    # solved = solve_game("tiny_5.bff")
    print('in main')
    print(solved)
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

