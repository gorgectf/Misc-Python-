import curses, random, copy, time, sys
from curses import wrapper

SCREEN: list = []
BLOCK_TYPE: dict[str, list] = {}
COLOUR_PAIRS: dict = {}

LOOKUP_OBJ: dict[int, str] = {
    0: "I",
    1: "J",
    2: "L",
    3: "O",
    4: "S",
    5: "T",
    6: "Z",
}

class GameState:
    """Game state manager handling score, level, block positions, and gameplay mechanics."""
    score: int = 0
    level: int = 0
    current_block = list()
    current_type: str = "I"
    held_block: str = ""
    blocks = list()

    def __init__(self, width: int, height: int, terminal_h: int, terminal_w: int, bg_character: str) -> None:
        """ Initializes screen using width, height parameter. \n 
        Sets screen x and y offset and declares block type dict."""
        global SCREEN, BLOCK_TYPE
        self.width = width
        self.height = height
        self.x_offset = (terminal_h // 2) - height
        self.y_offset = (terminal_w // 2) - width
        self.half_h = self.height // 2

        SCREEN = [[bg_character for x in range(self.width)] for y in range(self.height)]

        BLOCK_TYPE = {
            "I": [[0, self.half_h - 2],
                [1, self.half_h - 2],
                [2, self.half_h - 2],
                [3, self.half_h - 2]],
            "J": [[0, self.half_h - 2],
                [1, self.half_h - 2],
                [2, self.half_h - 2],
                [2, self.half_h - 1 - 2]],
            "L": [[0, self.half_h - 2],
                [1, self.half_h - 2],
                [2, self.half_h - 2],
                [2, self.half_h + 1 - 2]],
            "O": [[0, self.half_h - 2],
                [1, self.half_h - 2],
                [0, self.half_h + 1 - 2],
                [1, self.half_h + 1 - 2]],
            "S": [[0, self.half_h - 2],
                [0, self.half_h + 1 - 2],
                [1, self.half_h - 2],
                [1, self.half_h - 1 - 2]],
            "T": [[0, self.half_h - 2],
                [0, self.half_h - 1 - 2],
                [0, self.half_h + 1 - 2],
                [1, self.half_h - 2]],
            "Z": [[0, self.half_h - 2],
                [0, self.half_h - 1 - 2],
                [1, self.half_h - 2],
                [1, self.half_h + 1 - 2]],
        }

    def level_up(self, base_wait: int) -> int:
        """ Decreases the waiting time to accept input in the main loop. \n
            new_level = current_level / 8 \n
            new_level = new_level.__trunc__() \n
            base_wait = max(1, new_level) \n
        """
        division: int = (GameState.level // 8).__trunc__()
        base_wait /= max(1, division) # type: ignore
    

        if base_wait < 100: 
            base_wait = 100

        return int(base_wait)

    def next_block(self) -> None:
        """ Gets the next block by using a random number from 0 to 7 and looking at the LOOKUP_OBJ for the type. """
        global BLOCK_TYPE

        dict_copy: dict = copy.deepcopy(BLOCK_TYPE)
        letter: int = random.randint(0, len(LOOKUP_OBJ) - 1)
        GameState.current_type = LOOKUP_OBJ[letter]
        lookup = str(LOOKUP_OBJ[letter])
        GameState.current_block = dict_copy[lookup]

    def save_blocks(self) -> None:
        """ Loops through the positions of the current block and adds them to the total blocks, then sorts the total blocks."""
        for item in GameState.current_block:
            current_tuple: list[int] = item
            item = tuple(item)
            GameState.blocks.append(item)

        self.next_block()

    def shift_blocks(self, left) -> None:
        """ Shift blocks left or right if they will be out of bounds in the next iteration. """
        shift: int = 0
        y_positions = list()
        expression: str = ">"

        for block in GameState.current_block:
            y: int = block[1]
            y_positions.append(y)

        if left:
            expression = "<"

        for pos in y_positions:
            if eval(f"{pos} {expression} {shift}"):
                shift = pos

        if left:
            shift = abs(shift) + 1
        else:
            shift -= self.width - 1

        for i, block in enumerate(GameState.current_block):
            block = GameState.current_block[i]
            tuple_y = block[1]

            if left:
                tuple_y += shift
            else:
                tuple_y -= shift

            new = tuple((block[0], tuple_y))
            GameState.current_block[i] = new # type: ignore

    def apply_gravity(self) -> None:
        """ Puts all blocks down until it hits another block or the floor. """
        if len(GameState.blocks) > 0:
            for i, block in enumerate(GameState.blocks):
                tempx: int = block[0]
                tempy: int = block[1]

                incr_x: int = tempx + 1

                while incr_x < self.height:
                    new = tuple((incr_x, tempy))

                    if new not in GameState.blocks:
                        GameState.blocks[i] = new

                        incr_x += 1
                    else:
                        break
                else:
                    GameState.blocks.sort()
                    return

    # Note: inefficient
    def clear_rows(self) -> None:
        """ Process: \n
            1. Sort all blocks, \n
            2. If the current coordinates x is equal to the coordinate at n + widths position, check if the y at n + width is equal to y + width - 1 \n
            3. If step 2 is true, then that must mean a row has been filled out. Otherwise, go back to step 2 and increment n. \n
            4. Delete from the current n to n + width - 1, deleting a row.
        """
        GameState.blocks.sort()
        i: int = 0

        if len(GameState.blocks) > self.width:
            while True:
                item: list = GameState.blocks[i]
                x: int = item[0]
                y: int = item[1]

                to_compare: list = GameState.blocks[i + (self.width - 1)]
                x_compare: int = to_compare[0]
                y_compare: int = to_compare[1]

                to_delete = list()
                if x == x_compare:
                    if (y + (self.width - 1)) == y_compare:
                        for j in range(i, (i + (self.width)), 1):
                            to_delete.append(GameState.blocks[j])

                        count: int = 0
                        for item in to_delete:
                            while item in GameState.blocks:
                                if count >= self.width * 4:
                                    GameState.score += 4000
    
                                GameState.blocks.remove(item)
                                GameState.score += 100
                                count += 1                    
                        else:
                            GameState.level += 1
                i += 1

                if (i > len(GameState.blocks) - 1 or (i + (self.width - 1)) > len(GameState.blocks) - 1):
                    break

    def update_gamestate(self) -> None:
        """ Applies gravity and clears any possible rows """
        self.apply_gravity()
        self.clear_rows()

def init_colours() -> None:
    """ Initializes colour pairs and adds them to the COLOUR_PAIRS dictionairy."""
    global COLOUR_PAIRS

    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_WHITE)     # I
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_WHITE)     # J
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_WHITE)   # L (approximation for orange)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_WHITE)   # O
    curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_WHITE)    # S
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_WHITE)  # T
    curses.init_pair(7, curses.COLOR_RED, curses.COLOR_WHITE)      # Z
    curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_WHITE) # Placed blocks
    
    COLOUR_PAIRS = {
            'I': curses.color_pair(1),
            'J': curses.color_pair(2),
            'L': curses.color_pair(3),
            'O': curses.color_pair(4),
            'S': curses.color_pair(5),
            'T': curses.color_pair(6),
            'Z': curses.color_pair(7)
    }   

def input_fetcher(key: int) -> int:
    """ Checks the ordinal value of the key parameter and returns a magic number based on viable inputs. """
    match key:
        case 27: # ESC
            quit()
        case 97 | 65: # a, A - Move left
            return -1
        case 100 | 68: # d, D - Move right
            return 1
        case 119| 87: # w, W -Rotate
            return 2
        case 115 | 83: # s, S - Fast fall
            return 3
        case 114 | 82: # r, R - Hold block
            return 4
        case 122 | 90: # Double move left
            return 5
        case 120 | 88: # Double move right
            return 6
        case _: # Case else
            return 0

def rotate(game_obj: GameState) -> None:
    """ Rotates the current block. """
    pivot_coords: list[int] = GameState.current_block[0]
    pivot_x: int = pivot_coords[0]
    pivot_y: int = pivot_coords[1]

    for i, block in enumerate(GameState.current_block):
        temp: list[int] = block
        x: int = temp[0]
        y: int = temp[1]

        x_prime: int = x - pivot_x
        y_prime: int = y - pivot_y

        x_rot: int = -y_prime
        y_rot: int = x_prime

        x_new: int = x_rot + pivot_x # UD
        y_new: int = y_rot + pivot_y # LR

        final = tuple((x_new, y_new))
        GameState.current_block[i] = final # type: ignore
    else:
        for p, brock in enumerate(GameState.current_block):
            temp: list[int] = brock
            y: int = temp[1]

            if y < 0:
                game_obj.shift_blocks(True)
                return

            if y > game_obj.width - 1:
                game_obj.shift_blocks(False)
                return

def game_over(stdscr, game_obj: GameState) -> None:
    """ Due to how I built the system, game over is only triggered if any block has its origin coordinates, meaning it couldnt move when placed, so it must be game over if that happens."""
    tupled_current_block = [tuple(x) for x in GameState.current_block]

    if all(elem in GameState.blocks for elem in tupled_current_block):
        for x in range(game_obj.height):
            for y in range(game_obj.width):
                stdscr.addstr(x, y, " ")
            
        stdscr.nodelay(False)
        stdscr.addstr(game_obj.height//2, game_obj.width//2, "Game Over!")
        stdscr.addstr(game_obj.height//2 + 10, game_obj.width//2, f"Score: {GameState.score}")
        stdscr.addstr(game_obj.height//2 + 20, game_obj.width//2, f"Level: {GameState.level}")
        stdscr.getch()
        stdscr.timeout(1000)
        time.sleep(5)
        quit()
    return

def update(stdscr, movement: int, game_obj: GameState, fast_fall: int = 0):
    """ Updates the block based on movement, checks if the game over condition is met, and checks if the boundaries are being touched currently and with any movement. """
    match movement:
        case 2:
            rotate(game_obj)
            movement = 0
            fast_fall = -1
        case 3:
            fast_fall = 1
            movement = 0
        case 5:
            movement = -2
        case 6:
            movement = 2
        case 4:
            dict_pos_copy = copy.deepcopy(BLOCK_TYPE)
            
            if GameState.held_block == "":
                GameState.current_block = list()
                GameState.held_block = GameState.current_type
                game_obj.save_blocks()
                return
            else:
                current_copy = GameState.current_type
                GameState.current_type = GameState.held_block
                GameState.held_block = current_copy
                GameState.current_block = dict_pos_copy[GameState.current_type]
            return

    game_over(stdscr, game_obj)

    for array in GameState.current_block:
        arrayx: int = array[0] # UD
        arrayy: int = array[1] # LR

        if tuple((arrayx + 1, arrayy)) in GameState.blocks:
            game_obj.save_blocks()
            return
    
        if (arrayx + 1 >= game_obj.height):
            game_obj.save_blocks()
            return
                
        if arrayx == game_obj.height:
            game_obj.save_blocks()
            return
        
        if tuple((arrayx, arrayy + movement)) in GameState.blocks:
            movement = 0

        if (0<= (arrayy + movement) <= game_obj.width - 1) == False:
            movement = 0

        if tuple((arrayx, (0 <= (arrayy + movement) <= game_obj.width - 1))) == False:
            movement = 0

    for i, item in enumerate(GameState.current_block):
        temp: list[int] = copy.deepcopy(item)
        x: int = temp[0] # UD
        y: int = temp[1] # LR
        new_pos = list()

        if (x + 1 >= game_obj.height) and movement == 0:
            game_obj.save_blocks()
            return
                
        if x >= game_obj.height and movement == 0:
            game_obj.save_blocks()
            return
        
        if (x + (1 + fast_fall)) >= game_obj.height:
            fast_fall = -1

        fast_fall_pos = tuple(((x + (1 + fast_fall)), y))

        if  fast_fall_pos in GameState.blocks:
            fast_fall = -1
                    
        x += 1 + fast_fall

        if (0<= (y + movement) <= game_obj.width - 1) == False:
            movement = 0
        
        y += movement

        new_pos: list = [x, y]
        blocks_tuples = tuple(new_pos)

        if blocks_tuples in GameState.blocks:
            game_obj.save_blocks()
            return

        GameState.current_block[i] = new_pos

def render(stdscr, game_obj: GameState):
    """ Renders the screen, score, level, and current held block type. """
    try:
        global SCREEN
        stdscr.addstr(0, 0, f"Score: {GameState.score}")
        stdscr.addstr(10, 0, f"Level: {GameState.level}")
        stdscr.addstr(20, 0, f"Held Block: {GameState.held_block}")

        for x in range(game_obj.height):
            for y in range(game_obj.width):
                x_pos: int = (x * 2) + game_obj.x_offset
                y_pos: int = (y * 2) + game_obj.y_offset

                stdscr.addstr(x_pos, y_pos, SCREEN[x][y])

        for upper in GameState.current_block:
            block_x: int = (upper[0] * 2) + game_obj.x_offset 
            block_y: int = (upper[1] * 2) + game_obj.y_offset

            stdscr.addstr(block_x, block_y, "O", COLOUR_PAIRS[GameState.current_type])

        for lower in GameState.blocks:
            cblock_x: int = (lower[0] * 2) + game_obj.x_offset
            cblock_y: int = (lower[1] * 2) + game_obj.y_offset

            stdscr.addstr(cblock_x, cblock_y, "#", curses.color_pair(8))
    except ValueError as e:
        stdscr.addstr(0, 0, f"Render error: {e}.")
        return
    except curses.error as f:
        stdscr.addstr(0, 0, f"Curses error: {f}. Restart and resize screen.")
        return

def display_intro_text(stdscr) -> None:
    """ Displays the intro text: Tetris, version, general info, controls, and known issues. """
    stdscr.addstr(0, 0, r"""
        _______ _______ _______ _______ _______ _______ 
        |\     /|\     /|\     /|\     /|\     /|\     /|
        | +---+ | +---+ | +---+ | +---+ | +---+ | +---+ |
        | |T  | | |E  | | |T  | | |R  | | |I  | | |S  | |
        | +---+ | +---+ | +---+ | +---+ | +---+ | +---+ |
        |/_____\|/_____\|/_____\|/_____\|/_____\|/_____\|
        """)

    stdscr.addstr(6, 10, "v1.0.2")
    stdscr.addstr(8, 10, "It is recommended to go fullscreen to avoid errors. Minimum dimension: 800x850 px")
    stdscr.addstr(10, 10, "Controls: A - Left, D - Right, W - Rotate, R - Hold, ESC - Quit, Z - Move 2 spaces left, X - Move 2 spaces right")
    stdscr.addstr(12, 10, "It will say 'curses() ERR' if your screen is not large enough. Restart if this happens.")
    stdscr.addstr(14, 10, "Press any key, or resize the terminal, to begin.")

    stdscr.addstr(18, 10, "Known issues:")
    stdscr.addstr(20, 10, "1. Blocks that rotate on the right edge of the screen when theres a lot of placed blocks get a part of them removed for some reason.")
    stdscr.getch()

def validate_dimensions(term_h: int, term_w: int):
    """ Fetches the width and height from the arguments, validates, and returns them if all checks are passed. """
    args: list[str] = sys.argv
    width = ""
    height = ""

    if len(args) == 3:
        width, height = args[1:]
    
    if width.isdigit() and height.isdigit():
        width = int(width)
        height = int(height)

        wrong: int = 0

        if width < term_h:
            wrong += 1

        if height < term_w:
            wrong += 1

        if width < 15:
            wrong += 1

        if height < 20:
            wrong += 1

        if wrong == 0:
            return width, height
    return 15, 20

def main(stdscr):
    terminal_h: int; terminal_w: int
    terminal_h, terminal_w = stdscr.getmaxyx()

    width, height = validate_dimensions(term_h=terminal_h, term_w=terminal_w)

    game_state = GameState(width=width, height=height, terminal_h=terminal_h, terminal_w=terminal_w,bg_character=".")

    init_colours()
    display_intro_text(stdscr)

    stdscr.nodelay(True)

    game_state.next_block()

    base_wait: int = 240

    while True:
        key = stdscr.getch()
        ordkey: int = input_fetcher(key)

        base_wait: int = game_state.level_up(base_wait)
        stdscr.timeout(base_wait)

        stdscr.clear()
        update(stdscr, ordkey, game_state)
        game_state.update_gamestate()
        render(stdscr, game_state)

if __name__ == "__main__":
    wrapper(main)
