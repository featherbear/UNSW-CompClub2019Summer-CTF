from ...ctf import SQLMethod as CTFtools
import tornado.httputil
import tornado.web

from .. import routing, JSON
from ...auth import methods as authTools
from ...authSession import methods as sessionTools, authenticated, authorised
from ...config import config
from sqlite3 import IntegrityError


@routing.POST("/auth/login")
def login(self: tornado.web.RequestHandler, args: dict):
    self.request: tornado.httputil.HTTPServerRequest

    if "username" in args and "password" in args:
        uid = authTools.authenticate(args["username"], args["password"])
        if uid is not None:
            return self.finish(JSON.DATA(dict(token=sessionTools.createSession(uid))))

        return self.finish(JSON.ERROR("Invalid username or password"))
    return self.finish(JSON.FALSE())


@routing.POST("/auth/logout")
@authenticated
def logout(self: tornado.web.RequestHandler, args: dict):
    self.request: tornado.httputil.HTTPServerRequest

    sessionTools.deleteSession(token=self.current_user["token"])

    return self.finish(JSON.TRUE())


@routing.GET("/auth")
@authorised
def getUsers(self: tornado.web.RequestHandler, args: dict):
    return self.finish(JSON.DATA(authTools.getUsers()))


@routing.PUT("/auth")
@authenticated
def changePassword(self: tornado.web.RequestHandler, args: dict):
    self.request: tornado.httputil.HTTPServerRequest

    newPassword = args["password"]

    isAdmin = self.current_user["id"] == 0
    targetId = args.get("id", self.current_user["id"])

    isChangingSelf = targetId == self.current_user["id"]

    if isChangingSelf and isAdmin:
        self.set_status(400)
        self.finish(JSON.ERROR("Admin password can only be modified locally"))
        return

    if not isChangingSelf and not isAdmin:
        self.set_status(403)
        self.finish(JSON.ERROR("Not Authorised"))
        return

    result = authTools.changePassword(targetId, newPassword)

    if not result:
        self.finish(JSON.ERROR("User does not exist"))
        return

    sessionTools.deleteSession(user=targetId)

    if isChangingSelf:
        sessionTools.forceAddSession(targetId, self.current_user["token"])

    return self.finish(JSON.TRUE())


@routing.POST("/auth")
def register(self: tornado.web.RequestHandler, args: dict):
    if self.current_user:
        return self.finish(JSON.ERROR("User already authenticated"))

    self.request: tornado.httputil.HTTPServerRequest

    username = args["username"]
    password = args["password"]
    name = args["name"]

    try:
        uid = authTools.createUser(username, password, name)
    except IntegrityError:
        return self.finish(JSON.ERROR("Username taken"))

    if uid is not None:
        return self.finish(JSON.DATA(dict(token=sessionTools.createSession(uid))))

    return self.finish(JSON.ERROR("Something went wrong"))


@routing.DELETE("/auth")
@authorised
def delete(self: tornado.web.RequestHandler, args: dict):
    self.request: tornado.httputil.HTTPServerRequest

    user = args["id"]

    result = authTools.deleteUser(user)

    if not result:
        self.finish(JSON.ERROR("User does not exist"))
        return

    sessionTools.deleteSession(user=user)
    CTFtools.questions.deleteUser(user)

    self.finish(JSON.TRUE())


@routing.POST("/auth/usernameAvailable")
def usernameAvailable(self: tornado.web.RequestHandler, args: dict):
    self.request: tornado.httputil.HTTPServerRequest

    username = args["username"].strip().lower()

    if len(username) == 0:
        return self.finish(JSON.FALSE())

    if username != config["ADMIN"].get("username", "admin") and not authTools.getUser(args["username"]):
        return self.finish(JSON.TRUE())

    return self.finish(JSON.FALSE())


@routing.POST("/auth/validate")
def tokenValid(self: tornado.web.RequestHandler, args: dict):
    return self.finish(JSON.TRUE() if self.current_user else JSON.FALSE())
