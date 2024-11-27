class ClientNotFoundError(Exception):
    pass

class AccountNotFoundError(Exception):
    pass

class InsufficientFundsError(Exception):
    pass

class UnauthorizedAuthorError(Exception):
    pass

class DissolveTimeLimitError(Exception):
    pass