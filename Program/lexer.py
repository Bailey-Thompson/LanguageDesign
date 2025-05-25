# lexer.py
from tokens import (
    Token, INTEGER, PLUS, EOF, MINUS, MUL, DIV, LPAREN, RPAREN,
    TRUE, FALSE, AND, OR, NOT, LT, GT, LE, GE, EQ, NEQ,
    STRING, IDENTIFIER, ASSIGN
)

class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        self.pos += 1

    def peek(self):
        if self.pos + 1 >= len(self.text):
            return None
        return self.text[self.pos + 1]

    def skip_whitespace(self):
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.advance()

    def number(self):
        result = ''
        dot_count = 0
        while self.pos < len(self.text) and (self.text[self.pos].isdigit() or self.text[self.pos] == '.'):
            if self.text[self.pos] == '.':
                dot_count += 1
                if dot_count > 1:
                    self.error()
            result += self.text[self.pos]
            self.advance()
        if dot_count == 0:
            return Token(INTEGER, int(result))
        else:
            return Token(INTEGER, float(result))

    def get_next_token(self):
        while self.pos < len(self.text):
            current_char = self.text[self.pos]

            if current_char.isspace():
                self.skip_whitespace()
                continue

            if current_char.isdigit():
                return self.number()

            if current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if current_char == '/':
                self.advance()
                return Token(DIV, '/')

            if current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            if current_char == '=':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token(EQ, '==')
                else:
                    self.advance()
                    return Token(ASSIGN, '=')

            if current_char == '!':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token(NEQ, '!=')
                else:
                    self.advance()
                    return Token(NOT, '!')

            if current_char == '<':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token(LE, '<=')
                else:
                    self.advance()
                    return Token(LT, '<')

            if current_char == '>':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token(GE, '>=')
                else:
                    self.advance()
                    return Token(GT, '>')

            if current_char.isalpha():
                start_pos = self.pos
                while (self.pos < len(self.text) and
                       (self.text[self.pos].isalnum() or self.text[self.pos] == '_')):
                    self.advance()
                word = self.text[start_pos:self.pos].lower()
                if word == 'true':
                    return Token(TRUE, True)
                elif word == 'false':
                    return Token(FALSE, False)
                elif word == 'and':
                    return Token(AND, 'and')
                elif word == 'or':
                    return Token(OR, 'or')
                elif word == 'not':
                    return Token(NOT, 'not')
                else:
                    return Token(IDENTIFIER, word)

            if current_char == '"':
                self.advance()
                result = ''
                while self.pos < len(self.text) and self.text[self.pos] != '"':
                    if self.text[self.pos] == '\\':
                        self.advance()
                        if self.pos < len(self.text):
                            esc_char = self.text[self.pos]
                            if esc_char == 'n':
                                result += '\n'
                            elif esc_char == 't':
                                result += '\t'
                            elif esc_char == 'e':
                                print("Exiting program.")
                                exit(0)
                            else:
                                result += esc_char
                    else:
                        result += self.text[self.pos]
                    self.advance()

                if self.pos >= len(self.text):
                    self.error()
                self.advance()
                return Token(STRING, result)

            self.error()

        return Token(EOF, None)
