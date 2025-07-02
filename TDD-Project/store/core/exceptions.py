class BaseException(Exception):
    message: str = "Internal Server Error"

    def _init_(self, message: str | None = None) -> None:

        if message:
            self.message = message

class NotFoundException(BaseException):
    message = "Not Found"