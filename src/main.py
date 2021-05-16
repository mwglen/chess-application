import curses

def main(stdscr):
    # Clear screen
    stdscr.clear()
    curses.curs_set(0)
    curses.start_color()

    # Do something
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    
    stdscr.bkgd(" ", curses.color_pair(2))
    stdscr.box("|", "-")
    stdscr.addstr(0, 0, "Chess Application", curses.color_pair(1))
    stdscr.getch()

curses.wrapper(main)
