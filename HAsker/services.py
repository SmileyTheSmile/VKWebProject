import random
import string
import lorem
from lorem.text import TextLorem

def random_user_data(field_lengths):
    return (''.join(random.choice(string.ascii_lowercase)
                    for _ in range(random.randint(1, length)))
                    for length in field_lengths)

def random_question_data():
    return lorem.sentence(), lorem.text()

def random_tagword():
    return random.choice(lorem.sentence().split())

def random_tagwords(num):
    return TextLorem(srange=(num, num)).sentence().split()

def random_string(length):
    return ''.join(random.choice(string.ascii_lowercase)
                    for _ in range(random.randint(1, length)))

def random_user_data_list(num, max_lengths):
    return [random_user_data(max_lengths) for _ in range(num)]

def random_string_list(num, max_length):
    return [random_string(max_length) for _ in range(num)]