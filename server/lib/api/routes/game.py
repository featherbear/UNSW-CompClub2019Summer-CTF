from .. import routing, JSON
from tornado.web import authenticated, RequestHandler

from ...ctf import SQLMethod as ctfSQLMethod
from ...auth import SQLMethod as authSQLMethod
from sqlite3 import IntegrityError

from ...authSession.methods import authenticated

@routing.GET("/leaderboard.json")
def leaderboard(self: RequestHandler, args: dict):
    questionsSQL = ctfSQLMethod.questions.getQuestions()
    solvesSQL = ctfSQLMethod.questions.getSolves()
    usersSQL = authSQLMethod.getUsers()

    pointsMap = {}
    for question in questionsSQL:
        pointsMap[question[0]] = question[3]

    leaderboard = {}
    for user in usersSQL:
        leaderboard[user[0]] = dict(name=user[2] or user[1],  # user might not have a display name?
                                    points=0)

    for solve in solvesSQL:
        try:
            leaderboard[solve[0]]["points"] += pointsMap[solve[1]]
        except:
            pass

    return self.finish(JSON.DATA(leaderboard))


@routing.POST("/ctf/userSolves.json")
@authenticated
def userSolves(self: RequestHandler, args: dict):
    return self.finish(JSON.data(ctfSQLMethod.questions.getSolves(user=self.current_user.id)))


@routing.POST("/ctf/questionSolves.json")
@authenticated
def questionSolves(self: RequestHandler, args: dict):
    return self.finish(JSON.data(len(ctfSQLMethod.questions.getSolves(question=args["question"]))))


@routing.POST("/ctf/solve")
@authenticated
def trySolve(self: RequestHandler, args: dict):
    if args["flag"] == ctfSQLMethod.questions.getFlag(args["question"]):
        try:
            ctfSQLMethod.questions.solveQuestion(
                self.current_user.id, args["question"])
            SSE_messages.addMessage(
                self.current_user.name + " has found a flag!")
        except IntegrityError:
            pass
        return self.finish(JSON.YES())
    return self.finish(JSON.NO())
