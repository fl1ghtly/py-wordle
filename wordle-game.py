import os, sys
import random


words_path = os.path.join(sys.path[0], 'words.txt')

class Game:
    MAX_TRIES = 6
    
    def __init__(self) -> None:
        self.win = False
        self.finished = False
        self.current_tries = 0
    

    def set_word(self):
        with open(words_path, 'r') as f:
            words = f.read().splitlines()
            index = random.randrange(0, len(words))
            self.word = words[index].lower()
            

    def receive_guess(self, guess):
        with open(words_path, 'r') as f:
            words = f.read().splitlines()
            if guess.lower() not in words:
                return False

        self.guess = guess.lower()
        self.current_tries += 1
        return True
        
