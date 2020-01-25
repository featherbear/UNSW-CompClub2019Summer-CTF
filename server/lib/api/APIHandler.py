import re
import tornado.web
from time import time
from tornado.escape import json_decode

# from ..authSession import getSession, updateSession


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
    # def get_current_user(self):
    #     try:
    #         print(self)
    #         token = self.get_secure_cookie("session").decode()
    #         user, expiry = getSession(token)
    #         if int(time()) < expiry:
    #             return UserSession(user)
    #     except Exception:
    #         return False

    get = _generateRequestMethodHandler("GET")
    post = _generateRequestMethodHandler("POST")
    put = _generateRequestMethodHandler("PUT")
    delete = _generateRequestMethodHandler("DELETE")
