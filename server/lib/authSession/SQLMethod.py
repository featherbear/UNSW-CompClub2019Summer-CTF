from .SQLQuery import SQLQuery
from .. import database
from time import time


class SQLMethod:
    @staticmethod
    def newSession(user: int, token: str):
        return database.insert(SQLQuery.add, (user, token))

    @staticmethod
    def deleteSession(*, user: int = None, token: str = None):
        if user:
            return database.update(SQLQuery.deleteByUser, (user,))
        else:
            return database.update(SQLQuery.deleteByToken, (token,))

    @staticmethod
    def getSession(token: str):
        return database.fetchOne(SQLQuery.getSessionByToken, (token,))
