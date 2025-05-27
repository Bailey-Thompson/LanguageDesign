# tokens.py

# Define tokens used by lexer and parse
INTEGER, PLUS, EOF, MINUS, MUL, DIV, LPAREN, RPAREN = (
    'INTEGER', 'PLUS', 'EOF', 'MINUS', 'MUL', 'DIV', 'LPAREN', 'RPAREN'
)
TRUE, FALSE = 'TRUE', 'FALSE'
AND, OR, NOT = 'AND', 'OR', 'NOT'
LT, GT, LE, GE = 'LT', 'GT', 'LE', 'GE'
EQ, NEQ = 'EQ', 'NEQ'
STRING = 'STRING'
IDENTIFIER, ASSIGN = 'IDENTIFIER', 'ASSIGN'
DEL = 'DEL'
IF, THEN, ELSE, WHILE, INPUT = 'IF', 'THEN', 'ELSE', 'WHILE', 'INPUT'
LBRACE, RBRACE = 'LBRACE', 'RBRACE'

class Token(object):
    def __init__(self, type, value):
        # Initialize a token with type and optional value
        self.type = type
        self.value = value

    def __str__(self):
        # Return a string of token for debugging
        return f'Token({self.type}, {repr(self.value)})'

    def __repr__(self):
        # Return a string of token for debugging
        return self.__str__()
