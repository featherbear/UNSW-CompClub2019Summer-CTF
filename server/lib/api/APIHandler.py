import re
import tornado.web
from time import time
from tornado.escape import json_decode

from ..JSON import JSON
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
            self.set_status(400)
            return self.finish(JSON.ERROR("Malformed"))
        for urlRegex, function in routes[method].items():
            urlRoute = re.fullmatch(urlRegex, "/" + path)
            if urlRoute:
                return function(self, *urlRoute.groups(), args=args, **kwargs)
        self.set_status(404)
        return self.finish(JSON.ERROR("No route here"))
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
            data = jwt.decode(token,
                              config["SERVER"]["secret"],
                              algorithms='HS256'
                              )
            data["token"] = token
            return data
        except:
            return False

    get = _generateRequestMethodHandler("GET")
    post = _generateRequestMethodHandler("POST")
    put = _generateRequestMethodHandler("PUT")
    delete = _generateRequestMethodHandler("DELETE")
