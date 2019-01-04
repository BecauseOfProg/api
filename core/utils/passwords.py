from argon2 import PasswordHasher, exceptions
import bcrypt

ph = PasswordHasher()


class ArgonHasher:
    @staticmethod
    def generate_password(password):
        return ph.hash(password)

    @staticmethod
    def are_password_same(hashed, password):
        try:
            return ph.verify(hashed, password)
        except exceptions.VerifyMismatchError:
            return False


class BcryptHasher:
    @staticmethod
    def generate_password(password):
        return str(
            bcrypt.hashpw(
                bytes(password, "utf-8"),
                bcrypt.gensalt())) \
            .replace("b'", "")[:-1]

    @staticmethod
    def are_password_same(hashed, password):
        return bcrypt.checkpw(
            bytes(password, "utf-8"),
            bytes(hashed, "utf-8"))

