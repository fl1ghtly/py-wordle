from wordleAssistant import Assistant
from wordleGame import Game
import os, sys
import random

words_path = os.path.join(sys.path[0], 'words.txt')

class Simulation:
    MAX_SIMULATIONS = 100
    
    def __init__(self) -> None:
        self.assisstant = Assistant()
        self.game = Game()