from tokens import *
from lexer import Lexer
from ast_nodes import *

class Parser:
    def __init__(self, text):
        self.lexer = Lexer(text)
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception(f"Syntax error at token {self.current_token}")

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token

        if token.type == NOT:
            self.eat(NOT)
            return UnaryOp(token, self.factor())
        elif token.type == MINUS:
            self.eat(MINUS)
            return UnaryOp(token, self.factor())
        elif token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token.value)
        elif token.type == TRUE:
            self.eat(TRUE)
            return Bool(True)
        elif token.type == FALSE:
            self.eat(FALSE)
            return Bool(False)
        elif token.type == STRING:
            self.eat(STRING)
            return Str(token.value)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        elif token.type == IDENTIFIER:
            name = token.value
            self.eat(IDENTIFIER)
            return Var(name)
        elif token.type == DEL:
            self.eat(DEL)
            return Var("DEL")
        else:
            self.error()

    def term(self):
        node = self.factor()
        while self.current_token.type in (MUL, DIV):
            op = self.current_token
            self.eat(op.type)
            node = BinOp(node, op, self.factor())
        return node

    def arith_expr(self):
        node = self.term()
        while self.current_token.type in (PLUS, MINUS):
            op = self.current_token
            self.eat(op.type)
            node = BinOp(node, op, self.term())
        return node

    def comparison(self):
        node = self.arith_expr()
        while self.current_token.type in (LT, LE, GT, GE):
            op = self.current_token
            self.eat(op.type)
            node = BinOp(node, op, self.arith_expr())
        return node

    def equality(self):
        node = self.comparison()
        while self.current_token.type in (EQ, NEQ):
            op = self.current_token
            self.eat(op.type)
            node = BinOp(node, op, self.comparison())
        return node

    def logical_and(self):
        node = self.equality()
        while self.current_token.type == AND:
            op = self.current_token
            self.eat(AND)
            node = BinOp(node, op, self.equality())
        return node

    def logical_or(self):
        node = self.logical_and()
        while self.current_token.type == OR:
            op = self.current_token
            self.eat(OR)
            node = BinOp(node, op, self.logical_and())
        return node

    def expr(self):
        return self.logical_or()

    def statement(self):
        if self.current_token.type == IF:
            self.eat(IF)
            cond = self.expr()
            print("Condition parsed. Current token before THEN:", self.current_token)
            self.eat(THEN)
            then_expr = self.statement() if self.current_token.type != LBRACE else self.block()
            self.eat(ELSE)
            else_expr = self.statement() if self.current_token.type != LBRACE else self.block()
            return If(cond, then_expr, else_expr)

        elif self.current_token.type == WHILE:
            self.eat(WHILE)
            cond = self.expr()
            body = self.statement() if self.current_token.type != LBRACE else self.block()
            return While(cond, body)

        elif self.current_token.type == IDENTIFIER:
            name = self.current_token.value
            self.eat(IDENTIFIER)

            if self.current_token.type == ASSIGN:
                self.eat(ASSIGN)
                expr = self.expr()
                if isinstance(expr, Var) and expr.name == "DEL":
                    return Delete(name)
                return Assign(name, expr)

            elif name == "print":
                return Print(self.expr())

            elif name == "input":
                return Input(name)

            return Var(name)

        else:
            return self.expr()
        
    def block(self):
        statements = []
        self.eat(LBRACE)
        while self.current_token.type != RBRACE:
            statements.append(self.statement())
        self.eat(RBRACE)
        return Block(statements)
    
    def program(self):
        statements = []
        while self.current_token.type != EOF:
            statements.append(self.statement())
        return Block(statements)
