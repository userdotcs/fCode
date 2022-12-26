class Error:
    def __init__(self, msg):
        self.msg = msg

    def error(self):
        print(self.msg)


class WrongFloatError(Error):
    pass


class WrongCharError(Error):
    pass


class WrongSpaceError(Error):
    pass


class NotConvertableError(Error):
    pass


class WrongVariableError(Error):
    pass


class VariableNotFoundError(Error):
    pass


class VariableContainsError(Error):
    pass


class WrongParenError(Error):
    pass


class WrongClipError(Error):
    pass


class ParamError(Error):
    pass


class CommandNotFoundError(Error):
    pass


class WrongOperatorError(Error):
    pass
