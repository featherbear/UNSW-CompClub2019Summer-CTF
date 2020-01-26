from os import urandom
import jwt
from hashlib import sha1
from time import time

from .SQLMethod import SQLMethod
from ..JSON import JSON
from ..config import config

from tornado.web import RequestHandler

from datetime import datetime, timedelta


def authenticated(function):
    def decorator(self, *args, **kwargs):
        if self.current_user:
            function(self, *args, **kwargs)
        else:
            self.set_status(401)
            self.finish(JSON.ERROR("Not Authenticated"))

    return decorator


def authorised(function):
    def decorator(self, *args, **kwargs):
        if self.current_user and self.current_user["id"] == 0:
            function(self, *args, **kwargs)
        else:
            self.set_status(403)
            self.finish(JSON.ERROR("Not Authorised"))

    return decorator

import random, string
def randomChars(length):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))

def createSession(user: int):
    token = jwt.encode(
        dict(id=user,
             exp=datetime.utcnow() + timedelta(days=1),
             rng=randomChars(5)
             ),
        config["SERVER"].get("secret"),
        algorithm='HS256'
    ).decode()

    forceAddSession(user, token)

    return token

def forceAddSession(user, token):
    return SQLMethod.newSession(user, token)

def deleteSession(*, user: int = None, token: str = None):
    return SQLMethod.deleteSession(user=user, token=token)

def getSession(token: str):
    if not token:
        return False
    return SQLMethod.getSession(token)

# def cleanup():
#     return SQLMethod.cleanup()
