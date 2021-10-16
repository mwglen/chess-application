import curses
from menu_functions import create_subwindow
from constants import *

def display(w):
    max_y, max_x = w.getmaxyx(); curr_sel = 0;
    sw = create_subwindow(w, max_y - max_y//5, max_x - max_x//5)
    max_y, max_x = sw.getmaxyx();
    
    # Split the instructions into chunks that are able
    # to be displayed regardless of terminal size
    chunks = [];
    for text in TEXT:
        words = text.split(); chunk = "";
        if (not words): chunks.append("");
        while (words):
            if (len(chunk) + len(words[0]) + 1 < max_x - 2):
                if len(chunk) != 0: chunk += " ";
                chunk += words.pop(0);
                if (not words): chunks.append(chunk); chunk = "";
            else: chunks.append(chunk); chunk = "";
   
    while True: 
        _draw(sw, curr_sel, chunks)
        max_curr_sel = max(len(chunks) - max_y + 2, 0)
        c = sw.getch()
        if (c == 10 or c == curses.ascii.ESC): break
        elif (c == curses.KEY_UP and curr_sel > 0): 
            curr_sel -= 1
        elif (c == curses.KEY_DOWN and curr_sel < max_curr_sel):
            curr_sel += 1

def _draw(sw, curr_sel, chunks):
    # Erase the previous drawing
    sw.erase()

    # Color the sub window
    sw.bkgd(" ", curses.color_pair(SM))
    sw.box("|", "-")
    
    # Get maximum allowed x and y values
    max_y, max_x = sw.getmaxyx()
                
    # Print the submenu title
    sw.addstr(0, 1, "INSTRUCTIONS", curses.color_pair(SM))
    
    # Print the chunks
    i = 1;
    for chunk in chunks[curr_sel:len(chunks)]:
        sw.addstr(i, 1, chunk, curses.color_pair(SM)); i += 1;
        if (i > max_y - 2): break

TEXT = [
    "Gamemodes:",
    "In this application, there are two gamemodes. And both are available on the main menu screen.",
    "    \"VS COMPUTER\" starts a game against a chess AI",
    "    \"LOCAL GAME\" starts a game in which two people can play against eachother on the same device",
    "",
    "Navigating menus:",
    "The arrow keys and tab can be used to navigate menus while using this application. The enter key can be used to select an option from the menu. The escape key can be used to return to the main menu, and the backspace key can be used to return to the previous submenu (if there was no previous submenu, this key returns to the main menu).",
    "",
    "Choosing player names:",
    "After selecting a gamemode, a submenu will open prompting the user to enter the players' names. For the \"VS COMPUTER\" gamemode, \"Player 1\" represents the human and \"Computer\" represents the AI. By default, each player name is left blank. In order to specify each player's name, the user should hover over either the \"Player 1\" or \"Player 2\" option and enter the name using the keyboard. Names can only contain ASCII characters.",
    "",
    "Choosing player colors:",
    "After choosing player names, a submenu will open prompting the user to chooose each player's color. By default, \"Player 1\" is set to white while \"Player 2\" is set to black. This can be swapped by selecting the \"Swap\" option on the menu",
    "",
    "How to play:",
    "After choosing player names and colors, the game will be started. When it is your turn a move can be entered in algebraic notation (e.g. \"Nf3\", \"e4\", \"O-O-O\",\"exf4+\", \"Rxd4#\"). After entering your move, the system will confirm that your move is valid and then make the move. It will then be the other player's turn. If the \"VS COMPUTER\" gamemode was selected, the computer will quickly choose a move and then the current turn will be given back to the player."
]
