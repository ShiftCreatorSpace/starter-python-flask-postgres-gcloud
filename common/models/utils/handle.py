import string
import random


def random_string(string_length=4):
    s = string.ascii_uppercase + string.digits
    return ''.join(random.sample(s, string_length))
