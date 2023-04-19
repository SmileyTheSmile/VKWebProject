import random
import string
import lorem

def random_word(max_length):
    return ''.join(random.choice(string.ascii_lowercase)
                    for _ in range(random.randint(1, max_length)))

def random_sentence(max_word_length, max_word_num):
    return ''.join(random_word(max_word_length)
                    for _ in range(random.randint(1, max_word_num)))

def random_text(max_word_length, max_word_num, max_sentence_num):
    return ''.join(random_sentence(max_word_length, max_word_num)
                    for _ in range(random.randint(1, max_sentence_num)))


def random_user_data(field_lengths):
    return (''.join(random.choice(string.ascii_lowercase)
                    for _ in range(random.randint(1, length)))
                    for length in field_lengths)

def random_question_data():
    return (random_sentence(12, 12),
            random_text(12, 12, 12))

def random_user_data_list(num, max_lengths):
    return [random_user_data(max_lengths) for _ in range(num)]

def random_word_list(num, max_length):
    return [random_word(max_length) for _ in range(num)]