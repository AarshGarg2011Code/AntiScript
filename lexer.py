# lexer.py

from dataclasses import dataclass


@dataclass
class Token:
    type: str
    value: str
    line: int


KEYWORDS = {
    "yell": "YELL",
    "maybe": "IF",
    "otherwise": "ELSE",
    "repeat": "REPEAT",
    "times": "TIMES_KW",
    "as": "AS",
    "long": "LONG",
    "done": "DONE",
    "with": "WITH",
    "that": "THAT",
    "the": "THE",
    "thing": "THING",
    "called": "CALLED",
    "which": "WHICH",
    "needs": "NEEDS",
    "give": "GIVE",
    "back": "BACK",
    "borrow": "BORROW",
    "absolutely": "TRUE",
    "nope": "FALSE",
    "and": "AND",
    "or": "OR",
    "not": "NOT",
    "is": "ASSIGN",
    "from": "FROM",
    "all": "ALL",
    "thats": "THATS",
    "it": "IT",
    "ask": "ASK",
    "text": "TEXT_TYPE",
    "number": "NUMBER_TYPE",
    "decimal": "DECIMAL_TYPE",
    "truth": "TRUTH_TYPE",
}

WORD_OPERATORS = {
    "plus": "+",
    "minus": "-",
    "multiply": "*",
    "divide": "/",
    "equals": "==",
    "notequals": "!=",
    "greaterthan": ">",
    "lessthan": "<",
    "lessthaneq": "<=",
    "greaterthaneq": ">=",
}


class Lexer:

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.line = 1

    def current(self):
        if self.pos >= len(self.text):
            return None

        return self.text[self.pos]

    def advance(self):
        if self.current() == "\n":
            self.line += 1

        self.pos += 1

    def collect_number(self):
        result = ""
        dot_count = 0

        while self.current() and (
            self.current().isdigit()
            or self.current() == "."
        ):
            if self.current() == ".":
                dot_count += 1

            result += self.current()
            self.advance()

        if dot_count == 0:
            return Token("INTEGER", result, self.line)

        return Token("FLOAT", result, self.line)

    def collect_identifier(self):
        result = ""

        while self.current() and (
            self.current().isalnum()
            or self.current() == "_"
        ):
            result += self.current()
            self.advance()

        if result in WORD_OPERATORS:
            return Token(
                "OPERATOR",
                WORD_OPERATORS[result],
                self.line
            )

        if result in KEYWORDS:
            return Token(
                KEYWORDS[result],
                result,
                self.line
            )

        return Token(
            "IDENTIFIER",
            result,
            self.line
        )

    def collect_string(self):
        self.advance()

        result = ""

        while self.current() and self.current() != '"':
            result += self.current()
            self.advance()

        if self.current() != '"':
            raise SyntaxError(
                f"Unterminated string at line {self.line}"
            )

        self.advance()

        return Token(
            "STRING",
            result,
            self.line
        )

    def tokenize(self):

        tokens = []

        while self.current():

            char = self.current()
            
            if char == "#":

                while (
                    self.current() is not None
                    and self.current() != "\n"
                ):
                    self.advance()

                continue

            if char in " \t\r":
                self.advance()
                continue

            if char == "\n":
                tokens.append(
                    Token("NEWLINE", "\\n", self.line)
                )
                self.advance()
                continue

            if char.isdigit():
                tokens.append(
                    self.collect_number()
                )
                continue

            if char.isalpha() or char == "_":
                tokens.append(
                    self.collect_identifier()
                )
                continue

            if char == '"':
                tokens.append(
                    self.collect_string()
                )
                continue

            if char == "=":
                self.advance()

                if self.current() == "=":
                    self.advance()
                    tokens.append(
                        Token("OPERATOR", "==", self.line)
                    )
                else:
                    tokens.append(
                        Token("ASSIGN", "=", self.line)
                    )

                continue

            if char == "!":
                self.advance()

                if self.current() == "=":
                    self.advance()
                    tokens.append(
                        Token("OPERATOR", "!=", self.line)
                    )
                    continue

                raise SyntaxError(
                    f"Unexpected ! at line {self.line}"
                )

            if char in "+-*/<>":
                tokens.append(
                    Token(
                        "OPERATOR",
                        char,
                        self.line
                    )
                )
                self.advance()
                continue

            if char == "(":
                tokens.append(
                    Token("LPAREN", "(", self.line)
                )
                self.advance()
                continue

            if char == ")":
                tokens.append(
                    Token("RPAREN", ")", self.line)
                )
                self.advance()
                continue

            if char == "[":
                tokens.append(
                    Token("LBRACKET", "[", self.line)
                )
                self.advance()
                continue

            if char == "]":
                tokens.append(
                    Token("RBRACKET", "]", self.line)
                )
                self.advance()
                continue

            if char == ",":
                tokens.append(
                    Token("COMMA", ",", self.line)
                )
                self.advance()
                continue
            
            if char == ".":
                tokens.append(
                    Token("DOT", ".", self.line)
                )
                self.advance()
                continue

            raise SyntaxError(
                f"Unexpected character '{char}' at line {self.line}"
            )

        tokens.append(
            Token("EOF", "", self.line)
        )

        return tokens