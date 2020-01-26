from .SQLQuery import SQLQuery
from .. import database


def assertSQLResult(*result):
    result = all(result)

    if result:
        database.conn.commit()
    else:
        database.conn.rollback()
    return result


class SQLMethod:
    class questions:
        # User Functions
        @staticmethod
        def solveQuestion(user: int, question: int):
            return database.insert(SQLQuery.solves.add, (user, question))

        # Admin functions
        @staticmethod
        def unsolveQuestion(user: int, question: int):
            return database.update(SQLQuery.solves.deleteSpecific, (user, question))

        @staticmethod
        def createQuestion(title: str, description: str, flag: str, value: int, category: int):
            return database.insert(SQLQuery.questions.add, (title, description, flag, value, category))

        @staticmethod
        def editQuestion(question: int, title: str, description: str, value: int, category: int):
            return database.update(SQLQuery.questions.edit, (title, description, value, category, question))

        @staticmethod
        def editQuestionFlag(question: int, flag: str):
            return database.update(SQLQuery.questions.editFlag, (flag, question))

        @staticmethod
        def deleteQuestion(question: int):
            result = database.update(SQLQuery.questions.delete, (question,))
            if result:
                database.update(SQLQuery.solves.deleteQuestion, (question,))
                return True
            return False

        @staticmethod
        def deleteUser(user: int):
            return database.update(SQLQuery.solves.deleteUser, (user,))

        # Helper functions
        @staticmethod
        def getFlag(question: int):
            result = database.fetchOne(SQLQuery.questions.getFlag, (question,))
            if result:
                return result[0]
            return None

        @staticmethod
        def getSolves(*, user: int = None, question: int = None):
            if not any([user is not None, question is not None]):
                return database.fetchAll(SQLQuery.solves.getAll)
            elif user is not None:
                return list(map(lambda result: result[0], database.fetchAll(SQLQuery.solves.getUser, (user,))))
            else:  # question is not None
                return list(map(lambda result: result[0], database.fetchAll(SQLQuery.solves.getQuestion, (question,))))

        @staticmethod
        def getQuestions(*, question: int = None, flag: bool = False):
            if question:
                if flag:
                    return database.fetchOne(SQLQuery.questions.getOneWithFlag, (question,))
                else:
                    return database.fetchOne(SQLQuery.questions.getOne, (question,))
            else:  # get all
                if flag:
                    return database.fetchAll(SQLQuery.questions.getAllWithFlag)
                else:
                    return database.fetchAll(SQLQuery.questions.getAll)

        getQuestion = getQuestions

    class categories:
        @staticmethod
        def getCategory(id):
            return database.fetchOne(SQLQuery.categories.getOne, (id,))

        @staticmethod
        def getCategories():
            categories = database.fetchAll(SQLQuery.categories.getAll)
            return {pair[0]: pair[1] for pair in categories}

        @staticmethod
        def createCategory(name: str):
            return database.insert(SQLQuery.categories.add, (name,))

        @staticmethod
        def editCategory(id: int, name: str):
            return database.update(SQLQuery.categories.edit, (name, id))

        @staticmethod
        def deleteCategory(id: int):
            result = database.update(SQLQuery.categories.delete, (id,))

            if result:
                database.update(
                    SQLQuery.categories.resetCategoriesFromID, (id,))
                return True

            return False
