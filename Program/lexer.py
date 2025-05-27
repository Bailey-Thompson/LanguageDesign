# lexer.py
from tokens import (
    Token, INTEGER, PLUS, EOF, MINUS, MUL, DIV, LPAREN, RPAREN,
    TRUE, FALSE, AND, OR, NOT, LT, GT, LE, GE, EQ, NEQ,
    STRING, IDENTIFIER, ASSIGN, DEL, IF, THEN, ELSE, WHILE, INPUT,
    LBRACE, RBRACE
)

class Lexer(object):
    def __init__(self, text):
        # Initialize the lexer with input source text
        self.text = text
        # Current position
        self.pos = 0

    def reset(self, pos):
        # Reset position to given value
        self.pos = pos

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        # Move forward one character
        self.pos += 1

    def peek(self):
        # Peek ahead without actually moving
        if self.pos + 1 >= len(self.text):
            return None
        return self.text[self.pos + 1]

    def skip_whitespace(self):
        # Sky over any whitespace
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.advance()

    def number(self):
        # Parse a numeric token
        result = ''
        # Counts decimal points to detect float or integer
        dot_count = 0
        while self.pos < len(self.text) and (self.text[self.pos].isdigit() or self.text[self.pos] == '.'):
            if self.text[self.pos] == '.':
                dot_count += 1
                # Can't have more than one decimal
                if dot_count > 1:
                    self.error()
            result += self.text[self.pos]
            self.advance()
        if dot_count == 0:
            # No decimal equals integer
            return Token(INTEGER, int(result))
        else:
            # Decimal equals float
            return Token(INTEGER, float(result))

    def get_next_token(self):
        while self.pos < len(self.text):
            current_char = self.text[self.pos]

            # Skips whitespace
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
                
            if current_char == '{':
                self.advance()
                return Token(LBRACE, '{')
            
            if current_char == '}':
                self.advance()
                return Token(RBRACE, '}')

            # Detects keywords
            if current_char.isalpha():
                start_pos = self.pos
                while (self.pos < len(self.text) and
                       (self.text[self.pos].isalnum() or self.text[self.pos] == '_')):
                    self.advance()
                # Takes full keyword
                word = self.text[start_pos:self.pos].lower()

                # Matches against saved keywords
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
                elif word == 'if':
                    return Token(IF, 'if')
                elif word == 'then':
                    return Token(THEN, 'then')
                elif word == 'else':
                    return Token(ELSE, 'else')
                elif word == 'while':
                    return Token(WHILE, 'while')
                elif word == 'input':
                    return Token(INPUT, 'input')
                elif word == "del":
                    return Token(DEL, 'del')
                else:
                    return Token(IDENTIFIER, word)

            # Detects string by speech marks
            if current_char == '"':
                self.advance()
                result = ''
                # Read characters until end
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
                                # Escape key
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

        # If no more characters, return End of Input
        return Token(EOF, None)
