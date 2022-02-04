import os, sys
import random

words_path = os.path.join(sys.path[0], 'words.txt')

class Assistant:
    def __init__(self) -> None:
        with open(words_path, 'r') as f:
            self.possible_words = f.read().splitlines()
        self.correction = []
        self.clean_correction = []
        self.incorrect = [[], [], [], [], []]
        self.anchor = []

    def reset(self):
        with open(words_path, 'r') as f:
            self.possible_words = f.read().splitlines()
        self.correction = []
        self.clean_correction = []
        self.incorrect = [[], [], [], [], []]
        self.anchor = []
        
    def set_correction(self, correction):
        self.correction = correction
        
    def set_anchor(self) -> list:
        for i in range(len(self.correction)):
            if '*' in self.correction[i]:
                self.anchor.append(i)

    def set_incorrect(self) -> list:
        for i in range(len(self.correction)):
            if '-' in self.correction[i]:
                self.incorrect[i].append(self.correction[i])
            
    def check_valid_anchor(self, word) -> bool:
        if not self.anchor:
            return False
        
        for index in self.anchor:
            if word[index] != self.clean_correction[index]:
                return False
            
        return True

    def clean_input(self, l):
        '''Takes a list and recursively iterates to find all non-list
        elements and returns the first character of it
        Args:
            l (list): A (nested) list of strings
        Returns:
            new_list (list): returns the same list but with only the first 
            character
        '''
        new_list = []
        for element in l:
            if type(element) is list:
                new_list.append(self.clean_input(element))
            else:
                new_list.append(element[0])
        return new_list

    def is_invalid_guess(self, word) -> bool:
        '''Finds if a word has either letters that have already been 
        guessed as incorrect or does not contain the anchor letters
        in the correct position
        
        Args:
            letters (list): letters of the guess
            words (list): letters of the current word to check
            anchors (list): list of indexes that are correct guesses
            incorrect_ltrs (list): list of already guessed letters
        Return:
            boolean
        '''
        # Checks if all the anchor letters are in the correct position
        for i in range(len(self.clean_correction)):
            if i in self.anchor:
                continue
            if self.clean_correction[i] == word[i]:
                return True
            
        # Checks if the word contains already guessed letters
        for i in range(len(self.incorrect)):
            for j in range(len(self.incorrect[i])):
                if self.incorrect[i][j][0] == word[i]:
                    return True
            
        return False

    def get_potential_words(self) -> list:
        '''Finds all possible words given a few anchor letters
        or if given no anchor, returns words
            letters (list): letters of the guess
            words (list): list of words to check
            anchors (list): list of indexes that are correct guesses
        Args:
        Returns:
            list: list of potential words
        '''
        potential_words = []
        if not self.anchor:
            return self.possible_words
        for word in self.possible_words:
            if self.check_valid_anchor(word):
                potential_words.append(word)
        return potential_words

    def pick_random_words(self):
        choices = []
        domain = 5 if len(self.possible_words) > 5 else len(self.possible_words)
        for i in range(domain):
            index = random.randrange(0, len(self.possible_words))
            choices.append(self.possible_words[index])
        return choices
        
    def guess_word(self) -> list:
        guesses = []
        # TODO optimize search by stopping loop for guess at anchor
        # index 0 because this is a dictionary
        potential = self.get_potential_words()

        for pword in potential:
            # Skips the word if it is invalid
            if self.is_invalid_guess(pword):
                continue
            
            valid = True
            for i, letter in enumerate(self.clean_correction):
                # Skips over letters that are already known to be incorrect
                if letter in self.incorrect[i]:
                    continue
                if letter not in pword and letter != '?':
                    valid = False
                    break
            if valid:
                guesses.append(pword)

        self.possible_words = guesses

if __name__ == '__main__':
    running = True
    helper = Assistant()
    
    while running:
        letters = input("What are the correct letters: ").split()

        if len(letters) != 5:
            print('Please choose a 5 letter word')
            continue
        
        helper.set_correction(letters)
        helper.set_anchor()
        helper.set_incorrect()

        helper.incorrect = helper.clean_input(helper.incorrect)
        helper.clean_correction = helper.clean_input(helper.correction)
        helper.guess_word()
        
        print(helper.pick_random_words())
        if len(helper.possible_words) <= 1:
            running = False