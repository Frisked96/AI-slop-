import curses

class WarningMenu:
    def __init__(self, stdscr):
        self.stdscr = stdscr

    def display(self):
        self.stdscr.clear()
        self.stdscr.addstr(1, 0, "--- WARNING ---")
        self.stdscr.addstr(3, 0, "Please maximize the terminal window (fullscreen) for the best experience.")
        self.stdscr.addstr(4, 0, "Running in a small window may cause the game to crash.")
        self.stdscr.addstr(6, 0, "Press any key to continue...")
        self.stdscr.refresh()
        self.stdscr.getch() # Wait for any key press

