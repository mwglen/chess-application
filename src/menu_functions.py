import curses

# Edits text, return true if key pressed was a linefeed
def edit_text(w, text, max_size) -> (str, bool):
    c = w.getch()
    if c == curses.ascii.DEL: text = text[:-1]
    elif curses.ascii.isascii(chr(c)) and c != 10:
        if len(text) < max_size: text += chr(c)
    return (text, c == 10)

# Creates a window in the center of the screen.
def create_subwindow(w, height, width):
    # Get maximum allowed x and y values
    max_y, max_x = w.getmaxyx()

    # Create a new window
    x = max_x//2 - width//2
    y = max_y//2 - height//2
    sw = curses.newwin(height, width, y, x)

    # Fix io
    sw.keypad(True)

    # Return the window
    return sw
