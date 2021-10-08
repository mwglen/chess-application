import curses
# Edits text, return true if key pressed was a linefeed
def edit_text(w, text, max_size) -> (str, bool):
    c = w.getch()
    if c == curses.ascii.DEL: text = text[:-1]
    elif curses.ascii.isascii(chr(c)):
        if len(text) < max_size: text += chr(c)
    return (text, (c == 10))

