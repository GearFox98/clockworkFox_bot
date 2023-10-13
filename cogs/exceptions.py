from enum import Enum

class RustyCog(Exception):
    def __init__(self, status, *args: object) -> None:
        self.status = status
    def __str__(self) -> str:
        return repr(self.status)

class Exceptions(Enum):
    CANT_BAN = 0
    NOT_A_GROUP = 1
    EMPTY_USER = 2
    NOT_AN_ADMIN = 3
    NO_ARGUMENT_PROVIDED = 4
    NON_EXISTENT_USER = 5