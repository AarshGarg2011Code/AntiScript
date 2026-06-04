# main.py

import sys

from lexer import Lexer
from parser import Parser
from runtime import Runtime
from interpreter import Interpreter


def run_file(filename):

    with open(
        filename,
        "r",
        encoding="utf-8"
    ) as f:
        source = f.read()

    lexer = Lexer(source)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    ast = parser.parse()

    runtime = Runtime()

    interpreter = Interpreter(runtime)

    interpreter.run(ast)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print(
            "Usage: python main.py program.anti"
        )
        sys.exit(1)

    try:

        run_file(sys.argv[1])

    except Exception as e:

        print(e)
        
    pause = str(input("Press any key to continue . . . . ."))