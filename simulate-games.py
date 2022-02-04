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
            
    def reset_simulation(self):
        self.assisstant.reset()
        self.game.reset()
        
    def simulate_game(self):
        for i in range(self.MAX_SIMULATIONS):
            self.game.set_word()
            
            guess = self.choose_initial_word()
            self.game.receive_guess(guess)
            corr = self.game.get_corrected_word()
            num_guesses = 1

            while not self.game.finished:
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
                num_guesses += 1

            if self.game.win:
                self.success += 1

                if num_guesses in Simulation.DATA:
                    Simulation.DATA[num_guesses] += 1
                else:
                    # Used in case we update max tries
                    Simulation.DATA.update({num_guesses: 1})
            
            self.reset_simulation()
                

if __name__ == '__main__':
    sim = Simulation()
    sim.simulate_game()