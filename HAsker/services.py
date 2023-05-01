import random
import string
import lorem

def random_word(max_length):
    return ''.join(random.choice(string.ascii_lowercase)
                    for _ in range(random.randint(1, max_length)))

def random_sentence(max_word_length, max_word_num):
    return ' '.join(random_word(max_word_length)
                    for _ in range(random.randint(1, max_word_num)))

def random_text(max_word_length, max_word_num, max_sentence_num):
    return '. '.join(random_sentence(max_word_length, max_word_num)
                    for _ in range(random.randint(1, max_sentence_num)))