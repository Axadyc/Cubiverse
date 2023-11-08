# Example file showing a basic pygame "game loop"
import pygame
import json
from GameState import GameState
from GameBoardWindows import GameBoardWindows
from Player import Player

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# GameBoard
with open("gameboard.json") as gameboard_data:
    gameboard_json = json.load(gameboard_data)

gameboard = gameboard_json["gameboard"]

round_number = 1

gameboard_window : GameBoardWindows = GameBoardWindows(gameboard)


GAMESTATUS = GameState.HOMESCREEN
playerOne = Player(1, gameboard_window)
playerTwo = Player(2, gameboard_window)
playerThree = Player(3, gameboard_window)
playerFour = Player(4, gameboard_window)

list_players : list[Player] = [playerOne, playerTwo, playerThree, playerFour]

list_fighting_players : list[Player] = []

def drawMenu() -> None:
    """Draw menu
    """
    # render text
    label = myfont.render("Bonjour tout le monde !", 1, (0,0,0))
    screen.blit(label, (SCREEN_WIDTH / 2 - int(label.get_size()[0] / 2), SCREEN_HEIGHT / 2 - 200))

    pygame.draw.rect(screen, (0,0,0), (535,300,200,100))
    screen.blit(myfont_big.render("Jouer", 1, (255,0,0)), (573, 325))

def getButtonPressed(mouse_pos : tuple, origin : tuple, size : tuple) -> bool:
    """Get if btn is pressed

    Args:
        mouse_pos (tuple): Mouse position
        origin (tuple): Origin position of button
        size (tuple): (Width, Height)

    Returns:
        bool: True if it is, False else
    """
    if mouse_pos[0] >= origin[0] and mouse_pos[0] <= origin[0] + size[0]:
        if mouse_pos[1] >= origin[1] and mouse_pos[1] <= origin[1] + size[1]:
            return True
    return False

def drawPlayerImage(typeOfPlayer : str, coordinate : tuple) -> None:
    """Draw the image of the player with coordinate

    Args:
        typeOfPlayer (str): Type of player, can be MINOR or FIGHTER
        coordinate (tuple): position of the player in gameboard
    """
    # Button minor class
    path  = "./assets/png/"
    if typeOfPlayer == "MINOR":
        path = path + "pickaxe.png"
    elif typeOfPlayer == "FIGHTER":
        path = path + "sword.png"
    else:
        return
    image = pygame.image.load(path).convert_alpha()
    image = pygame.transform.scale(image, (image.get_width()*2, image.get_height()*2))
    screen.blit(image, coordinate)

def drawChoosePlayerMenu() -> None:
    """Draw the menu that shows all players
    """
    # render text
    label = myfont.render("Choisissez votre classe", 1, (0,0,0))
    screen.blit(label, (SCREEN_WIDTH / 2 - int(label.get_size()[0] / 2), SCREEN_HEIGHT / 2 - 200))

    # Player 1
    pygame.draw.rect(screen, (0,0,0), (400,250,100,100))
    screen.blit(myfont_big.render("1", 1, (255,0,0)), (440, 275))
    drawPlayerImage(playerOne._typeofclass, (235, 252))


    # Player 2
    pygame.draw.rect(screen, (0,0,0), (800,250,100,100))
    screen.blit(myfont_big.render("2", 1, (255,0,0)), (840, 275))
    drawPlayerImage(playerTwo._typeofclass, (635, 252))

    # Player 3
    pygame.draw.rect(screen, (0,0,0), (400,450,100,100))
    screen.blit(myfont_big.render("3", 1, (255,0,0)), (440, 475))
    drawPlayerImage(playerThree._typeofclass, (235, 452))

    # Player 4
    pygame.draw.rect(screen, (0,0,0), (800,450,100,100))
    screen.blit(myfont_big.render("4", 1, (255,0,0)), (840, 475))
    drawPlayerImage(playerFour._typeofclass, (635, 452))

    # Play button
    pygame.draw.rect(screen, (255,0,0), (527,610,250,50))
    screen.blit(myfont.render("Lancer", 1, (255,255,255)), (610,625))

def getGameBoardPositionByMouse(mouse_pos : tuple, max_gameboard_size : int = 14) -> tuple:
    """Return a tuple that represent the pos of mouse in the gameboard

    Args:
        mouse_pos (tuple): tuple with x and y pos
        max_gameboard_size (int, optional): Size of gameboard. Defaults to 14.

    Returns:
        tuple: (x,y) | None if the pos is invalid
    """
    y : int = int(mouse_pos[1] / 50)
    x : int = int((mouse_pos[0] - 1280 / 4.5) / 50) 
    if x >= 0 and x < max_gameboard_size:
        # x is in gameboard
        if y >= 0 and y < max_gameboard_size:
            return (y, x)
    return None

def getGameBoardPositionByCase(pos : tuple) -> tuple:
    """Return a tuple that represent the pos in the gameboard

    Args:
        pos (tuple): coordinate

    Returns:
        tuple: (x,y)
    """
    y : int = int(pos[1] * 50) + 1280 / 4.5
    x : int = int((pos[0]) * 50)
    return (y,x)

def getCaseByPosition(gameboard_pos : tuple) -> str:
    """Get case by position of the gameboard

    Args:
        gameboard_pos (tuple): Position in the gameboard

    Returns:
        str: letter that represent element in gameboard
    """
    if gameboard_pos != None:
        return(gameboard[gameboard_pos[0]][gameboard_pos[1]])

def drawChooseTypeOfPlayer(nb_player : int):
    #Fond
    pygame.draw.rect(screen, (100,100,100), (400,100,500,500))
    screen.blit(myfont_big.render(str(nb_player), 1, (255,255,255)), (640, 125))

    # Button minor class
    drawPlayerImage("MINOR", (600, 225))

    # Button sword class
    drawPlayerImage("FIGHTER", (600, 350))

    # Button done
    pygame.draw.rect(screen, (255,0,0), (527,510,250,50))
    screen.blit(myfont.render("Retour", 1, (255,255,255)), (610,525))

def drawUI(player : Player) -> None:
    
    label = myfont.render("Au tour du joueur : " + str(player._number), 1, (0,0,0))
    screen.blit(label, (10, 100))
    
    label = myfont_little.render("Type de joueur : " + player._typeofclass, 1, (0,0,0))
    screen.blit(label, (10, 125))

    label = myfont_little.render("Vie : " + str(player._health), 1, (0,0,0))
    screen.blit(label, (10, 145))

    label = myfont_little.render("Attaque : " + str(player._attack), 1, (0,0,0))
    screen.blit(label, (10, 165))

    label = myfont_little.render("Point de mouvement : " + str(player._maxrange), 1, (0,0,0))
    screen.blit(label, (10, 185))
    
    # Draw red box
    screen.blit(pygame.image.load("./assets/png/select.png").convert_alpha(), getGameBoardPositionByCase(player._pos))

    # Draw end of the round btn
    screen.blit(pygame.image.load("./assets/png/end_round.png").convert_alpha(), (993, 630))

def drawFight() -> None:
    i = 0
    for player in list_fighting_players:

        drawPlayerImage(player._typeofclass, (80 + i, 250))

        label = myfont_little.render("Numéro : " + str(player._number), 1, (0,0,0))
        screen.blit(label, (10 + i, 350))

        label = myfont_little.render("Type de joueur : " + player._typeofclass, 1, (0,0,0))
        screen.blit(label, (10 + i, 370))

        label = myfont_little.render("Vie : " + str(player._health), 1, (0,0,0))
        screen.blit(label, (10 + i, 390))

        label = myfont_little.render("Attaque : " + str(player._attack), 1, (0,0,0))
        screen.blit(label, (10 + i, 410))

        i += 1030

    pygame.draw.rect(screen, (100,255,100), (30,470,185,30))
    pygame.draw.rect(screen, (100,255,100), (1060,470,185,30))

def isCellOccuped(pos : tuple) -> bool:
    """Check if the cell is occuped by a player

    Args:
        pos (tuple): pos

    Returns:
        bool: True if there is a player in, False if not
    """
    for p in list_players:
        if (p._pos == pos):
            return True
    return False

def getPlayerByPos(pos : tuple) -> Player:
    for p in list_players:
        if (p._pos == pos):
            return p
    return None

def getPlayerByNum(num : int) -> Player:
    for p in list_players:
        if p._number == num:
            return p
    return None        

# pygame setup
pygame.init()
# initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
myfont : pygame.font = pygame.font.SysFont("monospace", 20)
myfont_little : pygame.font = pygame.font.SysFont("monospace", 16)
myfont_big : pygame.font = pygame.font.SysFont("monospace", 40)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True


while running:
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if GAMESTATUS == GameState.GAMELAUNCHED:

                # If a player is in mouse pos
                if isCellOccuped(getGameBoardPositionByMouse(pygame.mouse.get_pos())) and getPlayerByPos(getGameBoardPositionByMouse(pygame.mouse.get_pos()))._number != round_number:
                    list_fighting_players.append((getPlayerByPos(getGameBoardPositionByMouse(pygame.mouse.get_pos()))))
                    list_fighting_players.append(getPlayerByNum(round_number))
                    GAMESTATUS = GameState.FIGHT

                else:
                    # Try to move player if it's their round
                    for p in list_players:
                        if p._number == round_number:
                            p.movePlayer(getGameBoardPositionByMouse(pygame.mouse.get_pos()))

                
                # If the end turn btn is pressed
                if (getButtonPressed(pygame.mouse.get_pos(), (993, 630), (277,68))):
                    if round_number + 1 > 4:    
                        playerFour.resetMaxMovement()
                        round_number = 1
                    else:
                        if round_number == 1: playerOne.resetMaxMovement()
                        elif round_number == 2: playerTwo.resetMaxMovement()
                        elif round_number == 3: playerThree.resetMaxMovement()
                        round_number += 1      
            elif GAMESTATUS == GameState.CHOOSEMENU:
                # Player 1 button
                if getButtonPressed(pygame.mouse.get_pos(), (400,250), (100,100)):
                    GAMESTATUS = GameState.CHOOSEMENU_TYPE
                    playerOne.setTypeOfClass("CHOOSING")
                
                # Player 2 button
                elif getButtonPressed(pygame.mouse.get_pos(), (800,250), (100,100)):
                    GAMESTATUS = GameState.CHOOSEMENU_TYPE
                    playerTwo.setTypeOfClass("CHOOSING")

                # Player 3 button
                elif getButtonPressed(pygame.mouse.get_pos(), (400,450), (100,100)):
                    GAMESTATUS = GameState.CHOOSEMENU_TYPE
                    playerThree.setTypeOfClass("CHOOSING")

                # Player 4 button
                elif getButtonPressed(pygame.mouse.get_pos(), (800,450), (100,100)):
                    GAMESTATUS = GameState.CHOOSEMENU_TYPE
                    playerFour.setTypeOfClass("CHOOSING")  
                
                # Play button
                elif getButtonPressed(pygame.mouse.get_pos(), (527,610), (250,50)):
                    # Add player in gameboard
                    gameboard_window._gameboard[playerOne._pos[0]][playerOne._pos[1]] += playerOne._typeingameboard
                    gameboard_window._gameboard[playerTwo._pos[0]][playerTwo._pos[1]] += playerTwo._typeingameboard
                    gameboard_window._gameboard[playerThree._pos[0]][playerThree._pos[1]] += playerThree._typeingameboard
                    gameboard_window._gameboard[playerFour._pos[0]][playerFour._pos[1]] += playerFour._typeingameboard
                    GAMESTATUS = GameState.GAMELAUNCHED      
            elif GAMESTATUS == GameState.HOMESCREEN:
                # Play button
                if getButtonPressed(pygame.mouse.get_pos(), (535, 300), (200, 100)):
                    # Launch game
                    GAMESTATUS = GameState.CHOOSEMENU
            elif GAMESTATUS == GameState.CHOOSEMENU_TYPE:
                if getButtonPressed(pygame.mouse.get_pos(), (600, 225), (48*2,48*2)):
                    # The Choosing player is minor
                    for p in list_players:
                        if p._typeofclass == "CHOOSING":
                            p.setTypeOfClass("MINOR")
                  
                elif getButtonPressed(pygame.mouse.get_pos(), (600, 350), (48*2,48*2)):
                    # The Choosing player is fighter
                    for p in list_players:
                        if p._typeofclass == "CHOOSING":
                            p.setTypeOfClass("FIGHTER")

                elif getButtonPressed(pygame.mouse.get_pos(), (527,510), (610,525)):
                    GAMESTATUS = GameState.CHOOSEMENU
            elif GAMESTATUS == GameState.FIGHT:
                # Player left button
                if getButtonPressed(pygame.mouse.get_pos(), (400,250), (100,100)):
                    pass

    # If player is not defined, pass round automaticaly
    if getPlayerByNum(round_number)._typeofclass == "UNDEFINED":
        if round_number + 1 > 4:    
            playerFour.resetMaxMovement()
            round_number = 1
        else:
            if round_number == 1: playerOne.resetMaxMovement()
            elif round_number == 2: playerTwo.resetMaxMovement()
            elif round_number == 3: playerThree.resetMaxMovement()
            round_number += 1   

    if GAMESTATUS == GameState.HOMESCREEN:
        drawMenu()
    elif GAMESTATUS == GameState.CHOOSEMENU:
        drawChoosePlayerMenu()
    elif GAMESTATUS == GameState.CHOOSEMENU_TYPE:
        if playerOne._typeofclass == "CHOOSING":    drawChooseTypeOfPlayer(1)
        elif playerTwo._typeofclass == "CHOOSING":  drawChooseTypeOfPlayer(2)
        elif playerThree._typeofclass == "CHOOSING":drawChooseTypeOfPlayer(3)
        elif playerFour._typeofclass == "CHOOSING": drawChooseTypeOfPlayer(4)
        else:                                       GAMESTATUS = GameState.CHOOSEMENU
    elif GAMESTATUS == GameState.GAMELAUNCHED:
        gameboard_window.drawGameboard(screen)
        # Draw UI for good player
        for p in list_players:
            if p._number == round_number:
                drawUI(p)
    elif GAMESTATUS == GameState.FIGHT:
        drawFight()

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(24)

pygame.quit()