from tokens import *
from lexer import Lexer
from ast_nodes import *

class Interpreter:
    def __init__(self, global_vars=None):
        self.global_vars = global_vars if global_vars is not None else {}

    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        raise Exception(f"No visit_{type(node).__name__} method")

    def visit_Num(self, node):
        return node.value

    def visit_Bool(self, node):
        return node.value

    def visit_Str(self, node):
        return node.value

    def visit_Var(self, node):
        if node.name in self.global_vars:
            return self.global_vars[node.name]
        raise Exception(f"Undefined variable '{node.name}'")

    def visit_Assign(self, node):
        val = self.visit(node.expr)
        self.global_vars[node.name] = val
        return val

    def visit_Delete(self, node):
        if node.name in self.global_vars:
            del self.global_vars[node.name]
        return None

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op_type = node.op.type

        if op_type == PLUS:
            return left + right
        if op_type == MINUS:
            return left - right
        if op_type == MUL:
            return left * right
        if op_type == DIV:
            return left / right
        if op_type == EQ:
            return left == right
        if op_type == NEQ:
            return left != right
        if op_type == LT:
            return left < right
        if op_type == GT:
            return left > right
        if op_type == LE:
            return left <= right
        if op_type == GE:
            return left >= right
        if op_type == AND:
            return left and right
        if op_type == OR:
            return left or right

        raise Exception(f"Unknown operator {op_type}")

    def visit_UnaryOp(self, node):
        val = self.visit(node.expr)
        if node.op.type == NOT:
            return not val
        if node.op.type == MINUS:
            return -val
        raise Exception(f"Unknown unary operator {node.op.type}")

    def visit_Print(self, node):
        val = self.visit(node.expr)
        print(val)

    def visit_Input(self, node):
        val = input(f"{node.var_name}> ")
        self.global_vars[node.var_name] = val
        return val

    def visit_If(self, node):
        if self.visit(node.cond):
            return self.visit(node.then_expr)
        else:
            return self.visit(node.else_expr)

    def visit_While(self, node):
        while self.visit(node.cond):
            self.visit(node.body)

    def visit_Block(self, node):
        result = None
        for stmt in node.statements:
            result = self.visit(stmt)
        return result
