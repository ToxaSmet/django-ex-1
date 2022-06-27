import random
import string


def generate_random_string(size=16):
    return str(''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits + ' ', k=size)))
