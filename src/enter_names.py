from constants import *
from menu_functions import edit_text
import curses

# Displays the main menu
def start(w, gm) -> (str, str):
    curr_sel = 0
    player1 = ""
    player2 = ""
    sw = _create_window(w)
    
    while True:
        
        # Draw the menu
        _draw(sw, gm, curr_sel, player1, player2)
        
        # Get inputted character
        c = sw.getch()
        
        # Handle linefeeds
        if c == 10:
            
            # If user selected to edit the name of Player 1
            if curr_sel == 0:
                while (c := sw.getch()) != 10:
                    if c == curses.ascii.DEL:
                        player1 = player1[:-1]
                    elif curses.ascii.isascii(chr(c)):
                        if len(player1) < 7: player1 += chr(c)
                    _draw(sw, gm, curr_sel, player1, player2)
            
            # If user selected to edit the name of Player 2
            elif curr_sel == 1:
                while (c := sw.getch()) != 10:
                    if c == curses.ascii.DEL:
                        player2 = player2[:-1]
                    elif curses.ascii.isascii(chr(c)):
                        if len(player2) < 7: player2 += chr(c)
                    _draw(sw, gm, curr_sel, player1, player2)
            
            # If user selected to Continue to Color Selection
            elif curr_sel == 2: return (player1, player2)
            
            # If user selected to return to the Main Menu
            elif curr_sel == 3: return quit()

        # Handle up arrow key
        elif (c == curses.KEY_UP and curr_sel > 0):
            curr_sel -= 1
        
        # Handle down arrow key
        elif (c == curses.KEY_DOWN and curr_sel < 3):
            curr_sel += 1


def _create_window(w):
    # Get maximum allowed x and y values
    max_y, max_x = w.getmaxyx()

    # Create a new window
    height = 10
    width = 25
    x = max_x//2 - width//2
    y = max_y//2 - height//2
    sw = curses.newwin(height, width, y, x)

    # Fix io
    sw.keypad(True)

    # Return the window
    return sw

def _draw(sw, gm, curr_sel, player1, player2):
    
    # Erase the previous drawing
    sw.erase()

    # Color the sub window
    sw.bkgd(" ", curses.color_pair(SM))
    sw.box("|", "-")

    # Get maximum allowed x and y values
    max_y, max_x = sw.getmaxyx()
    
    # Add Prompt for Player 1
    text = "Enter Names"
    sw.addstr(1, max_x//2 - len(text)//2,
        text, curses.color_pair(SM))
    
    # Add Prompt for Player 1
    prompt = "Player: " if gm == VS_COMPUTER else "Player 1: "
    text = prompt + player1
    sw.addstr(3, 1, text,
        curses.color_pair(SM2 if curr_sel == 0 else SM))
    
    # Add Prompt for Player 2
    prompt = "Computer: " if gm == VS_COMPUTER else "Player 2: "
    text = prompt + player2
    sw.addstr(5, 1, text,
        curses.color_pair(SM2 if curr_sel == 1 else SM))

    # Add Prompt to Continue
    text = "Continue"
    sw.addstr(7, max_x//2 - len(text)//2, text,
        curses.color_pair(SM2 if curr_sel == 2 else SM))
    
    # Add Prompt to Return
    text = "Return to Main Menu"
    sw.addstr(8, max_x//2 - len(text)//2, text,
        curses.color_pair(SM2 if curr_sel == 3 else SM))
