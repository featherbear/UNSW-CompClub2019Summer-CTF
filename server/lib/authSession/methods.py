from hashlib import sha1
from time import time

from .SQLMethod import SQLMethod
from ..JSON import JSON


def authenticated(function):
    def decorator(self, *args, **kwargs):
        try:
            auth_header = self.request.headers.get("Authorization")
            canary, token = auth_header.split(" ", 1)

            # Remedial checking
            if canary != "Bearer":
                raise Exception()

        except:
            self.set_status(403)
            self.finish(JSON.error("Not Authenticated"))
        else:
            function(self, *args, **kwargs)

    return decorator


def createSession(user: int):
    currentTime = int(time())
    token = sha1((str(user) + ":" + str(currentTime)).encode()).hexdigest()
    SQLMethod.newSession(user, currentTime + 120 * 60, token)
    return token


def updateSession(token: str):
    return not not SQLMethod.updateSession(token, int(time()) + 120 * 60)


def getSession(token: str):
    if not token:
        return False
    return SQLMethod.getSession(token)


def cleanup():
    return SQLMethod.cleanup()
