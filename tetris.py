import curses, random, copy, time
from curses import wrapper

WIDTH: int = 15
HEIGHT: int = 20
HALF_H: int= int(HEIGHT // 2)
X_TOP_OFFSET: int = 10
Y_TOP_OFFSET: int = 10

BG_CHARACTER: str = "."
SCREEN: list[list[str]]= [[BG_CHARACTER for x in range(WIDTH)] for y in range(HEIGHT)] # The background screen
BLOCKS: list = list() # Holds [x, y]'s all placed blocks
CURRENT_BLOCK: list[list[int]] = list() # Holds the [x, y]'s of the currently active block
CURRENT_TYPE: str = "I"
HELD_BLOCK: str = ""

SCORE: int = 1
LEVEL: int = 0

COLOUR_PAIRS: dict[str, int] = {}

LOOKUP_OBJ: dict[int, str] = {
    0: "I",
    1: "J",
    2: "L",
    3: "O",
    4: "S",
    5: "T",
    6: "Z",
}

# Pivot point = first value
BLC_TYPE: dict[str, list[list[int]]] = {
    "I": [[0, HALF_H - 2],
          [1, HALF_H - 2],
          [2, HALF_H - 2],
          [3, HALF_H - 2]],
    "J": [[0, HALF_H - 2],
          [1, HALF_H - 2],
          [2, HALF_H - 2],
          [2, HALF_H - 1 - 2]],
    "L": [[0, HALF_H - 2],
          [1, HALF_H - 2],
          [2, HALF_H - 2],
          [2, HALF_H + 1 - 2]],
    "O": [[0, HALF_H - 2],
          [1, HALF_H - 2],
          [0, HALF_H + 1 - 2],
          [1, HALF_H + 1 - 2]],
    "S": [[0, HALF_H - 2],
          [0, HALF_H + 1 - 2],
          [1, HALF_H - 2],
          [1, HALF_H - 1 - 2]],
    "T": [[0, HALF_H - 2],
          [0, HALF_H - 1 - 2],
          [0, HALF_H + 1 - 2],
          [1, HALF_H - 2]],
    "Z": [[0, HALF_H - 2],
          [0, HALF_H - 1 - 2],
          [1, HALF_H - 2],
          [1, HALF_H + 1 - 2]],
}

def save_blocks() -> None:
    global CURRENT_BLOCK, CURRENT_TYPE, BLOCKS, SCORE, LEVEL

    for item in CURRENT_BLOCK:
        current_tuple: list[int] = item
        item = tuple(item)
        BLOCKS.append(item)

    dict_copy: dict[str, list[list[int]]] = copy.deepcopy(BLC_TYPE)
    letter: int = random.randint(0, len(LOOKUP_OBJ) - 1)
    CURRENT_TYPE = LOOKUP_OBJ[letter]
    lookup: str = str(LOOKUP_OBJ[letter])
    CURRENT_BLOCK = dict_copy[lookup]
    SCORE += 10

def clear_row_n() -> None:
    global BLOCKS, SCORE, LEVEL

    BLOCKS.sort()
    i: int = 0

    if len(BLOCKS) > WIDTH:
        while True:
            item: list = BLOCKS[i]
            x: int = item[0]
            y: int = item[1]

            to_compare: list = BLOCKS[i + (WIDTH - 1)]
            x_compare: int = to_compare[0]
            y_compare: int = to_compare[1]

            to_delete = list()
            if x == x_compare:
                if (y + (WIDTH - 1)) == y_compare:
                    for j in range(i, (i + (WIDTH)), 1):
                        to_delete.append(BLOCKS[j])

                    count: int = 0
                    for item in to_delete:
                        while item in BLOCKS:
                            if count == WIDTH * 4:
                                SCORE += 4000

                            BLOCKS.remove(item)
                            SCORE += 100
                            count += 1
                            
                    else:
                        #BLOCKS.sort()
                        LEVEL += 1
            i += 1

            if (i > len(BLOCKS) - 1 or (i + (WIDTH - 1)) > len(BLOCKS) - 1):
                BLOCKS.sort()
                break

def gravity() -> None:
    if len(BLOCKS) > 0:
        for i, block in enumerate(BLOCKS):
            tempx: int = block[0]
            tempy: int = block[1]

            incr_x: int = tempx + 1

            while incr_x < HEIGHT:
                new = tuple((incr_x, tempy))

                if new not in BLOCKS:
                    BLOCKS[i] = new

                    incr_x += 1
                else:
                    break
            else:
                BLOCKS.sort()
                return
                

def input_fetcher(key: int) -> int: 
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
        case _:
            return 0
        
def shift_into_screen(left: bool) -> None: # LR = True = Shift all positions left. False = shift all positions right
    shift: int = 0
    y_positions = list()
    expression: str = ">"

    for block in CURRENT_BLOCK:
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
        shift -= WIDTH - 1

    for i, tupl in enumerate(CURRENT_BLOCK):
        tupl = CURRENT_BLOCK[i]
        tuple_y = tupl[1]

        if left:
            tuple_y += shift
        else:
            tuple_y -= shift

        new = tuple((tupl[0], tuple_y))
        CURRENT_BLOCK[i] = new # type: ignore

def rotate() -> None:
    global CURRENT_BLOCK

    pivot_coords: list[int] = CURRENT_BLOCK[0]
    pivot_x: int = pivot_coords[0]
    pivot_y: int = pivot_coords[1]

    for i, block in enumerate(CURRENT_BLOCK):
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
        CURRENT_BLOCK[i] = final # type: ignore
    else:
        for p, brack in enumerate(CURRENT_BLOCK):
            temp: list[int] = brack
            y: int = temp[1]

            if y < 0:
                shift_into_screen(True)
                return

            if y > WIDTH - 1:
                shift_into_screen(False)
                return
        else:
            return

def update(stdscr, movement: int, fast_fall: int = 0) -> None:  # Return True if should be deleted
    global SCORE, DROP_WAIT, LEVEL, BLOCKS, CURRENT_BLOCK, HELD_BLOCK, CURRENT_TYPE, WIDTH, HEIGHT
    #stdscr.addstr(5, 30 , str(CURRENT_BLOCK))
    #stdscr.addstr(0, 30 , str(BLC_TYPE["I"]))
    #stdscr.addstr(3, 30 , str(BLOCKS))

    if movement == 2:
        rotate()
        movement = 0
        fast_fall = -1

    if movement == 3:
        fast_fall = 1
        movement = 0

    if movement == 5:
        movement = -2
    
    if movement == 6:
        movement = 2

    if movement == 4:
        dict_pos_copy = copy.deepcopy(BLC_TYPE)
        
        if HELD_BLOCK == "":
            CURRENT_BLOCK = list()
            HELD_BLOCK = CURRENT_TYPE
            save_blocks()
            return
        else:
            current_copy = CURRENT_TYPE
            CURRENT_TYPE = HELD_BLOCK
            HELD_BLOCK = current_copy
            CURRENT_BLOCK = dict_pos_copy[CURRENT_TYPE]
            return

    tuples: list[tuple[int, ...]] = [tuple(x) for x in CURRENT_BLOCK]

    # Game Over
    if all(elem in BLOCKS for elem in tuples):
        for x in range(HEIGHT):
            for y in range(WIDTH):
                stdscr.addstr(x, y, " ")
            
        stdscr.nodelay(False)
        stdscr.addstr(HEIGHT//2, WIDTH//2, "Game Over!")
        stdscr.addstr(HEIGHT//2 + 10, WIDTH//2, f"Score: {SCORE}")
        stdscr.addstr(HEIGHT//2 + 20, WIDTH//2, f"Level: {LEVEL}")
        stdscr.getch()
        stdscr.timeout(1000)
        time.sleep(5)
        quit()
                
    for array in CURRENT_BLOCK:
        arrayx: int = array[0] # UD
        arrayy: int = array[1] # LR

        if tuple((arrayx + 1, arrayy)) in BLOCKS:
            save_blocks()
            return
    
        if (arrayx + 1 >= HEIGHT):
            save_blocks()
            return
                
        if arrayx == HEIGHT:
            save_blocks()
            return
        
        if tuple((arrayx, arrayy + movement)) in BLOCKS:
            movement = 0

        if (0<= (arrayy + movement) <= WIDTH - 1) == False:
            movement = 0

        if tuple((arrayx, (0 <= (arrayy + movement) <= WIDTH - 1))) == False:
            movement = 0
                
    for i, item in enumerate(CURRENT_BLOCK):
        temp: list[int] = copy.deepcopy(item)
        x: int = temp[0] # UD
        y: int = temp[1] # LR
        new_pos = list()

        if (x + 1 >= HEIGHT) and movement == 0:
            save_blocks()
            return
                
        if x >= HEIGHT and movement == 0:
            save_blocks()
            return
        
        if (x + (1 + fast_fall)) >= HEIGHT:
            fast_fall = -1

        fast_fall_pos = tuple(((x + (1 + fast_fall)), y))

        if  fast_fall_pos in BLOCKS:
            fast_fall = -1
                    
        x += 1 + fast_fall

        if (0<= (y + movement) <= WIDTH - 1) == False:
            movement = 0
        
        y += movement

        new_pos: list = [x, y]
        blocks_tuples = tuple(new_pos)

        if blocks_tuples in BLOCKS:
            save_blocks()
            return

        CURRENT_BLOCK[i] = new_pos
    return

def render(stdscr) -> None:
    global SCORE, WIDTH, HEIGHT

    try:
        stdscr.addstr(0, 0, f"Score: {SCORE}")
        stdscr.addstr(10, 0, f"Level: {LEVEL}")
        stdscr.addstr(20, 0, f"Held Block: {HELD_BLOCK}")

        for x in range(HEIGHT):
            for y in range(WIDTH):
                x_pos: int = (x * 2) + X_TOP_OFFSET
                y_pos: int = (y * 2) + Y_TOP_OFFSET

                stdscr.addstr(x_pos, y_pos, SCREEN[x][y])

        for upper in CURRENT_BLOCK:
            block_x: int = (upper[0] * 2) + X_TOP_OFFSET
            block_y: int = (upper[1] * 2) + Y_TOP_OFFSET

            stdscr.addstr(block_x, block_y, "O", COLOUR_PAIRS[CURRENT_TYPE])

        for lower in BLOCKS:
            cblock_x: int = (lower[0] * 2) + X_TOP_OFFSET
            cblock_y: int = (lower[1] * 2) + Y_TOP_OFFSET

            stdscr.addstr(cblock_x, cblock_y, "#", curses.color_pair(8))
    except ValueError as e:
        stdscr.addstr(0, 0, f"Render error: {e}.")
        return
    except curses.error as f:
        stdscr.addstr(0, 0, f"Curses error: {f}. Restart and resize screen.")
        return

def init_colours() -> None:
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

def display_intro_text(stdscr) -> None:
    stdscr.addstr(0, 0, r"""
        _______ _______ _______ _______ _______ _______ 
        |\     /|\     /|\     /|\     /|\     /|\     /|
        | +---+ | +---+ | +---+ | +---+ | +---+ | +---+ |
        | |T  | | |E  | | |T  | | |R  | | |I  | | |S  | |
        | +---+ | +---+ | +---+ | +---+ | +---+ | +---+ |
        |/_____\|/_____\|/_____\|/_____\|/_____\|/_____\|
        """)

    stdscr.addstr(6, 10, "v1.0.1")
    stdscr.addstr(8, 10, "It is recommended to go fullscreen to avoid errors. Minimum dimension: 800x850 px")
    stdscr.addstr(10, 10, "Controls: A - Left, D - Right, W - Rotate, R - Hold, ESC - Quit, Z - Move 2 spaces left, X - Move 2 spaces right")
    stdscr.addstr(12, 10, "It will say 'curses() ERR' if your screen is not large enough. Restart if this happens.")
    stdscr.addstr(14, 10, "Press any key, or resize the terminal, to begin.")

    stdscr.addstr(18, 10, "Known issues:")
    stdscr.addstr(20, 10, "1. Blocks that rotate on the right edge of the screen when theres a lot of placed blocks get a part of them removed for some reason.")
    stdscr.getch()

def level_up(base_wait: int) -> int:
    division: int = (LEVEL // 8).__trunc__()
    base_wait /= max(1, division) # type: ignore

    if base_wait < 100: 
        base_wait = 100

    return int(base_wait)

def main(stdscr) -> None:
    global CURRENT_BLOCK, CURRENT_TYPE, X_TOP_OFFSET, Y_TOP_OFFSET

    display_intro_text(stdscr)
    curses.start_color()
    init_colours()    

    terminal_h: int; terminal_w: int
    terminal_h, terminal_w = stdscr.getmaxyx()

    Y_TOP_OFFSET = (terminal_w // 2) - WIDTH
    X_TOP_OFFSET = (terminal_h // 2) - HEIGHT

    stdscr.nodelay(True)

    dict_copy = copy.deepcopy(BLC_TYPE)
    letter: int = random.randint(0, len(LOOKUP_OBJ) - 1)
    CURRENT_TYPE = LOOKUP_OBJ[letter]
    CURRENT_BLOCK = dict_copy[LOOKUP_OBJ[letter]]
    del dict_copy
    
    base_wait: int = 240

    while True:
        key = stdscr.getch()
        ordkey = input_fetcher(key)

        base_wait = level_up(base_wait)
        stdscr.timeout(base_wait)

        stdscr.clear()
        update(stdscr, ordkey)
        gravity()
        clear_row_n()
        render(stdscr)

if __name__ == "__main__":
    wrapper(main)

