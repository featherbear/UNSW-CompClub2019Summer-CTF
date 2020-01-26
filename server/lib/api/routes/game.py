from .. import routing, JSON
from tornado.web import authenticated, RequestHandler

from ...ctf import SQLMethod as ctfSQLMethod
from ...auth import SQLMethod as authSQLMethod
from sqlite3 import IntegrityError

from ...authSession.methods import authenticated


@routing.GET("/scores.json")
def scores(self: RequestHandler, args: dict):
    questionsSQL = ctfSQLMethod.questions.getQuestions()

    solvesSQL = ctfSQLMethod.questions.getSolves()

    usersSQL = authSQLMethod.getUsers()

    pointsMap = {}
    for question in questionsSQL:
        pointsMap[question[0]] = question[3]

    scores = {}
    for user in usersSQL:
        scores[user[0]] = dict(name=user[2] or user[1],  # user might not have a display name?
                               points=0)

    for solve in solvesSQL:
        try:
            scores[solve[0]]["points"] += pointsMap[solve[1]]
        except:
            pass

    return self.finish(JSON.DATA(scores))


@routing.GET("/solves.json")
@authenticated
def getSolves(self: RequestHandler, args: dict):
    if "question" in args:
        solves = ctfSQLMethod.questions.getSolves(question=args["question"])
        return self.finish(JSON.DATA(dict(count=len(solves))))

    if "user" in args:
        solves = ctfSQLMethod.questions.getSolves(user=args["user"])
        return self.finish(JSON.DATA(solves))

    solves = ctfSQLMethod.questions.getSolves()
    solvesMap = {}
    for userID, questionID in solves:
        if questionID not in solvesMap:
            solvesMap[questionID] = 0
        solvesMap[questionID] += 1

    return self.finish(JSON.DATA(solvesMap))


@routing.POST("/question/solve")
@authenticated
def trySolve(self: RequestHandler, args: dict):

    if self.current_user["id"] == 0:
        self.finish(JSON.ERROR("Admin cannot participate in challenges"))
        return

    flag = args["flag"]
    question = args["question"]
    if flag != ctfSQLMethod.questions.getFlag(question):
        return self.finish(JSON.FALSE())

    try:
        ctfSQLMethod.questions.solveQuestion(
            self.current_user["id"], question)
    except IntegrityError:
        pass

    return self.finish(JSON.TRUE())
