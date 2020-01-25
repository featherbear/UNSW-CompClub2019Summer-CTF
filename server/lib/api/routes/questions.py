from ...authSession.methods import authenticated, authorised
from .. import routing, JSON
from tornado.web import RequestHandler

from ...ctf import SQLMethod as ctfSQLMethod
from ...auth import SQLMethod as authSQLMethod

from sqlite3 import IntegrityError


@routing.GET("/questions.json")
@authenticated
def questions(self: RequestHandler, args: dict):
    self.finish(JSON.data(ctfSQLMethod.questions.getQuestions()))


@routing.POST("/question")
@authenticated
@authorised
def questionSubmit(self: RequestHandler, args: dict):
    try:
        result = ctfSQLMethod.questions.createQuestion(**args)
    except IntegrityError:
        return self.finish(JSON.ERROR("A question exists with the same flag"))

    if result:
        return self.finish(JSON.DATA(dict(id=result)))

    return self.finish(JSON.FALSE())


@routing.PUT("/question")
@authenticated
@authorised
def questionEdit(self: RequestHandler, args: dict):
    if "flag" in args:
        try:
            result = ctfSQLMethod.questions.editQuestionFlag(**args)
        except IntegrityError:
            return self.finish(JSON.ERROR("A question exists with the same flag"))
    else:
        result = ctfSQLMethod.questions.editQuestion(**args)

    if result:
        return self.finish(JSON.TRUE())

    return self.finish(JSON.FALSE())

@routing.DELETE("/question")
@authenticated
@authorised
def questionDelete(self: RequestHandler, args: dict):
    result = ctfSQLMethod.questions.deleteQuestion(**args)

    if result:
        return self.finish(JSON.TRUE())
    return self.finish(JSON.FALSE())
