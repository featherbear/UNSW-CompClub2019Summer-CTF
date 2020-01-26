from ...authSession.methods import authenticated, authorised
from .. import routing, JSON
from tornado.web import RequestHandler

from ...ctf import SQLMethod as ctfSQLMethod
from ...auth import SQLMethod as authSQLMethod

from sqlite3 import IntegrityError

ERROR_MESSAGE_DUPLICATE = "A question exists with the same flag"


@routing.GET("/questions.json")
@authenticated
def questions(self: RequestHandler, args: dict):
    self.finish(JSON.DATA(ctfSQLMethod.questions.getQuestions()))


@routing.POST("/question")
@authorised
def questionSubmit(self: RequestHandler, args: dict):
    if not ctfSQLMethod.categories.getCategory(args["category"]):
        return self.finish(JSON.FALSE())

    try:
        result = ctfSQLMethod.questions.createQuestion(**args)
    except IntegrityError:
        return self.finish(JSON.ERROR(ERROR_MESSAGE_DUPLICATE))

    if result:
        return self.finish(JSON.DATA(dict(id=result)))

    return self.finish(JSON.FALSE())


@routing.PUT("/question")
@authorised
def questionEdit(self: RequestHandler, args: dict):
    if "flag" in args:
        try:
            result = ctfSQLMethod.questions.editQuestionFlag(**args)
        except IntegrityError:
            return self.finish(JSON.ERROR(ERROR_MESSAGE_DUPLICATE))
    else:
        if "category" in args and not ctfSQLMethod.categories.getCategory(args["category"]):
            return self.finish(JSON.FALSE())
        
        result = ctfSQLMethod.questions.editQuestion(**args)

    if result:
        return self.finish(JSON.TRUE())

    return self.finish(JSON.FALSE())


@routing.DELETE("/question")
@authorised
def questionDelete(self: RequestHandler, args: dict):
    result = ctfSQLMethod.questions.deleteQuestion(**args)

    if result:
        return self.finish(JSON.TRUE())
    return self.finish(JSON.FALSE())


@routing.POST("/question/getFlag")
@authorised
def questionGetFlag(self: RequestHandler, args: dict):
    result = ctfSQLMethod.questions.getFlag(**args)

    if result:
        return self.finish(JSON.DATA(result))
    return self.finish(JSON.FALSE())
