import copy 
import random 
from PIL import Image


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

def save_board(board, blockSize=2, basename="lazor_solution_"):
    '''
    Purpose is to take the 2D array of pixel values
    and save them into a board as a PNG file
    **Parameters**
        board: *2D array int*
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
    w_blocks = len(board[0])
    # Height of the image
    h_blocks = len(board)
    # Tuple containing the width and length of the image
    # uses the block size to increase the dimensions of the image
    SIZE = (w_blocks * blockSize, h_blocks * blockSize)
    # Creating the image file
    # Note that the image is all black
    img = Image.new("RGB", SIZE, color=COLORS[VALID])
    # Nested for loop to go through the the newly
    # created image file and set different color
    # i.e. the PATH
    for y, row in enumerate(board):
        for x, block_ID in enumerate(row):
            set_color(img, x, y, blockSize, COLORS[block_ID])
    # Saving the image
    img.save("%s_%d_%d_%d.png"
             % (basename, w_blocks, h_blocks, blockSize))



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
        laser_pos: *tlist*
            [x, y] coordinates for the positions of the lasers
        laser_dir: *list*
            [x, y] directions of where the lasers are pointing to
        targets: *list*
            [x,y] coordinates of the taerget points
    '''
    file = open(filename,'r')
    raw_string_of_text = file.read()

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
    lasers_pos = []
    lasers_dir = []
    targets = []
    for idx, line in enumerate(keep):
        if line == "GRID START":
            start_idx = idx
        if line == "GRID STOP":
            stop_idx = idx
        if line[0] == 'A':
            if "o" not in line:
                reflect = line
        if line[0] =='B':
            if 'o' not in line:
                opaque = line
        if line[0] == 'C':
            if 'o' not in line:
                refract = line
        if line[0] == 'P':
            line = line.strip('P').replace(' ','')
            point = [int(line[0]), int(line[1])]
            targets.append(point)
        if line[0] == 'L':
            line = line.strip('L').strip().split(' ')
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
    # print(board_str)
    file.close()

    return board_str, num_blocks, lasers_pos, lasers_dir, targets


VALID = 0
INVALID = 1
REFRACT = 2
OPAQUE = 3
REFLECT = 4

COLORS = {
    # Color VAILD White
    VALID: (255, 255, 255),
    # Color INVALID Black
    INVALID: (0, 0, 0),
    # Color REFLECT Red
    REFLECT: (255, 0, 0),
    # Color OPAQUE Green
    OPAQUE: (0, 255, 0),
    # Color REFRACT Blue
    REFRACT: (0, 0, 255),

}

def solve_game(filename):
    '''
    Function that solves the game. This function takes a game as an input (this game object already has all the blocks available placed in a specific arrangement) and turns on all the lasers (shoot()). It will then calculate/obtain all the path trajectories from each laser and compare the points in the trajectories to the points that we are targetting. If all the target points are included in the trajectories then the game is solved and the function returns an image representation (or text to simplify) showing which block arrangement solves the puzzle. If any of the target points is missing in the trajectories then the puzzle is not solved, the function will regenerate the game() object and check to see if this new arrangement solves the board.

    **Parameters**

        filename: *str*
            filename plus extension of the file you want to read the game information from.

    **Returns**
        solved: *bool*
            True if game was solved, False if it was not
        board: *list*
            Board representation of the solution


    '''

    board_str, num_blocks, lasers_pos, lasers_dir, targets = read_file(filename)
    
    solved = False
    iterations = 0
    MAX_ITERATIONS = 10000000
    board_List = []

    # game1 = Game(board_str, num_blocks, lasers_pos, lasers_dir, targets)
    # game1.create_board()
    # game1.create_grid()
    # board_List.append(game1.board) #appends the empty board to initialize board_List

    while solved == False and iterations <= MAX_ITERATIONS:
        game1 = Game(board_str, num_blocks, lasers_pos, lasers_dir, targets)
        game1.create_board()
        game1.create_grid()

        # put the blocks available at particular positions. This is the logic that we need to figure out. 
        # put transparent blocks first, then reflective ones. Idk in what order the opaques should go (after transparent). The blocks should be in this order in the available_blocks list.

        # RANDOM LOGIC (NOT COMPLETELY RANDOM - has some positioning constraints)

        # for each block available get an x and y value within the board list. 
        rand_x = random.randint(0, len(game1.board[0])-1)
        rand_y = random.randint(0, len(game1.board)-1)
        next_rand = [[rand_x, rand_y]]

        # if the block at rand_x, rand_y is VALID put block there. Else get another random number for x and y 
        # if a target is on the edge of the board, then the block adjacent to the target becomes invalid for reflect and opaque blocks. If the target is not on the edge of the board, then the invalid block is the one adjacent to it from the side that the laser beam is coming.

        all_invalid_adj_blocks = []

        border_xs = [0, len(game1.grid[0])-1]
        border_ys = [0, len(game1.grid)-1]
        for i in targets:
            # print(i)
            if i[0] in border_xs or i[1] in border_ys:
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

        # conditions to place a block in a board position:
        # 1. board position must be valid
        # 2. if block is OPAQUE or REFLECT, board position must not be adjacent to target


        for i in range(len(game1.available_blocks)):
            next_block = game1.available_blocks[i]
            is_placed = False

            while is_placed == False:
                next_rand = [[rand_x, rand_y]]

                if game1.board[rand_y][rand_x] is not VALID:
                    rand_x = random.randint(0, len(game1.board[0])-1)
                    rand_y = random.randint(0, len(game1.board)-1)
                    is_placed = False

                elif game1.board[rand_y][rand_x] is VALID:
                    if next_block.block_type == OPAQUE or next_block.block_type == REFLECT:
                        if any(elem in all_invalid_adj_blocks for elem in next_rand) == True:
                            rand_x = random.randint(0, len(game1.board[0])-1)
                            rand_y = random.randint(0, len(game1.board)-1)
                            is_placed = False

                        else:
                            game1.put_block(next_block, rand_x, rand_y)
                            is_placed = True

                    else:
                        game1.put_block(next_block, rand_x, rand_y)
                        is_placed = True


        # create grids from the blocks you put
        game1.create_grid()

        if(len(board_List) != 0):
            if game1.board in board_List:
                pass

        #         for i in range(len(board_List)):
        #             if(game1.board == board_List[i]):
        #                 game1.create_board()
        #                 game1.create_grid()
        #                 rand_x = random.randint(0, len(game1.board[0]) - 1)
        #                 rand_y = random.randint(0, len(game1.board) - 1)

        print('board')
        for i in range(len(game1.board)):
            print(game1.board[i])

        for i in range(len(game1.available_lasers)):
            game1.shoot(game1.available_lasers[i])


        # while loop: while there are lasers that have not been shot do a for loop to shoot all lasers

        # all_shot = False
        # for i in range(len(game1.available_lasers)):
        #     if not game1.available_lasers[i].was_shot:
        #         game1.shoot(game1.available_lasers[i])
        #     else: 
        #         print('you shot all your shots')
        #         all_shot = True

        all_shot = False
 
        for i in range(len(game1.available_lasers)):
            if not game1.available_lasers[i].was_shot:
                game1.shoot(game1.available_lasers[i])

            # print(game1.available_lasers[i].get_trajectory())


        # once all lasers have been shot, re-check that and then check to see if the targets have been hit.

        # if all the targets have been hit then success you win, return self.board w the winning blocks position. Else: you lost, re-generate another game with a different position for the blocks (assuming it is random)


        if game1.hit_all_targets() == True:
            solved = True
            # print(iterations)
            max_iters = iterations + 1
            save_board(game1.board, blockSize=100)
            print("you solved it in %i iterations!" %max_iters)
            print('the winning board is:')
            for i in range(len(game1.board)):
                print(game1.board[i])

        else:
            board_List.append(game1.board)
            solve = False
            iterations += 1
            print("NEW BOARD")

        if iterations >= MAX_ITERATIONS:
            print("loser")
            print('the board could not be solved under the max specified iterations. Try running it again or increase the max allowed iterations per run')
            # print(iterations)
            solved = False
            

    return solved, game1.board


class Game():
    '''
    Game class contains the read in board, and generates Laser() and Block() instances accordingly, based on the read-in file.

    Methods included in the class are:
    - put_block: puts a block of type type in the x and y positions specified
    - solve: generates a new game() instance with the available blocks put in a random arrangement and checks to see if all the points are covered
    - Game will create instances of the block types and lasers according to input parameters
    '''

    def __init__(self, board_list_of_str, num_blocks, lasers_pos, lasers_dir, targets):
        '''
        Initializes Game() instance.

        board_list_of_str: list of strings corresponding to the board to be build
        num_blocks: list with the amount of each REFLECT, OPAQUE and REFRACT blocks in that order
        laser_pos: list of list specifyng the position of all lasers
        laser_dir: list of list specifying the direction of each laser. Same order as laser_pos. 
        targets: list of all the points the lasers are targeting.

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
        '''
        First initializes a board of the necessary dimensions and then populates it with the corresponding blocks from the base file.
        Stores the generated board as a self variable of the Game() instance.
        '''

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
        First initializes a grid of the necessary dimensions and duplicates it. The function then populates the first grid to match with the corresponding blocks from the self.board variable generated before.
        The function populates the duplicate grid with the values corresponding to the vertical (2) or horizontal (1) faces of each cube. This will determine laser behaviour when it encounters the blocks.
        Stores the generated grids as a self variables of the Game() instance.
        '''
        grid = [[VALID for _ in range(self.g_width)] for _ in range(self.g_height)]
        grid_faces = copy.deepcopy(grid)

        for w in range(self.b_width):
            for h in range(self.b_height):
                if self.board[h][w] == VALID:
                    uselessgrid, grid_faces = self.cardinal(grid, grid_faces, 2*w+1, 2*h+1, VALID)
                    continue
                if self.board[h][w] == INVALID:
                    grid[2*h+1][2*w+1] = INVALID
                    grid, grid_faces = self.cardinal(grid, grid_faces, 2*w+1, 2*h+1, INVALID)
                if self.board[h][w] == REFLECT: 
                    grid[2*h+1][2*w+1] = REFLECT
                    grid, grid_faces = self.cardinal(grid, grid_faces, 2*w+1, 2*h+1, REFLECT)
                if self.board[h][w] == OPAQUE:
                    grid[2*h+1][2*w+1] = OPAQUE
                    grid, grid_faces = self.cardinal(grid, grid_faces, 2*w+1, 2*h+1, OPAQUE)
                if self.board[h][w] == REFRACT: 
                    grid[2*h+1][2*w+1] = REFRACT
                    grid, grid_faces = self.cardinal(grid, grid_faces, 2*w+1, 2*h+1, REFRACT)

        self.grid =  grid
        self.grid_faces = grid_faces


    def cardinal(self, grid, grid_faces, x, y, value):
        '''
        This function will give a specified value to a center point and its cardinal points associated (up, down, left and right). It is used to add blocks into the grid space.

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
                value of the board block that we want to give to the grid positions. Can be valid (0), invalid (1), reflective block (4), opaque block (3), refractive block (2) 

        **Returns**

            grid: *list of list*
                the grid with the new block added
            grid_face: *list of list*
                the grid with the face values of the block that was put
        '''
        current = [x, y]
        up = [current[0], current[1]-1]
        down = [current[0], current[1]+1]
        left = [current[0]-1, current[1]]
        right = [current[0]+1, current[1]]
        dirs = [up, down, left, right] 


        grid[y][x] = value
        grid_faces[y][x] = 0
        i = 1
        for d in dirs:
            if self.within_bounds(grid, d[0],d[1]):
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
        This function puts a block of a certain type into the board of the game, and saves the updated board as the self.board variable in the Game() instance.

        **Parameters**

            block: *Block() object*:
                block that you want to put
            x: *int*
                x position of the board block (not of the grids)
            y: *int*
                y position of the board block (not of the grids)

        
        '''
        if block.block_type ==2 or block.block_type ==3 or block.block_type ==4:
            self.board[y][x] = block.block_type
        else:
            raise Exception("Block type input is not valid")
        return self.board
        

    def within_bounds(self, matrix, x, y):
        '''
        Function that checks if a given x and y coordinate is within the bounds of a given matrix type object or not. Returns True/False. 
        For laser beams, if the point is not within bounds anymore then disregard that path. If it is in the board take the next step and see if it bumps into anything. 

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
        '''
        Returns the value of the block face at a given x and y coordinates(1 or 2 for horizontal or vertical faces respectively)
        '''      
        return self.grid_faces[y][x]

    def hit_all_targets(self):
        '''
        This function checks if all the target points are covered in the lasers' trajectories. It pools all trajectories from the different available lasers and compares the list of target points to this list of trajectories. If all targets are within the trajectory list the function returns True. If one or more points are missing in the trajectories returns False. 
        '''

        total_trajectories = []

        for i in range(len(self.available_lasers)):
            traj = list(self.available_lasers[i].get_trajectory())
            total_trajectories.extend(traj)

        result = all(elem in total_trajectories for elem in self.targets)
        return result
        

    def shoot(self, laser):
        '''
        This funciton shoots a given laser, i.e. calculates all the points in the trajectory after the blocks have been placed. It does so stepwise and appends each step to the self.path variable in the laser.
        '''
        print('we\'re shooting laser: ' + str(laser.x) + ', ' + str(laser.y))
        print('so far it\'s trajectory is: ' + str(laser.path))

        # print('grid faces:')
        # for i in range(len(self.grid_faces)):
        #     print(self.grid_faces[i])

        current_x, current_y = laser.get_position()
        xdir, ydir = laser.get_direction()

        # check to see if any block is adjacent to the laser origin
        if self.grid[current_y][current_x] == REFLECT:
            print('reflective adj')
            if (self.grid_faces[current_y][current_x] == 2 and self.grid[current_y][current_x+xdir] == REFLECT) or (self.grid_faces[current_y][current_x] == 1 and self.grid[current_y+ydir][current_x] == REFLECT):
                face_number = self.get_block_face(current_x,current_y)
                # laser.add_to_path([current_x, current_y])
                print('direction before reflecting: '+ str(xdir) + ', ' + str(ydir))
                print('position: '+str(current_x)+', '+str(current_y))
                print('in face type: '+str(face_number))
                laser.reflect(xdir, ydir, face_number)
                print('it got reflected before entering the board')
                # # xdir, ydir = laser.get_direction()
                print('direction after reflecting: '+ str(laser.xdir) + ', ' + str(laser.ydir))
        if self.grid[current_y][current_x] == OPAQUE:
            print('opaque adj')
            if (self.grid_faces[current_y][current_x] == 2 and self.grid[current_y][current_x+xdir] == OPAQUE) or (self.grid_faces[current_y][current_x] == 1 and self.grid[current_y+ydir][current_x] == OPAQUE):
                # print('current position: ' + str(current_x) + ', ' + str(current_y))
                # print('current direction: ' + str(xdir)+ ', ' + str(ydir))
                # print('current face number: '+ str(self.grid_faces[current_y][current_x]))
                face_number = self.get_block_face(current_x,current_y)
                # laser.add_to_path([current_x, current_y])
                laser.absorb(xdir, ydir, face_number)
                # print('it got absorbed before entering board')
        if self.grid[current_y][current_x] == REFRACT:
            print('refract adj')
            if (self.grid_faces[current_y][current_x] == 2 and self.grid[current_y][current_x+xdir] == REFRACT) or (self.grid_faces[current_y][current_x] == 1 and self.grid[current_y+ydir][current_x] == REFRACT):
                face_number = self.get_block_face(current_x,current_y)
                # laser.add_to_path([current_x, current_y])
                print('direction of original laser before refracting: '+str(xdir)+', '+str(ydir))
                laser2 = laser.refract(current_x, current_y, xdir, ydir, face_number)
                print('direction of original laser after refracting: '+str(laser.xdir)+', '+str(laser.ydir))
                print('direction of second beam after refracting: '+str(laser2.xdir)+', '+str(laser2.ydir))


                self.available_lasers.append(laser2)
                print('laser was refracted in the edge block')
                print('current lasers with all trajectories and directions (and if they were shot) are:')
                for i in range(len(self.available_lasers)):
                    print(self.available_lasers[i].get_trajectory())
                    print(self.available_lasers[i].get_direction())
                    print(self.available_lasers[i].was_shot)

        # print('trying to add a '+str(type(current_y))+' and a '+str(type(laser.ydir)))#+' should result in '+str(current_y+laser.ydir))

        next_x = current_x + laser.xdir
        next_y = current_y + laser.ydir
        # if laser.get_trajectory()[-1] != [-2,-2]:
        #     next_x = current_x + laser.xdir
        #     next_y = current_y + laser.ydir

        # if laser.get_trajectory()[-1] == [-2,-2]:
        #     next_x = -2
        #     next_y = -2
        # print('next step is: '+ str(next_x) + ', ' + str(next_y))
        # print('is it within the maze?')
        # print(self.within_bounds(self.grid, next_x, next_y))

        while self.within_bounds(self.grid, next_x, next_y) and laser.get_trajectory()[-1] != [-2,-2]:
            print('while loop in shoot')

            # for i in range(len(self.board)):
            #     print(self.board[i])

            # print("trajectory so far:")
            # print(next_x)

            if self.within_bounds(self.grid, next_x, next_y) == True:

                laser.add_to_path([next_x, next_y])
                print('traj after adding potential next step: '+ str(laser.get_trajectory()))

                if self.grid[current_y][current_x] == REFLECT:
                    print('im touching a reflect block')
                    if (self.grid_faces[current_y][current_x] == 2 and self.grid[current_y][current_x+xdir] == REFLECT) or (self.grid_faces[current_y][current_x] == 1 and self.grid[current_y+ydir][current_x] == REFLECT):
                        # print('current position: ' + str(current_x) + ', ' + str(current_y))
                        # print('current direction: ' + str(xdir)+ ', ' + str(ydir))
                        # print('current face number: '+ str(self.grid_faces[current_y][current_x]))
                        # print('center in this direction: '+ str(self.grid[current_y+ydir][current_x]))
                        # print('reflect is number ' + str(REFLECT))
                        # print('current path before pop: '+ str(laser.path))
                        face_number = self.get_block_face(current_x,current_y)
                        laser.path.pop() #removes the appended next step
                        # laser.add_to_path([current_x, current_y])
                        # print('current path after pop: '+ str(laser.path))
                        # print('2direction before reflecting: '+ str(xdir) + ', ' + str(ydir))
                        laser.reflect(xdir, ydir, face_number)
                        # xdir, ydir = laser.get_direction()
                        # print('2direction after reflecting: '+ str(xdir) + ', ' + str(ydir))
                        print('it was reflected at position: '+str(current_x)+', '+str(current_y))

                        next_x = current_x + laser.xdir
                        next_y = current_y + laser.ydir
                        laser.add_to_path([next_x,next_y])

                if self.grid[current_y][current_x] == OPAQUE:
                    # print('im touching an opaque block')
                    if (self.grid_faces[current_y][current_x] == 2 and self.grid[current_y][current_x+xdir] == OPAQUE) or (self.grid_faces[current_y][current_x] == 1 and self.grid[current_y+ydir][current_x] == OPAQUE):
                        # print('current position: ' + str(current_x) + ', ' + str(current_y))
                        # print('current direction: ' + str(xdir)+ ', ' + str(ydir))
                        # print('current face number: '+ str(self.grid_faces[current_y][current_x]))
                        # print('corresponding center in this direction: '+ str(self.grid[current_y][current_x+xdir]))
                        # print('opaque is number ' + str(OPAQUE))
                        # print('current path so far: '+ str(laser.path))
                        face_number = self.get_block_face(current_x,current_y)
                        laser.path.pop() 
                        # laser.add_to_path([current_x, current_y])
                        laser.absorb(xdir, ydir, face_number)
                        print('it was absorbed at position: '+str(current_x)+', '+str(current_y))

                if self.grid[current_y][current_x] == REFRACT:
                    print('im touching a refractive block')
                    if (self.grid_faces[current_y][current_x] == 2 and self.grid[current_y][current_x+laser.xdir] == REFRACT) or (self.grid_faces[current_y][current_x] == 1 and self.grid[current_y+laser.ydir][current_x] == REFRACT):
                        face_number = self.get_block_face(current_x,current_y)
                        # laser.add_to_path([current_x, current_y])
                        print('2direction of original laser before refracting: '+str(laser.xdir)+', '+str(laser.ydir))
                        print('trajectory of main laser so far: ')
                        print(laser.get_trajectory())
                        initial_for_second = laser.path.pop()
                        print('trajectory after popping: ')
                        print(laser.get_trajectory())
                        laser2 = laser.refract(initial_for_second[0]-laser.xdir, initial_for_second[1]-laser.ydir, laser.xdir, laser.ydir, face_number)
                        print('laser beam was refracted at position '+str(current_x)+', '+str(current_y))
                        print('2direction of original laser after refracting: '+str(laser.xdir)+', '+str(laser.ydir))
                        print('2direction of second beam after refracting: '+str(laser2.xdir)+', '+str(laser2.ydir))
                        self.available_lasers.append(laser2)
                        print('2current lasers with all trajectories (and if they were shot) are:')
                        print(self.available_lasers)
                        next_x = current_x + laser.xdir
                        next_y = current_y + laser.ydir

                        for i in range(len(self.available_lasers)):
                            print(self.available_lasers[i].get_trajectory())
                            print(self.available_lasers[i].get_position())
                            print(self.available_lasers[i].was_shot)



            else: 
                laser.add_to_path([-1, -1])

            print('current: '+str(current_x)+', '+str(current_y))
            print('is being replaced by: '+str(next_x)+', '+str(next_y))

            current_x = next_x
            current_y = next_y
            print('now the current is: '+str(current_x)+', '+str(current_y))
            print('nd the path is: '+str(laser.get_trajectory()))
            next_x = current_x + laser.xdir
            next_y = current_y + laser.ydir
            print('if we follow direction: '+str(laser.xdir)+', '+str(laser.ydir))
            print('the next up is: '+str(next_x)+', '+str(next_y))

        laser.was_shot = True
        laser.path.append([-1,-1])

        # print(laser.path)



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
        Appends a step to the laser beam path and saves the appended list to the self.path variable for the laser.

        **Parameters**
            next_step: *list* 
                list of the x and y coordinates in the next step in the format  [x, y]
        '''
        self.path.append(next_step)

    def get_trajectory(self):
        '''
        Returns the path or paths of that laser as a list of tuples with each position the laser goes through

        **Returns** 

            self.path: *list of tuples*
                list with every position tuple (x,y) that the beam has gone through.
        '''
        return self.path

    def was_shot(self):
        '''
        Returns a boolean representing if the laser was shot
        '''
        return self.was_shot


    def reflect(self, xdir, ydir, face_number):
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
        if face_number == 1:

            new_xdir = xdir
            new_ydir = -ydir

        if face_number == 2:

            new_xdir = -xdir
            new_ydir = ydir

        # print('old dir: '+ str(xdir) +', ' + str(ydir))
        # print('new dir: '+ str(new_xdir)+ ', ' + str(new_ydir))

        self.xdir = new_xdir
        self.ydir = new_ydir

        # print('self dirs: ' + str(self.xdir)+ ', ' + str(self.ydir))

        

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

        

    def refract(self, x, y, xdir, ydir, face_number):
        '''
        Function the describes what happens when a laser beam hits an transparent block: light is refracted AND reflected. The function creates a new pseudo laser object at the point where the refraction occurs to account of the new path being created. The original beam is reflected and a new laser is created with origin at the refraction point and the same direction as teh original laser before refrction.


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
        refracted_laser = Laser(x, y, xdir, ydir) #creates a second laser from the refracting point, that continues the same path as previously.
        # since this refracted laser will have an adjacent refractive block always, add the first two steps to path from the beginning to avoid refracting the beam double.
        refracted_laser.path.append([x+xdir, y+ydir])
        if face_number==1:

            second_xdir = xdir
            second_ydir = - ydir

        if face_number==2:

            second_xdir = - xdir
            second_ydir = ydir

        self.xdir = second_xdir
        self.ydir = second_ydir 
        return refracted_laser



if __name__ == "__main__":
    # solved, winning_board = solve_game("dark_1.bff")
    # solved, winning_board = solve_game("showstopper_4.bff")
    # solved, winning_board = solve_game("mad_4.bff") # yes but slower
    # solved, winning_board = solve_game("numbered_6.bff")


    # solved, winning_board = solve_game("tiny_5.bff")
    solved, winning_board = solve_game("mad_1.bff")

    print('in main')
    for i in range(len(winning_board)):
        print(winning_board[i])
