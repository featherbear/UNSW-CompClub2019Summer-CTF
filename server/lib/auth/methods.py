from .SQLMethod import SQLMethod
from .. import database
from ..config import config


def authenticate(username, password):
    username = username.strip().lower()
    password = password.strip()

    adminUsername = config["ADMIN"].get("username", "").lower()
    adminPassword = config["ADMIN"].get("password")

    if len(username) == 0:
        return None

    if adminUsername == username and adminPassword == password:
        # Admin is UID 0
        return 0

    return SQLMethod.checkPassword(username, password)


def passwordHash(password: str, salt: str = None):
    import hashlib
    import os

    _salt = salt or os.urandom(16)

    hash = hashlib.pbkdf2_hmac('sha256', password.encode(), _salt, 1)
    return hash if salt else (hash, _salt)


def createUser(username: str, password: str, name: str):
    username = username.strip().lower()

    if len(username) == 0:
        return False

    if username == config["ADMIN"].get("username", "admin").lower():
        return False

    hash, salt = passwordHash(password)
    return SQLMethod.createUser(username, name.strip(), hash, salt)


def getUser(user):
    return SQLMethod.getUser(user)

def getUsers():
    return SQLMethod.getUsers()

def deleteUser(user: int):
    return SQLMethod.deleteUser(user)


def changePassword(user: id, password: str):
    hash, salt = passwordHash(password)
    return SQLMethod.changeHashSalt(user, hash, salt)


database.conn.create_function("cHash", 2, passwordHash)
