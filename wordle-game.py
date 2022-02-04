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
        
    def get_corrected_word(self):
        correction = []
        word_list = list(self.word)

        # This loop will not account for duplicate
        # letters in different positions
        # ex: These -> Those
        # It will mark both e's as correct instead
        # of only one e being correct 
        for i, letter in enumerate(self.guess):
            if letter in self.word:
                # Correct Letter in correct position
                if letter == self.word[i]:
                    correction.append(letter + '*')
                    word_list[i] = None
                # Correct Letter in wrong position
                else:
                    correction.append(letter)
            else:
                #Wrong Letter
                correction.append(letter + '-')
        
        # Loops over entire corrected list to find
        # any duplicated letters that were mistakenly
        # marked as correct in the wrong position
        for i, char in enumerate(correction):
            if char not in word_list and len(char) == 1:
                correction[i] += '-'

        return correction
