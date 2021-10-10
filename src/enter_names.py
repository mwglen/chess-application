from constants import *
from menu_functions import edit_text, create_subwindow
import curses

# Displays the main menu
def start(w, gm) -> (str, str):
    curr_sel = 0
    player1 = ""
    player2 = ""
    sw = create_subwindow(w, 10, 25)
    
    while True:
        # Draw the menu
        _draw(sw, gm, curr_sel, player1, player2)
        
        # Get inputted character
        c = sw.getch()
        
        # Handle linefeeds
        if c == 10:
            # If user selected to Continue to Color Selection
            if curr_sel == 2: 
                del sw; w.touchwin()
                return (player1, player2)
            
            # If user selected to return to the Main Menu
            elif curr_sel == 3: 
                del sw; w.touchwin()
                raise ReturnToMainMenu

        # Handle up tabs and arrow keys
        elif (c == curses.KEY_UP and curr_sel > 0): curr_sel -= 1
        elif (c == ord('k') and curr_sel > 0): curr_sel -= 1
        elif (c == curses.KEY_DOWN and curr_sel < 3): curr_sel += 1
        elif (c == ord('j') and curr_sel < 3): curr_sel += 1
        elif c == ord('\t'): curr_sel = (curr_sel + 1) % 4
        
        # Handle backspaces
        elif c == curses.ascii.DEL:
            if (curr_sel == 0): player1 = player1[:-1]
            if (curr_sel == 1): player2 = player2[:-1]

        # Handle ascii characters
        elif curses.ascii.isascii(chr(c)):
            if (curr_sel == 0) and (len(player1) < 11):
                player1 += chr(c)
            if (curr_sel == 1) and (len(player2) < 11):
                player2 += chr(c)

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
    sw.addstr(3, 2, text,
        curses.color_pair(SM2 if curr_sel == 0 else SM))
    
    # Add Prompt for Player 2
    prompt = "Computer: " if gm == VS_COMPUTER else "Player 2: "
    text = prompt + player2
    sw.addstr(5, 2, text,
        curses.color_pair(SM2 if curr_sel == 1 else SM))

    # Add Prompt to Continue
    text = "Continue"
    sw.addstr(7, max_x//2 - len(text)//2, text,
        curses.color_pair(SM2 if curr_sel == 2 else SM))
    
    # Add Prompt to Return
    text = "Return to Main Menu"
    sw.addstr(8, max_x//2 - len(text)//2, text,
        curses.color_pair(SM2 if curr_sel == 3 else SM))
