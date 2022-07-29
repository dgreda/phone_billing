class NotFound(Exception):
    pass


class NotUniqueError(Exception):
    pass


class UserNotFound(NotFound):
    def __init__(self, id: int):
        message = f"User {id} not found!"
        super().__init__(message)


class CallNotFound(NotFound):
    def __init__(self, id: int):
        message = f"Call {id} not found!"
        super().__init__(message)


class InvoiceNotFound(NotFound):
    def __init__(self, id: int):
        message = f"Invoice {id} not found!"
        super().__init__(message)


class InvoiceAlreadyExists(NotUniqueError):
    def __init__(self, year: int, month: int, identifier: str):
        message = f"Invoice {identifier} for {month}/{year} already exists!"
        super().__init__(message)
