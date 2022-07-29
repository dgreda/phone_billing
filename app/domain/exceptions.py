class NotFound(Exception):
    pass


class UserNotFound(NotFound):
    def __init__(self, id: int):
        message = f"User {id} not found!"
        super().__init__(message)


class CallNotFound(NotFound):
    def __init__(self, id: int):
        message = f"Call {id} not found!"
        super().__init__(message)
