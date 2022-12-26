import Errors.errors
from Interpreter.variable import VariableList
from Lexer.lexer import Lexer
from Parser.parser import Parser


class Interpreter:
    def __init__(self, code: list):
        self.code = code
        self.ind = -1
        self.cur_line = None
        self.step = 0
        self.else_controller = []
        self.while_controller = []
        self.variables = VariableList([])
        self.next()

    def set_codes(self, codes):
        self.code = codes
        self.ind = -1
        self.cur_line = None
        self.next()

    def next(self):
        self.ind += 1
        if self.ind + 1 > len(self.code):
            self.cur_line = None
        else:
            self.cur_line = self.code[self.ind]

    def run(self):
        while self.cur_line is not None:
            space_count = 0
            for i in self.cur_line:
                if i != ' ':
                    break
                space_count += 1

            if space_count % 3 != 0:
                Errors.errors.WrongSpaceError("Wrong spaces.").error()
                exit()

            space_count /= 3

            def_lexer = Lexer(self.cur_line)
            tokens, error = def_lexer.lex()
            if error is not None:
                error.error()
                exit()

            def_parser = Parser(tokens, None, self.step, space_count, self.else_controller, self.while_controller,
                                self.ind)
            code, error, step, else_conroller, whl, ln = def_parser.parse()
            self.else_controller = else_conroller
            self.while_controller = whl
            self.ind = ln
            self.step = step
            if error is not None:
                error.error()
                exit()
            code.run()
            self.next()

        exit()
