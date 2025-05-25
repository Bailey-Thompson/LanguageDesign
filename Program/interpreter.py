# interpreter.py
from lexer import Lexer
from tokens import (
    Token, INTEGER, PLUS, EOF, MINUS, MUL, DIV, LPAREN, RPAREN,
    TRUE, FALSE, AND, OR, NOT, LT, GT, LE, GE, EQ, NEQ,
    STRING, IDENTIFIER, ASSIGN
)

class Interpreter(object):
    def __init__(self, text, global_vars=None):
        self.lexer = Lexer(text)
        self.current_token = self.lexer.get_next_token()
        self.global_vars = global_vars if global_vars is not None else {}

    def error(self):
        raise Exception('Error parsing input')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            # print(f"Eating token: {self.current_token}")
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    # Factor, term, expr, logical_or, logical_and, equality, comparison, statement
    # ... [Same as your current methods] ...

    def factor(self):
        token = self.current_token

        if token.type == NOT:
            self.eat(NOT)
            return not self.factor()

        if token.type == MINUS:
            self.eat(MINUS)
            return -self.factor()

        if token.type == INTEGER:
            self.eat(INTEGER)
            return token.value

        if token.type == TRUE:
            self.eat(TRUE)
            return True

        if token.type == FALSE:
            self.eat(FALSE)
            return False

        if token.type == LPAREN:
            self.eat(LPAREN)
            result = self.logical_or()
            self.eat(RPAREN)
            return result

        if token.type == STRING:
            self.eat(STRING)
            return token.value

        if token.type == IDENTIFIER:
            var_name = token.value
            self.eat(IDENTIFIER)
            if var_name in self.global_vars:
                return self.global_vars[var_name]
            else:
                raise Exception(f"Undefined variable '{var_name}'")

        self.error()

    def term(self):
        result = self.factor()
        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
                result *= self.factor()
            elif token.type == DIV:
                self.eat(DIV)
                divisor = self.factor()
                if divisor == 0:
                    raise Exception('Division by zero')
                result /= divisor
        return result

    def expr(self):
        result = self.term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                right = self.term()
                if isinstance(result, str) and isinstance(right, str):
                    result = result + right
                elif isinstance(result, (int, float)) and isinstance(right, (int, float)):
                    result = result + right
                else:
                    raise Exception(f"Type error: cannot add {type(result).__name__} and {type(right).__name__}")
            elif token.type == MINUS:
                self.eat(MINUS)
                right = self.term()
                if isinstance(result, (int, float)) and isinstance(right, (int, float)):
                    result = result - right
                else:
                    raise Exception(f"Type error: cannot subtract {type(result).__name__} and {type(right).__name__}")
        return result

    def logical_or(self):
        result = self.logical_and()
        while self.current_token.type == OR:
            self.eat(OR)
            result = result or self.logical_and()
        return result

    def logical_and(self):
        result = self.equality()
        while self.current_token.type == AND:
            self.eat(AND)
            result = result and self.equality()
        return result

    def equality(self):
        result = self.comparison()
        while self.current_token.type in (EQ, NEQ):
            token = self.current_token
            if token.type == EQ:
                self.eat(EQ)
                result = (result == self.comparison())
            elif token.type == NEQ:
                self.eat(NEQ)
                result = (result != self.comparison())
        return result

    def comparison(self):
        result = self.expr()
        while self.current_token.type in (LT, GT, LE, GE):
            token = self.current_token
            if token.type == LT:
                self.eat(LT)
                result = (result < self.term())
            elif token.type == LE:
                self.eat(LE)
                result = (result <= self.term())
            elif token.type == GT:
                self.eat(GT)
                result = (result > self.term())
            elif token.type == GE:
                self.eat(GE)
                result = (result >= self.term())
        return result

    def statement(self):
        if self.current_token.type == IDENTIFIER and self.current_token.value == "print":
            self.eat(IDENTIFIER)
            expr_val = self.logical_or()
            print(expr_val)
            return expr_val

        if self.current_token.type == IDENTIFIER:
            var_name = self.current_token.value
            saved_pos = self.lexer.pos
            saved_token = self.current_token

            self.eat(IDENTIFIER)
            if self.current_token.type == ASSIGN:
                self.eat(ASSIGN)
                expr_val = self.logical_or()
                self.global_vars[var_name] = expr_val
                return expr_val
            else:
                self.lexer.pos = saved_pos
                self.current_token = saved_token

        return self.logical_or()
