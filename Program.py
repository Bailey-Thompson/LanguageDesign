# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER, PLUS, EOF, MINUS, MUL, DIV, LPAREN, RPAREN = 'INTEGER', 'PLUS', 'EOF', 'MINUS', 'MUL', 'DIV', 'LPAREN', 'RPAREN'


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
    def __init__(self, text):
        # client string input, e.g. "3+5"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        # current token instance
        self.current_token = self.get_next_token()

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        text = self.text

        while self.pos < len(text) and text[self.pos].isspace():
            self.pos += 1  # skip whitespace

        # is self.pos index past the end of the self.text ?
        # if so, then return EOF token because there is no more
        # input left to convert into tokens
        if self.pos > len(text) - 1:
            return Token(EOF, None)

        # get a character at the position self.pos and decide
        # what token to create based on the single character
        current_char = text[self.pos]

        # if the character is a digit then convert it to
        # integer, create an INTEGER token, increment self.pos
        # index to point to the next character after the digit,
        # and return the INTEGER token
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

        self.error()

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
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def factor(self):
        """factor : (MINUS)? (INTEGER | LPAREN expr RPAREN)"""
        token = self.current_token

        if token.type == MINUS:
            self.eat(MINUS)
            return -self.factor()

        if token.type == INTEGER:
            self.eat(INTEGER)
            return token.value
        elif token.type == LPAREN:
            self.eat(LPAREN)
            result = self.expr()
            self.eat(RPAREN)
            return result
        else:
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
                result += self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                result -= self.term()
        return result


def main():
    import sys

    if len(sys.argv) == 2:
        file_path = sys.argv[1]
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    interpreter = Interpreter(line)
                    result = interpreter.expr()
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
            interpreter = Interpreter(text)
            result = interpreter.expr()
            print(result)


if __name__ == '__main__':
    main()