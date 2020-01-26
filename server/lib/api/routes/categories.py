from ...authSession.methods import authenticated, authorised
from .. import routing, JSON
from tornado.web import RequestHandler

from ...ctf import SQLMethod as ctfSQLMethod
from ...auth import SQLMethod as authSQLMethod

from sqlite3 import IntegrityError

ERROR_MESSAGE_DUPLICATE = "A category exists with the same name"

@routing.GET("/categories.json")
@authenticated
def categories(self: RequestHandler, args: dict):
    self.finish(JSON.DATA(ctfSQLMethod.categories.getCategories()))

@routing.POST("/category")
@authorised
def categorySubmit(self: RequestHandler, args: dict):
    try:
        result = ctfSQLMethod.categories.createCategory(**args)
    except IntegrityError:
        return self.finish(JSON.ERROR(ERROR_MESSAGE_DUPLICATE))

    if result:
        return self.finish(JSON.DATA(dict(id=result)))

    return self.finish(JSON.FALSE())


@routing.PUT("/category")
@authorised
def categoryEdit(self: RequestHandler, args: dict):
    try:
        result = ctfSQLMethod.categories.editCategory(**args)
    except IntegrityError:
        return self.finish(JSON.ERROR(ERROR_MESSAGE_DUPLICATE))
  
    if result:
        return self.finish(JSON.TRUE())

    return self.finish(JSON.FALSE())

@routing.DELETE("/category")
@authorised
def categoryDelete(self: RequestHandler, args: dict):
    result = ctfSQLMethod.categories.deleteCategory(**args)

    if result:
        return self.finish(JSON.TRUE())
    return self.finish(JSON.FALSE())

