from parser import Parser
from interpreter import Interpreter
import sys

def run(text, interpreter):
    parser = Parser(text)
    ast = parser.program()  # parse all statements
    return interpreter.visit(ast)

def main():
    global_vars = {}
    interpreter = Interpreter(global_vars)

    if len(sys.argv) == 2:
        file_path = sys.argv[1]
        with open(file_path, 'r') as f:
            text = f.read()  # read whole file at once
        result = run(text, interpreter)
        if result is not None:
            print(result)
    else:
        while True:
            try:
                text = input('calc> ')
            except EOFError:
                break
            if not text.strip():
                continue
            result = run(text, interpreter)
            if result is not None:
                print(result)

if __name__ == '__main__':
    main()
