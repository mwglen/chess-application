def start(w):

def _create_subwindow(w):
    # Get maximum allowed x and y values
    max_y, max_x = w.getmaxyx()

    # Create a subwindow in the center of the screen
    height = max_y//3
    width = max_x//3
    x = max_x//2 - width//2
    y = max_y//2 - max_y//2
    sw = curses.newwin(height, width, y, x)

def _draw(w):
    # Color the sub window
    sw.bkgd(" ", curses.color_pair(1))
    sw.box("|", "-")

    # Get maximum allowed x and y values
    max_y, max_x = sw.getmaxyx()
    
    text = "Choose Colors"
    w.addstr(2, max_x//2 - len(text)//2,
        text, curses.color_pair(1))
    
    text = "Black: " + black
    w.addstr(2, max_x//2 - len(text)//2,
        text, curses.color_pair(1))
    
    text = "White: " + white
    sw.addstr(3, max_x//2 - len(text)//2,
        text, curses.color_pair(1))
    
    text = "Swap Colors"
    sw.addstr(4, max_x//2 - len(text)//2,
        text, curses.color_pair(1))
    
    text = "Randomize"
    sw.addstr(4, max_x//2 - len(text)//2,
        text, curses.color_pair(1))

    text = "Continue"
    sw.addstr(4, max_x//2 - len(text)//2,
        text, curses.color_pair(1))
    
    text = "Return to Name Selection"
    sw.addstr(4, max_x//2 - len(text)//2,
        text, curses.color_pair(1))
    
    black = random.shuffle(["Player", "Computer"])
