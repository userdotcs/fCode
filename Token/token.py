INT = 'INT'
FLOAT = 'FLT'
STR = 'STR'
BOOL = 'BOOL'
TAG = 'TAG'
PLUS = 'PLS'
MINUS = 'MIN'
MULTIPLY = 'MUL'
DIVIDE = 'DIV'
LPAREN = 'LPR'
RPAREN = 'RPR'
PARAM = 'PAR'
COM = 'COM'
EQUAL = 'EQL'
SMALL = 'SML'
BIG = 'BIG'
COMMENT = 'COMMENT'


class Token:
    def __init__(self, value, tok_type):
        self.value = value
        self.tok_type = tok_type

    def run(self):
        print(self.value)
