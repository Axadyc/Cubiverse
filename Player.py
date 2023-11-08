import Player
import GameBoardWindows

class Player():
    def __init__(self, number : int, gameboard_window : GameBoardWindows, typeofclass : str = "UNDEFINED") -> None:
        self._number : int = number
        self._inventory : list = []
        self._typeofclass : str = "UNDEFINED" # Can be UNDEFINED, CHOOSING, MINOR or FIGHTER
        self._gameboard_window = gameboard_window
        self._typeingameboard : str = ""
        self._health : int = 30
        self._attack : int = 10
        self._pos = (0,0)
        self._maxrange : int = 3
        if self._number == 1:
            self._pos = (6,1)
        elif self._number == 2:
            self._pos = (6,12)
        elif self._number == 3:
            self._pos = (1,6)
        elif self._number == 4:
            self._pos = (12,6)

        self.setTypeOfClass(typeofclass)

    def setTypeOfClass(self, type : str):
        if type == "MINOR":
            self._typeofclass = type
            self._typeingameboard = "_p_minor"
        elif type == "FIGHTER":
            self._attack = self._attack * 1.5
            self._typeofclass  = type
            self._typeingameboard = "_p_fighter"
        elif type == "CHOOSING":
            self._typeofclass = type


    def attack(self, p : Player) -> None:
        p._health = p._health - self._attack

    def resetMaxMovement(self) -> None:
        self._maxrange = 3

    def movePlayer(self, newPos : tuple) -> int:
        """Move the player and return the amount of movement

        Args:
            newPos (tuple): (int,int)

        Returns:
            int: amount of movement
        """
        if newPos != None:
            
            if self._pos[0] - self._maxrange <= newPos[0] <= self._pos[0] + self._maxrange:
                if self._pos[1] - self._maxrange <= newPos[1] <= self._pos[1] + self._maxrange:
                    
                    nb_movement = abs(self._pos[0] - newPos[0]) + abs(self._pos[1] - newPos[1])
                    if nb_movement <= 3:

                        # Remove typeingameboard of gameboard
                        self._gameboard_window._gameboard[self._pos[0]][self._pos[1]] = self._gameboard_window._gameboard[self._pos[0]][self._pos[1]].replace(self._typeingameboard, "")
                        # Add typeingameboard for the new pos
                        self._gameboard_window._gameboard[newPos[0]][newPos[1]] += self._typeingameboard
                        
                        self._pos = newPos
                        self._maxrange -= nb_movement
                        return nb_movement
            return 0
        
    def __repr__(self) -> str:
        return "Player : [number : " + str(self._number) + ", inventory : " + str(self._inventory) + ", type : " + self._typeofclass + ", health : " + str(self._health) + ", attack : " + str(self._attack) + ", pos : " + str(self._pos) + ", maxrange : " + str(self._maxrange) + "]"