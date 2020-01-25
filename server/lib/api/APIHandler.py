import re
import tornado.web
from time import time
from tornado.escape import json_decode

from ..config import config
from ..authSession import getSession, jwt


routes = {}


def _generateMethodDecorator(method):
    if method not in routes:
        routes[method] = {}

    def function(urlRegex):
        def wrapper(func):
            if urlRegex in routes[method]:
                raise Exception("Duplicate routing pattern: " + urlRegex)
            routes[method][urlRegex] = func
            return func

        return wrapper
    return function


class routing:
    GET = _generateMethodDecorator("GET")
    POST = _generateMethodDecorator("POST")
    PUT = _generateMethodDecorator("PUT")
    DELETE = _generateMethodDecorator("DELETE")


def _generateRequestMethodHandler(method):
    def function(self, path, **kwargs):
        try:
            args = json_decode(self.request.body or "{}")
        except:
            return self.finish(JSON.error("bad arguments"))
        for urlRegex, function in routes[method].items():
            urlRoute = re.fullmatch(urlRegex, "/" + path)
            if urlRoute:
                return function(self, *urlRoute.groups(), args=args, **kwargs)
        return self.finish(JSON.error("no route here"))
    return function


class APIHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        try:
            auth_header = self.request.headers.get("Authorization")
            canary, token = auth_header.split(" ", 1)

            # Remedial checking
            if canary != "Bearer":
                raise Exception()

            if not getSession(token):
                raise Exception()

            # TODO: Generate secret in the sqlite3 file
            return jwt.decode(token,
                               config["SERVER"]["secret"],
                               algorithms=['HS256']
                               )            
        except:
            return False

    get = _generateRequestMethodHandler("GET")
    post = _generateRequestMethodHandler("POST")
    put = _generateRequestMethodHandler("PUT")
    delete = _generateRequestMethodHandler("DELETE")
