from lexer import Lexer
from parser import Parser
with open(
    "hello.anti",
    "r",
    encoding="utf-8"
) as f:
    source = f.read()
lexer = Lexer(source)
tokens = lexer.tokenize()

for t in tokens:
    print(t)

parser = Parser(tokens)

ast = parser.parse()
print(ast)