import os, sys

words_path = os.path.join(sys.path[0], 'words.txt')

def find_anchors(letters):
    anchor = []
    for i in range(len(letters)):
        if '*' in letters[i]:
            anchor.append(i)
    return anchor

def find_incorrect(letters):
    incorrect = []
    for letter in letters:
        if '-' in letter:
            incorrect.append(letter[0])
    return incorrect

def check_valid_anchor(word, letters, anchor):
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
    # Checks if all the anchor letters are in the correct position
    for i in range(len(letters)):
        if i in anchor:
            continue
        if letters[i] == word[i]:
            return True
        
    # Checks if the word contains already guessed letters
    for letter in incorrect_ltrs:
        if letter in word:
            return True
        
    return False

def get_potential_words(letters, words, anchors):
    potential_words = []
    for word in words:
        if check_valid_anchor(word, letters, anchors):
            potential_words.append(word)
        if not anchors:
            potential_words.append(word)
    return potential_words

def guess_word(letters, words, anchors=[], incorrect_ltrs=[]):
    guesses = []
    # TODO optimize search by stopping loop for letters at anchor
    # index 0 because this is a dictionary
    potential = get_potential_words(letters, words, anchors)

    for pword in potential:
        if is_invalid_guess(letters, pword, anchors, incorrect_ltrs):
            continue
        
        valid = True
        for letter in letters:
            if letter in incorrect_ltrs:
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
        words = f.readlines()
    possible_words = words
    
    while running:
        letters = input("What are the correct letters: ").split()

        if len(letters) > 5:
            print('There are too many letters')
            continue

        anchor = find_anchors(letters)
        incorrect = []
        incorrect.extend(find_incorrect(letters))
        modified_letters = [s[0] for s in letters]
        possible_words = guess_word(modified_letters, possible_words, anchor, incorrect)
        
        print(possible_words)
        if len(possible_words) <= 1:
            running = False