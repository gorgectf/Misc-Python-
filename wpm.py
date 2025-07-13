import curses, time
from curses import wrapper

def start_screen(stdscr):
    stdscr.clear() # Clears the console
    stdscr.addstr("Welcome to WPM Game.")
    stdscr.addstr("\nPress anykey to begin")
    stdscr.refresh() # Refreshes console buffer
    stdscr.getkey() # Waits for input

def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"WPM: {wpm}")

    for i, char in enumerate(current): # Provides the index and value in an array
        correct_char = target[i]
        colour_pair = curses.color_pair(1)

        if correct_char == char:
            colour_pair = curses.color_pair(2)

        stdscr.addstr(0, i, char, colour_pair)

def wpm_test(stdscr):
    target_text = "Hello world this is text test for this app."
    current_text = []
    wpm: float = 0.0

    start_time = time.time()

    while True:
        if len(current_text) == len(target_text):
            break

        time_elapsed = max(time.time() - start_time, 1)

        assert time_elapsed != 0

        wpm = ((len(current_text) / 2) / (time_elapsed / 60)).__round__(1)

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm) # type: ignore
        stdscr.refresh()

        key = stdscr.getkey()
        assert key != None

        # Ordinal value 27 is ESC
        if ord(key) == 27: # Ordinal value, which is the number on the keyboard
            break
        
        # If key is in ARRAY:
        if key in ("KEY_BAKCSPACE", "\b", "\x7f"): # Allowing for handling if backspace is done on different O/S's
            if len(current_text) > 0:
                current_text.pop() # Pops off the last item, like in a stack
        elif len(current_text) < len(target_text):
            current_text.append(key)
        
        #stdscr.clear() # Clears the console
        
        #stdscr.addstr(target_text)
        #stdscr.refresh() # Refreshes console buffer

        #for char in current_text:
            #stdscr.addstr(char, curses.color_pair(1))
        
        stdscr.refresh()
    return wpm

def main(stdscr):
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_MAGENTA) # Sets a colour pair: Foreground, background
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLUE)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_YELLOW)

    #stdscr.clear() # Clears the console
    # stdscr.addstr(0, 0, "Hello world!", curses.color_pair(1)) # Prints text and assigns a colour pair at 0, 0
    #stdscr.refresh() # Refreshes console buffer
    #key = stdscr.getkey() # Waits for input

    start_screen(stdscr)
    wpm = wpm_test(stdscr)

    stdscr.clear()
    stdscr.addstr(f"WPM: {wpm}")
    stdscr.addstr("\nYou completed the app! Press esc to quit.")

    while True:
        key = stdscr.getkey()

        if ord(key) == 27: # Ordinal value, which is the number on the keyboard
            quit()

wrapper(main)
