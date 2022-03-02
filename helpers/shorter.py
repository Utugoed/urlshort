import random
import string


def generate_link(length):
    letters = string.ascii_letters
    link = "".join(random.choice(letters) for i in range(length))
    return link
