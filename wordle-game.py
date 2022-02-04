import os, sys
import random


words_path = os.path.join(sys.path[0], 'words.txt')

class Game:
    MAX_TRIES = 6
    
    def __init__(self) -> None:
        self.win = False
        self.finished = False
        self.current_tries = 0
