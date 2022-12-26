import Commands.commands
from Commands.commands import Command
from firecode_script_sys import def_variable_list, get_command
import Token.token
from Token import token as tok
from Errors.errors import *


class Parser:
    def __init__(self, token_list: list[Token.token.Token], code_mode: Command, step, tokens_space, else_controller: list, while_controller: list, line):
        self.token_list = token_list
        self.ind = -1
        self.tokens_space = tokens_space
        self.line = line
        self.code_mode = code_mode
        self.cur_token = None
        self.step = step
        self.else_controller = else_controller
        self.while_controller = while_controller
        self.next()

    def next(self):
        self.ind += 1
        if self.ind + 1 > len(self.token_list):
            self.cur_token = None
        else:
            self.cur_token = self.token_list[self.ind]

    def restart(self):
        self.ind = -1
        self.cur_token = None
        self.next()

    def get_parens(self):
        get_mode = False
        count = 0
        start_ind = None
        end_ind = None
        while self.cur_token is not None:
            if self.cur_token.tok_type == tok.LPAREN:
                count += 1
            if self.cur_token.tok_type == tok.RPAREN:
                count -= 1

            if count == 1 and get_mode is False:
                get_mode = True
                start_ind = self.ind
            elif count < 0:
                return WrongParenError("Wrong paren.")
            elif count == 0 and get_mode is True:
                get_mode = False
                end_ind = self.ind
                com: Command = None
                is_null_parens = end_ind - start_ind == 1
                list_copy = self.token_list[start_ind + 1: end_ind]
                if self.token_list[start_ind - 1].tok_type == tok.TAG:
                    com, err = get_command(self.token_list[start_ind - 1].value)
                    start_ind -= 1
                    if err is not None:
                        return err
                value, err, asd, asdasdasd, asdasdasd, asda = Parser(list_copy, com, 0, 0, [], [], 1).parse()
                if is_null_parens:
                    com.set_param([])
                    value = com
                if err is not None:
                    return err
                if value.tok_type == 'unvoid':
                    value = value.run()
                for i in range(end_ind - start_ind + 1):
                    self.token_list.pop(start_ind)
                self.token_list.insert(start_ind, value)
                get_mode = False
                count = 0
                start_ind = None
                end_ind = None
                self.restart()

            self.next()

        self.restart()

        if count > 0:
            return WrongParenError("Wrong paren.")

        return None

    def get_equal(self):
        self.restart()
        while self.cur_token is not None:
            if self.cur_token.tok_type == tok.EQUAL:
                if def_variable_list.get_variable(self.token_list[self.ind - 1].value) is None:
                    val, err, asd, asdasd, asdasda, jhi = Parser(self.token_list[2:len(self.token_list)], None, 0, 0, [], [], 1).parse()
                    def_variable_list.add_variable(self.token_list[self.ind - 1].value, val)
                    self.token_list = []
                else:
                    val, err, asd, asdasd, ass, asdasa = Parser(self.token_list[2:len(self.token_list)], None, 0, 0, [], [], 1).parse()
                    def_variable_list.change_variable_value(self.token_list[self.ind - 1].value, val)
                    self.token_list = []

                self.token_list = [tok.Token([], tok.PARAM)]
                self.code_mode = Commands.commands.NullCom('', '', 1)
                break

            self.next()

    def change_vars_value(self):
        self.restart()
        while self.cur_token is not None:
            if self.cur_token.tok_type == tok.TAG:
                if def_variable_list.get_variable(self.cur_token.value) is not None:
                    self.token_list[self.ind] = def_variable_list.get_variable(self.cur_token.value)
                    self.restart()
                    self.ind = -1
            self.next()

    def get_value_of_operation(self):
        thstoken = None
        if self.token_list[self.ind - 1].tok_type != self.token_list[self.ind + 1].tok_type:
            return WrongOperatorError("Wrong operator.")
        if self.cur_token.tok_type == tok.MULTIPLY:
            value = self.token_list[self.ind - 1].value * self.token_list[self.ind + 1].value
            thstoken = Token.token.Token(value, self.token_list[self.ind - 1].tok_type)
        elif self.cur_token.tok_type == tok.DIVIDE:
            value = self.token_list[self.ind - 1].value / self.token_list[self.ind + 1].value
            thstoken = Token.token.Token(value, tok.FLOAT)
        elif self.cur_token.tok_type == tok.PLUS:
            value = self.token_list[self.ind - 1].value + self.token_list[self.ind + 1].value
            thstoken = Token.token.Token(value, self.token_list[self.ind - 1].tok_type)
        elif self.cur_token.tok_type == tok.MINUS:
            value = self.token_list[self.ind - 1].value - self.token_list[self.ind + 1].value
            thstoken = Token.token.Token(value, self.token_list[self.ind - 1].tok_type)
        elif self.cur_token.tok_type == tok.SMALL:
            value = self.token_list[self.ind - 1].value < self.token_list[self.ind + 1].value
            thstoken = Token.token.Token(value, tok.BOOL)
        elif self.cur_token.tok_type == tok.BIG:
            value = self.token_list[self.ind - 1].value > self.token_list[self.ind + 1].value
            thstoken = Token.token.Token(value, tok.BOOL)
        elif self.cur_token.tok_type == tok.TAG and self.cur_token.value == 'is':
            value = self.token_list[self.ind - 1].value == self.token_list[self.ind + 1].value
            thstoken = Token.token.Token(value, tok.BOOL)
        elif self.cur_token.tok_type == tok.TAG and self.cur_token.value == 'isnot':
            value = self.token_list[self.ind - 1].value != self.token_list[self.ind + 1].value
            thstoken = Token.token.Token(value, tok.BOOL)
        elif self.cur_token.tok_type == tok.TAG and self.cur_token.value == 'and':
            value = self.token_list[self.ind - 1].value and self.token_list[self.ind + 1].value
            thstoken = Token.token.Token(value, tok.BOOL)
        elif self.cur_token.tok_type == tok.TAG and self.cur_token.value == 'or':
            value = self.token_list[self.ind - 1].value or self.token_list[self.ind + 1].value
            thstoken = Token.token.Token(value, tok.BOOL)

        for a in range(3):
            self.token_list.pop(self.ind - 1)
        self.token_list.insert(self.ind - 1, thstoken)

    def solve_operations(self):
        self.restart()
        while self.cur_token is not None:
            if self.cur_token.tok_type in [tok.MULTIPLY, tok.DIVIDE]:
                err = self.get_value_of_operation()
                if err is not None:
                    return err

                self.restart()
                self.ind = -1
            self.next()

        self.restart()

        while self.cur_token is not None:
            if self.cur_token.tok_type in [tok.PLUS, tok.MINUS]:
                err = self.get_value_of_operation()
                if err is not None:
                    return err

                self.restart()
                self.ind = -1
            self.next()

        self.restart()

        while self.cur_token is not None:
            if self.cur_token.tok_type == tok.TAG and self.cur_token.value == 'is':
                err = self.get_value_of_operation()
                if err is not None:
                    return err

            if self.cur_token.tok_type == tok.TAG and self.cur_token.value == 'isnot':
                err = self.get_value_of_operation()
                if err is not None:
                    return err

                self.restart()
                self.ind = -1
            self.next()

        self.restart()

        while self.cur_token is not None:
            if (self.cur_token.tok_type == tok.TAG and self.cur_token.value == 'and') or (self.cur_token.tok_type == tok.TAG and self.cur_token.value == 'or'):
                err = self.get_value_of_operation()
                if err is not None:
                    return err

                self.restart()
                self.ind = -1
            self.next()

        self.restart()

        while self.cur_token is not None:
            if self.cur_token.tok_type in [tok.BIG, tok.SMALL]:
                err = self.get_value_of_operation()
                if err is not None:
                    return err

                self.restart()
                self.ind = -1
            self.next()

    def find_if(self):
        self.restart()
        while self.cur_token is not None:
            if self.cur_token.tok_type == tok.TAG and self.cur_token.value == 'if':
                if self.ind != 0:
                    pass
                if self.token_list[1].value:
                    self.step += 1
                self.else_controller.append(self.token_list[1])
                self.code_mode = Commands.commands.NullCom('', '', 0)
                self.code_mode.set_param([])
            elif self.cur_token.tok_type == tok.TAG and self.cur_token.value == 'endif':
                if self.ind != 0:
                    pass
                if self.step < 0:
                    pass
                self.else_controller.pop(len(self.else_controller) - 1)
                self.code_mode = Commands.commands.NullCom('', '', 0)
                self.code_mode.set_param([])
            elif self.cur_token.tok_type == tok.TAG and self.cur_token.value == 'else':
                if self.ind != 0:
                    pass
                if self.else_controller[len(self.else_controller) - 1].value is False:
                    self.step += 1

                self.code_mode = Commands.commands.NullCom('', '', 0)
                self.code_mode.set_param([])
            self.next()

    def find_while(self):
        self.restart()
        while self.cur_token is not None:
            if self.cur_token.tok_type == tok.TAG and self.cur_token.value == 'while':
                if self.ind != 0:
                    pass
                if self.token_list[1].value:
                    self.step += 1
                    self.while_controller.append([self.line, True])
                else:
                    self.while_controller.append([self.line, False])
                self.code_mode = Commands.commands.NullCom('', '', 0)
                self.code_mode.set_param([])
            elif self.cur_token.tok_type == tok.TAG and self.cur_token.value == 'endwhile':
                if self.ind != 0:
                    pass
                if self.step < 0:
                    pass
                if self.while_controller[len(self.while_controller) - 1][1] is True:
                    self.line = self.while_controller[len(self.while_controller) - 1][0] - 1
                self.step = self.tokens_space
                self.while_controller.pop(len(self.while_controller) - 1)
                self.code_mode = Commands.commands.NullCom('', '', 0)
                self.code_mode.set_param([])
            self.next()

    def get_param(self):
        self.restart()
        while self.cur_token is not None:
            if self.cur_token.tok_type == tok.COM:
                if self.token_list[self.ind - 1].tok_type == tok.PARAM:
                    value = tok.Token(self.token_list[self.ind - 1].value + [self.token_list[self.ind + 1]], tok.PARAM)
                    for a in range(3):
                        self.token_list.pop(self.ind - 1)
                    self.token_list.insert(self.ind - 1, value)
                else:
                    value = tok.Token([self.token_list[self.ind - 1], self.token_list[self.ind + 1]], tok.PARAM)
                    for a in range(3):
                        self.token_list.pop(self.ind - 1)
                    self.token_list.insert(self.ind - 1, value)

                self.restart()
            self.next()

    def connect(self):
        if self.token_list[0].tok_type == tok.PARAM:
            self.code_mode.set_param(self.token_list[0].value)
            self.token_list = [self.code_mode]
        else:
            self.code_mode.set_param([self.token_list[0]])
            self.token_list = [self.code_mode]

    def parse(self):
        if len(self.token_list) == 0:
            self.code_mode = Commands.commands.NullCom('', '', 0)
            self.code_mode.set_param([])
            return self.code_mode, None, self.step, self.else_controller, self.while_controller, self.line
        else:
            if self.token_list[0].value == 'endif' or self.token_list[0].value == 'else' or self.token_list[0].value == 'endwhile':
                if self.step - self.tokens_space <= 1 and self.step >= self.tokens_space:
                    self.step = self.tokens_space
            if self.tokens_space != self.step:
                self.code_mode = Commands.commands.NullCom('', '', 0)
                self.code_mode.set_param([])
                return self.code_mode, None, self.step, self.else_controller, self.while_controller, self.line
            self.get_equal()
            self.change_vars_value()
            err = self.get_parens()
            if err is not None:
                return None, err, self.step, self.else_controller, self.while_controller, self.line
            err = self.get_parens()
            if err is not None:
                return None, err, self.step, self.else_controller, self.while_controller, self.line
            err = self.solve_operations()
            if err is not None:
                return None, err, self.step, self.else_controller, self.while_controller, self.line
            self.find_if()
            self.find_while()
            if self.code_mode is None:
                return self.token_list[0], None, self.step, self.else_controller, self.while_controller, self.line
            else:
                self.get_param()
                self.connect()
                return self.code_mode, None, self.step, self.else_controller, self.while_controller, self.line
