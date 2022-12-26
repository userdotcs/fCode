import Errors.errors
import Token.token
from Token.token import Token as _Tok


class Command:
    def __init__(self, arg, com_type, len):
        self.arg = arg
        self.tok_type = com_type
        self.param_length = len
        self.parameters = []

    def set_param(self, param):
        self.parameters = param

    def run(self):
        pass

    def control(self):
        if len(self.parameters) != self.param_length and self.param_length != 'optimize':
            Errors.errors.ParamError("Wrong param count.").error()
            exit()

    def get_arg(self):
        return self.arg


class PrintCom(Command):
    def run(self):
        self.control()
        cur = ''
        for param in self.parameters:
            cur += str(param.value)
        print(cur)


class InpCom(Command):
    def run(self):
        self.control()
        arg = input(self.parameters[0].value)
        return _Tok(arg, Token.token.STR)


class ExitCom(Command):
    def run(self):
        self.control()
        exit()


class WaitInpCom(Command):
    def run(self):
        self.control()
        input()


class ToStrCom(Command):
    def run(self):
        self.control()
        try:
            return Token.token.Token(str(self.parameters[0].value), Token.token.STR)
        except:
            Errors.errors.NotConvertableError("Not convertable.").error()
            exit()


class ToIntCom(Command):
    def run(self):
        self.control()
        try:
            return Token.token.Token(int(self.parameters[0].value), Token.token.INT)
        except:
            Errors.errors.NotConvertableError("Not convertable.").error()
            exit()


class NullCom(Command):
    pass
