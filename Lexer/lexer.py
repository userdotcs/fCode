from Token import token
from Errors.errors import *


digits = '0123456789'
letters = 'qwertyuıopğüasdfghjklşizxcvbnmöçQWERTYUIOPĞÜASDFGHJKLŞİZXCVBNMÖÇ_'


def ret_token(tok_text):
    tok_text = str(tok_text)
    is_str = False
    for let in tok_text:
        if let in letters:
            is_str = True
        else:
            is_str = False
            break
    if tok_text.startswith('"') and tok_text.endswith('"'):
        return token.Token(tok_text[1:len(tok_text) - 1], token.STR)
    elif is_str:
        if tok_text == 'true':
            return token.Token(True, token.BOOL)
        elif tok_text == 'false':
            return token.Token(False, token.BOOL)
        return token.Token(str(tok_text), token.TAG)
    elif tok_text.count('.') > 0:
        return token.Token(float(tok_text), token.FLOAT)
    elif tok_text.count('.') == 0:
        return token.Token(int(tok_text), token.INT)


class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.spaces = 0

    def lex(self):
        cur = ''
        dot = 0
        in_clips = False
        tokens = []
        for char in self.text:
            if in_clips:
                if char == '"':
                    cur += char
                    tokens.append(ret_token(cur))
                    in_clips = False
                    cur = ''
                else:
                    cur += char
            else:
                if char == '"':
                    if cur != '':
                        tokens.append(ret_token(cur))
                        dot = 0
                    cur = '"'
                    in_clips = True
                elif char in digits:
                    cur += char
                elif char == '.':
                    dot += 1
                    cur += char
                    if dot > 1:
                        return None, WrongFloatError("Float is wrong.")
                elif char == ']':
                    tokens.append(token.Token(char, token.COMMENT))
                elif char == ' ':
                    if cur != '':
                        tokens.append(ret_token(cur))
                        cur = ''
                        dot = 0
                elif char in '+-*/=><':
                    if cur != '':
                        tokens.append(ret_token(cur))
                        cur = ''
                        dot = 0

                    if char == '+':
                        tokens.append(token.Token(char, token.PLUS))
                    elif char == '-':
                        tokens.append(token.Token(char, token.MINUS))
                    elif char == '*':
                        tokens.append(token.Token(char, token.MULTIPLY))
                    elif char == '/':
                        tokens.append(token.Token(char, token.DIVIDE))
                    elif char == '=':
                        tokens.append(token.Token(char, token.EQUAL))
                    elif char == '<':
                        tokens.append(token.Token(char, token.SMALL))
                    elif char == '>':
                        tokens.append(token.Token(char, token.BIG))
                elif char == ',':
                    if cur != '':
                        tokens.append(ret_token(cur))
                        cur = ''
                        dot = 0

                    tokens.append(token.Token(char, token.COM))
                elif char in '()':
                    if cur != '':
                        tokens.append(ret_token(cur))
                        cur = ''
                        dot = 0

                    if char == '(':
                        tokens.append(token.Token(char, token.LPAREN))
                    elif char == ')':
                        tokens.append(token.Token(char, token.RPAREN))
                elif char in letters:
                    cur += char
                else:
                    return None, WrongCharError(char)
        if cur != '':
            tokens.append(ret_token(cur))
            cur = ''
            dot = 0

        return tokens, None
