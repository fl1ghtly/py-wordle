import os, sys

words_path = os.path.join(sys.path[0], 'words.txt')

def find_anchors(letters) -> list:
    anchor = []
    for i in range(len(letters)):
        if '*' in letters[i]:
            anchor.append(i)
    return anchor

def find_incorrect(letters, incorrect) -> list:
    for i in range(len(letters)):
        if '-' in letters[i]:
            incorrect[i].append(letters[i])
        
    return incorrect

def check_valid_anchor(word, letters, anchor) -> bool:
    if not anchor:
        return False
    
    for index in anchor:
        if word[index] != letters[index]:
            return False
        
    return True

def clean_input(l):
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
            new_list.append(clean_input(element))
        else:
            new_list.append(element[0])
    return new_list

def is_invalid_guess(letters, word, anchor, incorrect_ltrs) -> bool:
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
    for i in range(len(letters)):
        if i in anchor:
            continue
        if letters[i] == word[i]:
            return True
        
    # Checks if the word contains already guessed letters
    for i in range(len(incorrect_ltrs)):
        for j in range(len(incorrect_ltrs[i])):
            if incorrect_ltrs[i][j][0] == word[i]:
                return True
        
    return False

def get_potential_words(letters, words, anchors) -> list:
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
    if not anchors:
        return words
    for word in words:
        if check_valid_anchor(word, letters, anchors):
            potential_words.append(word)
        if not anchors:
            potential_words.append(word)
    return potential_words

def guess_word(guess, words, anchors=[], incorrect_ltrs=[]) -> list:
    guesses = []
    # TODO optimize search by stopping loop for letters at anchor
    # index 0 because this is a dictionary
    potential = get_potential_words(guess, words, anchors)

    for pword in potential:
        # Skips the word if it is invalid
        if is_invalid_guess(guess, pword, anchors, incorrect_ltrs):
            continue
        
        valid = True
        for i, letter in enumerate(guess):
            # Skips over letters that are already known to be incorrect
            if letter in incorrect_ltrs[i]:
                continue
            if letter not in pword and letter != '?':
                valid = False
                break
        if valid:
            guesses.append(pword)

    return guesses

if __name__ == '__main__':
    running = True
    with open(words_path, 'r') as f:
        words = f.read().splitlines()
    possible_words = words
    
    incorrect = [[], [], [], [], []]
    while running:
        letters = input("What are the correct letters: ").split()

        if len(letters) > 5:
            print('There are too many letters')
            continue

        anchor = find_anchors(letters)
        incorrect = find_incorrect(letters, incorrect)
        incorrect = clean_input(incorrect)
        modified_letters = clean_input(letters)
        possible_words = guess_word(modified_letters, possible_words, anchor, incorrect)
        
        print(possible_words)
        if len(possible_words) <= 1:
            running = False