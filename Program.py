# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER, PLUS, EOF, MINUS, MUL, DIV, LPAREN, RPAREN = 'INTEGER', 'PLUS', 'EOF', 'MINUS', 'MUL', 'DIV', 'LPAREN', 'RPAREN'
TRUE, FALSE = 'TRUE', 'FALSE'
AND, OR, NOT = 'AND', 'OR', 'NOT'
LT, GT, LE, GE = 'LT', 'GT', 'LE', 'GE'
EQ, NEQ = 'EQ', 'NEQ'
STRING = 'STRING'
IDENTIFIER, ASSIGN = 'IDENTIFIER', 'ASSIGN'


class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, or EOF
        self.type = type
        # token value: 0, 1, 2. 3, 4, 5, 6, 7, 8, 9, '+', or None
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS '+')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Interpreter(object):
    def __init__(self, text, global_vars):
        # client string input, e.g. "3+5"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        # current token instance
        self.current_token = self.get_next_token()

        self.global_vars = global_vars if global_vars is not None else {}

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        text = self.text

        while self.pos < len(text) and text[self.pos].isspace():
            self.pos += 1  # skip whitespace

        if self.pos > len(text) - 1:
            return Token(EOF, None)

        current_char = text[self.pos]

        if current_char.isdigit():
            return self.number()

        if current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token
        
        if current_char == '-':
            token = Token(MINUS, current_char)
            self.pos += 1
            return Token(MINUS, '-')
        
        if current_char == '*':
            token = Token(MUL, current_char)
            self.pos += 1
            return Token(MUL, '*')
        
        if current_char == '/':
            token = Token(DIV, current_char)
            self.pos += 1
            return Token(DIV, '/')
        
        if current_char == '(':
            token = Token(LPAREN, current_char)
            self.pos += 1
            return Token(LPAREN, '(')
        
        if current_char == ')':
            token = Token(RPAREN, current_char)
            self.pos += 1
            return Token(RPAREN, ')')
        
        if current_char == '=':
            self.pos += 1
            return Token(ASSIGN, '=')
        
        if self.pos + 1 < len(text):
            two_char = text[self.pos:self.pos+2]
            if two_char == '==':
                self.pos += 2
                return Token(EQ, '==')
            elif two_char == '!=':
                self.pos += 2
                return Token(NEQ, '!=')
            elif two_char == '<=':
                self.pos += 2
                return Token(LE, '<=')
            elif two_char == '>=':
                self.pos += 2
                return Token(GE, '>=')

        # Single character tokens
        if current_char == '<':
            self.pos += 1
            return Token(LT, '<')
        if current_char == '>':
            self.pos += 1
            return Token(GT, '>')
        if current_char == '!':
            self.pos += 1
            return Token(NOT, '!')

        # Keywords and identifiers (for true, false, and, or)
        if current_char.isalpha():
            start_pos = self.pos
            while self.pos < len(text) and (text[self.pos].isalnum() or text[self.pos] == '_'):
                self.pos += 1
            word = text[start_pos:self.pos].lower()
            print(f"Found word token: '{word}'")
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
            self.pos += 1
            result = ''
            while self.pos < len(text) and text[self.pos] != '"':
                if text[self.pos] == '\\':
                    self.pos += 1
                    if self.pos < len(text):
                        esc_char = text[self.pos]
                        if esc_char == 'n':
                            result += '\n'
                        if esc_char == 't':
                            result += '\t'
                        elif esc_char == 'e':
                            print("Exiting program.")
                            exit(0)
                        else:
                            result += esc_char
                else:
                    result += text[self.pos]
                self.pos += 1

            if self.pos >= len(text):
                self.error()
            self.pos += 1
            return Token(STRING, result)

    def number(self):
        result = ''
        dot_count = 0

        while self.pos < len(self.text) and (self.text[self.pos].isdigit() or self.text[self.pos] == '.'):
            if self.text[self.pos] == '.':
                dot_count += 1
                if dot_count > 1:
                    self.error()
            result += self.text[self.pos]
            self.pos += 1

        if dot_count == 0:
            return Token(INTEGER, int(result))
        else:
            return Token(INTEGER, float(result))


    def eat(self, token_type):
        if self.current_token.type == token_type:
            print(f"Eating token: {self.current_token}")
            self.current_token = self.get_next_token()
        else:
            self.error()


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

        elif token.type == LPAREN:
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
                raise Exception(f"Undefined variable '{var_name}")

        self.error()

    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
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
        """expr : term ((PLUS | MINUS) term)*"""
        result = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                right = self.term()

                if isinstance(result, str) and isinstance(right, str):
                    result = result+right
                elif isinstance(result, (int, float)) and isinstance(right, (int, float)):
                    result = result + right
                else:
                    raise Exception(f"Type error: cannot add {type(result).__name__} and {type(right).__name__}")
            elif token.type == MINUS:
                self.eat(MINUS)
                right= self.term()
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
            saved_pos = self.pos
            saved_token = self.current_token

            self.eat(IDENTIFIER)
            if self.current_token.type == ASSIGN:
                self.eat(ASSIGN)
                expr_val = self.logical_or()
                self.global_vars[var_name] = expr_val
                return expr_val
            else:
                self.pos = saved_pos
                self.current_token = saved_token

        return self.logical_or()


def main():
    import sys
    global_vars = {}

    if len(sys.argv) == 2:
        file_path = sys.argv[1]
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    interpreter = Interpreter(line, global_vars)
                    result = interpreter.statement()
                    print(result)
        except FileNotFoundError:
            print(f"File not found: {file_path}")

    else:

        while True:
            try:
                # To run under Python3 replace 'raw_input' call
                # with 'input'
                text = input('calc> ')
            except EOFError:
                break
            if not text:
                continue
            interpreter = Interpreter(text, global_vars)
            result = interpreter.statement()
            print(result)


if __name__ == '__main__':
    main()