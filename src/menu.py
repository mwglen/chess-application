from position import Position, InvalidMove
from board import Board
import random
import curses

# Displays the main menu
def display(w):
   
    curr_sel = 0
    
    while True:
        
        # Draw the menu
        _draw(w, curr_sel)

        # Get inputted character
        c = w.getch()

        # Handle linefeeds
        if c == 10:
            # If user selected vs_computer
            if curr_sel == 0:
                info = "0"
                # Create a new board
                b = Board(w)
                b.position = Position.base()
                b.play()

            # If user selected local
            elif curr_sel == 1:
                pass

            # If user selected through_ssh
            elif curr_sel == 2:
                pass
            
            # If user selected exit
            elif curr_sel == 3:
                quit()

            # Handle up arrow key
        elif (c == curses.KEY_UP and curr_sel > 0):
            curr_sel -= 1
        
        # Handle down arrow key
        elif (c == curses.KEY_DOWN and curr_sel < 3):
            curr_sel += 1

def _draw(w, curr_sel):

    # Get the size of the window
    max_y, max_x = w.getmaxyx()

    # Erase the previous drawing
    w.erase()
    
    # Color the main window
    w.bkgd(" ", curses.color_pair(1))
    w.box("|", "-")

    # Add the title to header
    # w.addstr(0, 0, "Chess Application", 
    #         curses.color_pair(1))
  

    # Add the title
    title = [
        r" _____                   _             _   _____ _                    ",
        r"|_   _|                 (_)           | | /  __ \ |                   ",
        r"  | | ___ _ __ _ __ ___  _ _ __   __ _| | | /  \/ |__   ___  ___ ___  ",
        r"  | |/ _ \ '__| '_ ` _ \| | '_ \ / _` | | | |   | '_ \ / _ \/ __/ __| ",
        r"  | |  __/ |  | | | | | | | | | | (_| | | | \__/\ | | |  __/\__ \__ \ ",
        r"  \_/\___|_|  |_| |_| |_|_|_| |_|\__,_|_|  \____/_| |_|\___||___/___/ ",
        r""
    ]
    
    # Used to vertically offset text
    i = -4
    for text in title:
        w.addstr(max_y//2+i, max_x//2 - len(text)//2, text, 
                curses.color_pair(1))
        i += 1

    # Add "VS COMPUTER" button
    text = "VS COMPUTER"
    w.addstr(max_y//2+i, max_x//2 - len(text)//2, text, 
            curses.color_pair(6 if curr_sel == 0 else 1))
    i += 1

    # Add "LOCAL" button
    text = "LOCAL"
    w.addstr(max_y//2+i, max_x//2 - len(text)//2, text, 
            curses.color_pair(6 if curr_sel == 1 else 1))
    i += 1
   
    # Add "THROUGH SSH" button
    text = "THROUGH SSH"
    w.addstr(max_y//2+i, max_x//2 - len(text)//2, text, 
            curses.color_pair(6 if curr_sel == 2 else 1))
    i += 1
    
    # Add "QUIT" button
    text = "QUIT"
    w.addstr(max_y//2+i, max_x//2 - len(text)//2, text, 
            curses.color_pair(6 if curr_sel == 3 else 1))
    i += 1
    
    # Add info box
    w.addstr(max_y - 2, 2, f"Current Selection: {curr_sel}")
