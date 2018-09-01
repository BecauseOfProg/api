from argon2 import PasswordHasher, exceptions

ph = PasswordHasher()


def generate_password(password):
    return ph.hash(password)


def are_password_same(hashed, password):
    try:
        return ph.verify(hashed, password)
    except exceptions.VerifyMismatchError:
        return False
