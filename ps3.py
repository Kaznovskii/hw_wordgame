# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : Kaznovskii Anton
# Collaborators : -
# Time spent    : 5 hours

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7
WILDCARD = '*'
SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, "*": 0
}
WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0

    """
    wordlen = len(word)

    first_component = sum((SCRABBLE_LETTER_VALUES[i.lower()] for i in word))
    second_component = 7*wordlen - 3*(n - wordlen)

    if second_component > 1:
        return first_component * second_component
    return first_component


def display_hand(hand):
    """Displays the letters currently in the hand.

    hand: dictionary (string -> int)
    returns: nothing, but prints all letters in hand

    """
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')
    print()


def deal_hand(n):
    """Returns a random hand containing n lowercase letters.

    n: int >= 0
    returns: dictionary (string -> int)

    """
    hand={}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels - 1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    hand[WILDCARD] = 1

    return hand


def update_hand(hand, word):
    """Updates the hand.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)

    Uses up the letters in the given word
    and returns the new hand, without those letters in it.
    Has no side effects: does not modify hand.

    """
    new_hand = hand.copy()

    for letter in word:
        letter = letter.lower()
        if letter in new_hand:
            new_hand[letter] -= 1
            if new_hand[letter] == 0:
                del new_hand[letter]
    return new_hand


def is_valid_word(word, hand, word_list):
    """Check word's correctness.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: True if word is in the word_list and is entirely
        composed of letters in the hand, False otherwise

    Does not mutate hand or word_list.

    """
    new_hand = hand.copy()
    word = word.lower()

    if word in word_list:
        checking_word = word
        return is_in_hand(checking_word, new_hand)

    elif WILDCARD in word:
        if is_in_hand(word, new_hand):
            for vowel in VOWELS:
                checking_word = word.replace(WILDCARD, vowel)
                if checking_word in word_list:
                        return True

    return False


def is_in_hand(word, hand):
    """Checks letters from word for being in hand

    word: string
    hand: dictionary (string -> int)
    returns: True if all letters from checking word are in hand,
        False otherwise

    """
    for letter in word:
        if letter in hand:
            hand[letter] -= 1
            if hand[letter] == 0:
                del hand[letter]
        else:
            return False
    return True
    

def calculate_handlen(hand):
    """Counts the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer

    """
    return sum(hand.get(i) for i in hand)


def play_hand(hand, word_list):
    """Allows the user to play the given hand.

    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: the total score for the hand

    """
    # Keep track of the total score
    score = 0
    # As long as there are still letters left in the hand:
    while bool(len(hand)):
        # Display the hand
        print("Current Hand: ", end="")
        display_hand(hand)
        # Ask user for input
        word = input("Enter word, or “!!” to indicate that you are finished: ")
        # If the input is two exclamation points:
        if word == "!!":
            # End the game (break out of the loop)
            break
        # Otherwise (the input is not two exclamation points):
        else:
            # If the word is valid:
            if is_valid_word(word, hand, word_list):
                # Tell the user how many points the word earned,
                # and the updated total score
                score += get_word_score(word, calculate_handlen(hand))

                print('"' + word + '"', 'earned', 
                    str(get_word_score(word, calculate_handlen(hand))) + '. Total:', 
                    score, 'points')
            # Otherwise (the word is not valid):
            else:
                # Reject invalid word (print a message)
                print("This is not a valid word. Please choose another word.")
            # update the user's hand by removing the letters of their inputted word
            hand = update_hand(hand, word)
        print()

    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score
    print("Total score for this hand:", score, "points.")

    # Return the total score as result of function
    return score


def substitute_hand(hand, letter):
    """ 
    Changes selected letter in current hand

    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)

    """
    if letter in hand:
        possible_letters = set(VOWELS).union(set(CONSONANTS)).difference(set(hand))
        new_letter = random.choice(list(possible_letters))
        hand[new_letter] = hand.get(letter)
        del hand[letter]

    return hand
     
    
def play_game(word_list):
    """Main gaming function for several hands with total score.

    word_list: list of lowercase strings
    return: int, total score for the series of hands

    Displays all game process.

    """
    total_score = 0
    replay = False

    # Entering amount of hands
    while True:
        try:
            hands_amount = int(input("Enter total number of hands: "))
            if hands_amount < 1:
                raise ValueError
            break
        except ValueError:
            print("Please, enter a natural number.")

    # Playing amount of entered hands
    for j in range(hands_amount):
        hand = deal_hand(HAND_SIZE)
        print("Current Hand: ", end="")
        display_hand(hand)
        print()

        # Substitution
        substitution = yes_no("Would you like to substitute a letter? ")
        if substitution:
            while True:
                substitute_letter = input("Which letter would you like to replace: ").lower()
                if len(substitute_letter) == 1 and substitute_letter.isalpha():
                    hand = substitute_hand(hand, substitute_letter)
                    break
                else:
                    print("Please, enter only 1 latin letter.")
        print()

        # Playing a hand
        score = play_hand(hand, word_list)
        print("-"*8)
        if not replay:
            # Asking for replaying current hand
            replay = yes_no("Would you like to replay the hand? ")
            if replay:
                replay_score = play_hand(hand, word_list)
                score = max(score, replay_score)
                print("-"*8)
            
        
        # Adding total score
        total_score += score

    print("Total score over all hands:", total_score)
    return total_score
    

def yes_no(question):
    """Allows to ask user yes/no question.

    question: string with question to ask user about
    returns: True if user answers "yes",
        False if user answers "no
    
    """
    while True:
        ask = input(question).lower()
        if ask.lower() == "yes":
            return True
        elif ask.lower() == "no":
            return False
        print("Plese, enter only 'yes' or 'no'.")

    

if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
