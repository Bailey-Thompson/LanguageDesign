from parser import Parser
from interpreter import Interpreter
import sys

# Runs the program
def run(text, interpreter):
    parser = Parser(text) # Create a parset instance
    ast = parser.program()  # parse all statements into an AST
    return interpreter.visit(ast) #Interpret AST

def main():
    global_vars = {} # Dictionary holds variables
    interpreter = Interpreter(global_vars) # Create interpreter with variable
    
    # Checks if file path is provided as a command line argument
    if len(sys.argv) == 2:
        file_path = sys.argv[1] # Gets fle path
        with open(file_path, 'r') as f:
            text = f.read()  # Reads file
        result = run(text, interpreter) # Parse and run the file
        if result is not None:
            print(result) # Print any results
    else:
        while True:
            try:
                text = input('input> ') # Prompt user for input
            except EOFError:
                break # Exit loop on EOF
            if not text.strip():
                continue # Ignore empty lines
            result = run(text, interpreter) # Parse and run user input
            if result is not None:
                print(result) # Print any results

# Entry point: run main()
if __name__ == '__main__':
    main()
