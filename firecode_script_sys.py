from Commands.commands import *
from Interpreter.variable import VariableList

commands: list[Command] = [
        PrintCom('print', 'void', 'optimize'),
        InpCom('input', 'unvoid', 1),
        ExitCom('exit', 'void', 0),
        WaitInpCom('wait_input', 'void', 0),
        ToStrCom('to_string', 'unvoid', 1),
        ToIntCom('to_int', 'unvoid', 1)
    ]


def get_command(arg):
    for command in commands:
        if command.get_arg() == arg:
            return command, None

    return None, Errors.errors.CommandNotFoundError(f"'{arg}' not found.")


def_variable_list = VariableList([])
