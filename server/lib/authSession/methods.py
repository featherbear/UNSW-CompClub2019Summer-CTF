import jwt
from hashlib import sha1
from time import time

from .SQLMethod import SQLMethod
from ..JSON import JSON
from ..config import config

from tornado.web import RequestHandler


def authenticated(function):
    def decorator(self, *args, **kwargs):
        if self.current_user:
            function(self, *args, **kwargs)
        else:
            self.set_status(403)
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


def createSession(user: int):
    token = jwt.encode(
        dict(id=user),
        config["SERVER"].get("secret", "we_have_top_men_working_on_it"),
        algorithm='HS256'
    ).decode()

    SQLMethod.newSession(user, token)

    print("New token:", token)

    return token


# def updateSession(token: str):
#     return not not SQLMethod.updateSession(token, int(time()) + 120 * 60)


def getSession(token: str):
    if not token:
        return False
    return SQLMethod.getSession(token)


# def cleanup():
#     return SQLMethod.cleanup()
