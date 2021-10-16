### Gamemodes ###
VS_COMPUTER = 0
LOCAL_GAME = 1
THROUGH_SSH = 2

### Colors ###
# Main Menu Colors
MM = 1

# Chessboard Colors
WW = 2 # White on White
BW = 3 # Black on White
WB = 4 # White on Black
BB = 5 # Black on Black

# Error Message During Game
ER = 6

# Sub Menu Colors
SM = 7
SM2 = 8


class ReturnToMainMenu(Exception):
    pass
