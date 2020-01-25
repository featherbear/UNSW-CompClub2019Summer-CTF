class SQLQuery:
    createTable = """
        CREATE TABLE IF NOT EXISTS user_sessions (
            user INTEGER NOT NULL,
            token TEXT NOT NULL,

            UNIQUE (token)
        )
        """
    add = """
        INSERT
        INTO user_sessions (user, token)
        VALUES (?, ?)
        """
    deleteByUser = "DELETE FROM user_sessions WHERE user = ?"
    deleteByToken = "DELETE FROM user_sessions WHERE token = ?"

    getSessionByToken = "SELECT user FROM user_sessions WHERE token = ?"
