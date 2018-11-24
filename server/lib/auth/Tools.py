from .SQLMethod import SQLMethod
from .. import database
from ..config import config


def authenticate(username, password):
    if "ADMIN" in config:
        if config["ADMIN"]["username"] == username and config["ADMIN"]["password"] == password:
            return 0
    else:
        if SQLMethod.checkPassword(username, password):
            return SQLMethod.getUser(username)
    return None


def passwordHash(password: str, salt: str = None):
    import hashlib, os
    _salt = salt if salt else os.urandom(16)
    hash = hashlib.pbkdf2_hmac('sha256', password.encode(), _salt, 1)
    return hash if salt else (hash, _salt)


def createUser(username: str, password: str, name: str):
    if username == config["ADMIN"].get("username", "admin"):
        return False

    hash, salt = passwordHash(password)
    return SQLMethod.createUser(username, name, hash, salt)


def changePassword(user: id, password: str):
    hash, salt = passwordHash(password)
    return SQLMethod.changeHashSalt(user, hash, salt)


database.conn.create_function("cHash", 2, passwordHash)