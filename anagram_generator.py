import random

def load_words():
    with open('words.txt', 'r') as file:
        words = file.read().splitlines()
    return words

def generate_anagram():
    words = load_words()
    selected_words = random.sample(words, 10)  # Select 10 random words
    anagrams = [''.join(random.sample(word, len(word))) for word in selected_words]
    return anagrams

def is_valid_anagram_solution(puzzle, solution):
    for original, submitted in zip(puzzle, solution):
        if ''.join(sorted(original)) != ''.join(sorted(submitted)):
            return False
    return True