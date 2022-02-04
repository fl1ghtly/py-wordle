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
        
    def choose_initial_word(self):
        with open(words_path, 'r') as f:
            words = f.read().splitlines()
            index = random.randrange(0, len(words))
            return words[index].lower()
            
    def simulate_game(self):
        self.game.set_word()
        
        guess = self.choose_initial_word()
        self.game.receive_guess(guess)
        corr = self.game.get_corrected_word()

        while not self.game.finished:
            print(f'Guess is {guess}')
            print(f'Correction is {corr}')
            
            self.assisstant.set_correction(corr)
            self.assisstant.set_anchor()
            self.assisstant.set_incorrect()

            self.assisstant.incorrect = self.assisstant.clean_input(self.assisstant.incorrect)
            self.assisstant.clean_correction = self.assisstant.clean_input(self.assisstant.correction)

            self.assisstant.guess_word()
            idx = random.randrange(0, len(self.assisstant.possible_words))
            guess = self.assisstant.possible_words[idx]
            self.game.receive_guess(guess)

            corr = self.game.get_corrected_word()
            self.game.end_game(corr)


        print(f'The word was {self.game.word}!')
