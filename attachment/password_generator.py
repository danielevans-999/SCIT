import secrets
import string

def generate_password():
    characters = '!@#' + string.ascii_letters + string.digits
    password = ''.join(secrets.choice(characters) for i in range(8))
    return password


print(generate_password())