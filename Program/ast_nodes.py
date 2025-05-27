class AST:
    pass

class Block(AST):
    def __init__(self, statements):
        self.statements = statements

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class UnaryOp(AST):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

class Num(AST):
    def __init__(self, value):
        self.value = value

class Bool(AST):
    def __init__(self, value):
        self.value = value

class Str(AST):
    def __init__(self, value):
        self.value = value

class Var(AST):
    def __init__(self, name):
        self.name = name

class Assign(AST):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

class Delete(AST):
    def __init__(self, name):
        self.name = name

class Print(AST):
    def __init__(self, expr):
        self.expr = expr

class Input(AST):
    def __init__(self, var_name):
        self.var_name = var_name

class If(AST):
    def __init__(self, cond, then_expr, else_expr):
        self.cond = cond
        self.then_expr = then_expr
        self.else_expr = else_expr

class While(AST):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body
