__all__ = ["CommandExecutionError", "InvalidCommandArgs",
           "WrapperFailure", "ConnectionFailure"]


class CommandExecutionError(Exception):
    pass


class InvalidCommandArgs(Exception):
    pass


class WrapperFailure(Exception):
    pass


class ConnectionFailure(Exception):
    pass
