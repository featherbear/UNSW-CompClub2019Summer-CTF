from typing import Union

from . import Tools
from .SQLMethod import SQLMethod
from ..config import config

userType = Union[int, str]


class UserSession:
    id: int = None
    username: str = None
    name: str = None

    def __init__(self, user: userType):
        if user == 0:
            self.id = 0
            self.username = config["ADMIN"].get("username", "admin")
            self.name = "Admin"
        else:
            data = SQLMethod.getUser(user)
            if not data:
                raise Exception("No such user")
            if type(user) is int:
                self.id = user
                self.username = data[0]
            else:
                self.id = data[0]
                self.username = user
            self.name = data[1]

    def changePassword(self, password: str):
        return Tools.changePassword(self.id, password)