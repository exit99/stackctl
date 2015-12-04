__all__ = ["CommandExecutionError", "InvalidCommandArgs",
           "WrapperFailure", "ConnectionFailure", "CredentialError"]


class CredentialError(Exception):
    pass


class CommandExecutionError(Exception):
    pass


class InvalidCommandArgs(Exception):
    pass


class WrapperFailure(Exception):
    pass


class ConnectionFailure(Exception):
    pass
