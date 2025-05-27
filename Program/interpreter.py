# Imports token type, lexer and AST node classes
from tokens import *
from lexer import Lexer
from ast_nodes import *

class Interpreter:
    def __init__(self, global_vars=None):
        # Initializes interpreter with the globabl variables
        self.global_vars = global_vars if global_vars is not None else {}

    def visit(self, node):
        # Dispatch method to call appropriate method
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        # Called if no specific visit_method exists
        raise Exception(f"No visit_{type(node).__name__} method")

    def visit_Num(self, node):
        # Returns numeric value
        return node.value

    def visit_Bool(self, node):
        # Returns the boolean value
        return node.value

    def visit_Str(self, node):
        # Returns the string value
        return node.value

    def visit_Var(self, node): 
        # Looks for variable in dictionary
        if node.name in self.global_vars:
            return self.global_vars[node.name]
        # Raises exception if variable doesn't exist
        raise Exception(f"Undefined variable '{node.name}'")

    def visit_Assign(self, node):
        # Evaluates right hand side expression
        val = self.visit(node.expr)
        # Assigns the value to the variable in the dictionary
        self.global_vars[node.name] = val
        return val

    def visit_Delete(self, node):
        # Remove variable from dictionary if it exists
        if node.name in self.global_vars:
            del self.global_vars[node.name]
        return None

    def visit_BinOp(self, node):
        # Evaluates left and right
        left = self.visit(node.left)
        right = self.visit(node.right)
        # Operator token type
        op_type = node.op.type 
        
        # All Binary options
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
        # Evaluates the expression to apply the unary operator
        val = self.visit(node.expr)
        # Handles NOT
        if node.op.type == NOT:
            return not val
        # Handles unary minus
        if node.op.type == MINUS:
            return -val
        raise Exception(f"Unknown unary operator {node.op.type}")

    def visit_Print(self, node):
        # Evaluates print
        val = self.visit(node.expr)
        # Output result
        print(val)

    def visit_Input(self, node):
        # Prompt the user with variable name and read input
        val = input(f"{node.var_name}> ")
        # Store the input under variable name
        self.global_vars[node.var_name] = val
        return val

    def visit_If(self, node):
        # Evaluate the condition expression
        if self.visit(node.cond):
            # If true, eavluate and return then
            return self.visit(node.then_expr)
        else:
            # Otherwise return else
            return self.visit(node.else_expr)

    def visit_While(self, node):
        # Keep executing the body while its condition is true
        while self.visit(node.cond):
            self.visit(node.body)

    def visit_Block(self, node):
        # Execute block in order
        result = None
        for stmt in node.statements:
            result = self.visit(stmt)
        # Return the final statement
        return result
