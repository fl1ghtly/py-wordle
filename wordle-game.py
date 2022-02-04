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
    
    def end_game(self, correction):
        # Game is finished when max tries is exceeded
        if self.current_tries >= self.MAX_TRIES:
            self.finished = True
            
        for letter in correction:
            if '*' not in letter:
                return

        # Game is finished when the correct word is found
        self.finished = True
        self.win = True
                
            
if __name__ == '__main__':
    g = Game()
    g.set_word()
    while not g.finished:
        guess = input("Guess the word: ")

        if len(guess) != 5:
            print('Please only use 5 letter words')
            continue

        if not g.receive_guess(guess):
            print("Please type in a valid word")
            continue

        corr = g.get_corrected_word()
        print(corr)
        g.end_game(corr)
        

    print(f'The word was {g.word}!')