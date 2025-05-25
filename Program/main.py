# main.py
from interpreter import Interpreter

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
