import random
import string


def generate_session_id():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(16))
