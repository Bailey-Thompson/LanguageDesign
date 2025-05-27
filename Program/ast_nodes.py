class AST:
    # Base class
    pass

class Block(AST):
    def __init__(self, statements):
        # Block = multiple statements
        self.statements = statements

class BinOp(AST):
    def __init__(self, left, op, right):
        #  Represents binary, op = operator token
        self.left = left
        self.op = op
        self.right = right

class UnaryOp(AST):
    def __init__(self, op, expr):
        # Represents unary operation
        self.op = op
        self.expr = expr

class Num(AST):
    def __init__(self, value):
        # Represents numeric value
        self.value = value

class Bool(AST):
    def __init__(self, value):
        # Represents boolean value
        self.value = value

class Str(AST):
    def __init__(self, value):
        # Represents string value
        self.value = value

class Var(AST):
    def __init__(self, name):
        # Represents variable identifier
        self.name = name

class Assign(AST):
    def __init__(self, name, expr):
        # Represents assignment statement
        self.name = name
        self.expr = expr

class Delete(AST):
    def __init__(self, name):
        # Represents delete statement, removing varialbe 
        self.name = name

class Print(AST):
    def __init__(self, expr):
        # Represents print statement
        self.expr = expr

class Input(AST):
    def __init__(self, var_name=None):
        # Represents input statement
        self.var_name = var_name

class If(AST):
    def __init__(self, cond, then_expr, else_expr):
        # Represents if statement with branches, condition, then if true, else if false
        self.cond = cond
        self.then_expr = then_expr
        self.else_expr = else_expr

class While(AST):
    def __init__(self, cond, body):
        # Represents a while loop
        self.cond = cond
        self.body = body
