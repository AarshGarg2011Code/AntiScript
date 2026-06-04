# parser.py

from ast_nodes import *
class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    # =====================
    # BASIC HELPERS
    # =====================
    
    def parse_or(self):

        node = self.parse_and()

        while self.current().type == "OR":

            self.advance()

            right = self.parse_and()

            node = BinaryOpNode(
                node,
                "or",
                right
            )

        return node
        
    def parse_and(self):

        node = self.parse_comparison()

        while self.current().type == "AND":

            self.advance()

            right = self.parse_comparison()

            node = BinaryOpNode(
                node,
                "and",
                right
            )

        return node

    def current(self):
        return self.tokens[self.pos]

    def peek(self, offset=1):
        index = self.pos + offset

        if index >= len(self.tokens):
            return self.tokens[-1]

        return self.tokens[index]

    def advance(self):
        self.pos += 1

    def match(self, token_type):
        if self.current().type == token_type:
            tok = self.current()
            self.advance()
            return tok

        raise SyntaxError(
            f"Expected {token_type}, got {self.current().type}"
        )

    def skip_newlines(self):
        while self.current().type == "NEWLINE":
            self.advance()

    # =====================
    # ENTRY POINT
    # =====================

    def parse(self):
        
        statements = []

        while self.current().type != "EOF":
            self.skip_newlines()

            if self.current().type == "EOF":
                break

            stmt = self.parse_statement()

            if stmt is not None:
                statements.append(stmt)

        return ProgramNode(statements)
    # =====================
    # STATEMENTS
    # =====================

    def parse_statement(self):                
        self.skip_newlines()

        if self.current().type == "EOF":
            return None

        token = self.current()

        if token.type == "YELL":
            return self.parse_yell()

        if token.type == "BORROW":
            return self.parse_borrow()

        if token.type == "IF":
            return self.parse_if()

        if token.type == "REPEAT":
            return self.parse_repeat()
            
        if token.type == "AS":
            return self.parse_while()

        if token.type == "THE":
            return self.parse_function()

        if token.type == "GIVE":
            return self.parse_return()

        if (
            token.type == "IDENTIFIER"
            and self.peek().type == "ASSIGN"
        ):
            return self.parse_assignment()

        expr = self.parse_expression()
        return expr

    # =====================
    # YELL
    # =====================

    def parse_yell(self):

        self.match("YELL")

        expr = self.parse_expression()

        return PrintNode(expr)

    # =====================
    # BORROW
    # =====================

    def parse_borrow(self):

        self.match("BORROW")

        module = self.match(
            "IDENTIFIER"
        ).value

        return BorrowNode(module)

    # =====================
    # RETURN
    # =====================

    def parse_return(self):

        self.match("GIVE")
        self.match("BACK")

        value = self.parse_expression()

        return ReturnNode(value)

    # =====================
    # ASSIGNMENT
    # =====================

    def parse_assignment(self):

        name = self.match(
            "IDENTIFIER"
        ).value

        self.match("ASSIGN")

        value = self.parse_expression()

        return AssignmentNode(
            name=name,
            value=value
        )

    # =====================
    # IF / MAYBE
    # =====================

    def parse_if(self):

        self.match("IF")

        condition = self.parse_expression()

        self.skip_newlines()

        true_body = []
        false_body = []

        while (
            self.current().type != "ELSE"
            and self.current().type != "DONE"
        ):
            stmt = self.parse_statement()

            if stmt is not None:
                true_body.append(stmt)

            self.skip_newlines()

        if self.current().type == "ELSE":

            self.match("ELSE")
            self.skip_newlines()

            while self.current().type != "DONE":
                false_body.append(
                    self.parse_statement()
                )

                self.skip_newlines()

        self.match("DONE")
        self.match("WITH")
        self.match("THAT")

        return IfNode(
            condition,
            true_body,
            false_body
        )

    # =====================
    # REPEAT
    # =====================

    def parse_repeat(self):

        self.match("REPEAT")

        count = self.parse_expression()

        if self.current().type == "TIMES_KW":
            self.advance()

        self.skip_newlines()

        body = []
        
        print(self.current())

        while self.current().type != "DONE":

            stmt = self.parse_statement()

            if stmt is not None:
                body.append(stmt)

            self.skip_newlines()

        self.match("DONE")
        self.match("WITH")
        self.match("THAT")

        return RepeatNode(
            count,
            body
        )

    # =====================
    # FUNCTIONS
    # =====================

    def parse_function(self):

        self.match("THE")
        self.match("THING")
        self.match("CALLED")

        name = self.match(
            "IDENTIFIER"
        ).value

        params = []

        if self.current().type == "WHICH":

            self.match("WHICH")
            self.match("NEEDS")

            while self.current().type == "IDENTIFIER":
                params.append(
                    self.current().value
                )
                self.advance()
                if self.current().type == "AND":
                    self.advance()

        self.skip_newlines()

        body = []

        self.skip_newlines()

        while self.current().type != "THATS":

            stmt = self.parse_statement()

            if stmt is not None:
                body.append(stmt)

            self.skip_newlines()

        self.match("THATS")
        self.match("IT")

        return FunctionDefNode(
            name,
            params,
            body
        )

    # =====================
    # EXPRESSIONS
    # =====================

    def parse_expression(self):
        return self.parse_or()

    def parse_comparison(self):

        node = self.parse_term()

        while (
            self.current().type == "OPERATOR"
            and self.current().value in (
                "==",
                "!=",
                ">",
                "<",
                ">=",
                "<="
            )
        ):

            op = self.current().value

            self.advance()

            right = self.parse_term()

            node = BinaryOpNode(
                node,
                op,
                right
            )

        return node

    def parse_term(self):

        node = self.parse_factor()

        while (
            self.current().type == "OPERATOR"
            and self.current().value in (
                "+",
                "-"
            )
        ):
            op = self.current().value
            self.advance()

            right = self.parse_factor()

            node = BinaryOpNode(
                node,
                op,
                right
            )

        return node

    def parse_factor(self):

        node = self.parse_unary()

        while (
            self.current().type == "OPERATOR"
            and self.current().value in (
                "*",
                "/"
            )
        ):
            op = self.current().value
            self.advance()

            right = self.parse_unary()

            node = BinaryOpNode(
                node,
                op,
                right
            )

        return node

    def parse_unary(self):

        if self.current().type == "NOT":

            self.advance()

            return UnaryOpNode(
                "not",
                self.parse_unary()
            )

        if (
            self.current().type == "OPERATOR"
            and self.current().value == "-"
        ):

            self.advance()

            return UnaryOpNode(
                "-",
                self.parse_unary()
            )

        return self.parse_primary()
        
    def parse_while(self):

        self.match("AS")
        self.match("LONG")
        self.match("AS")

        condition = self.parse_expression()

        self.skip_newlines()

        body = []

        while self.current().type != "DONE":

            stmt = self.parse_statement()

            if stmt is not None:
                body.append(stmt)

            while self.current().type == "NEWLINE":
                self.advance()

        self.match("DONE")
        self.match("WITH")
        self.match("THAT")

        return WhileNode(
            condition,
            body
        )

    # =====================
    # PRIMARY
    # =====================

    def parse_primary(self):      
        while self.current().type == "NEWLINE":
            self.advance()
        token = self.current()

        if token.type == "INTEGER":
            self.advance()
            return NumberNode(
                int(token.value)
            )

        if token.type == "FLOAT":
            self.advance()
            return NumberNode(
                float(token.value)
            )

        if token.type == "STRING":
            self.advance()
            return StringNode(
                token.value
            )

        if token.type == "TRUE":
            self.advance()
            return BooleanNode(True)

        if token.type == "FALSE":
            self.advance()
            return BooleanNode(False)
            
        if token.type == "ASK":

            self.advance()

            type_token = self.current()

            if type_token.type not in (
                "TEXT_TYPE",
                "NUMBER_TYPE",
                "DECIMAL_TYPE",
                "TRUTH_TYPE"
            ):
                raise SyntaxError(
                    "Expected a type after 'ask'"
                )

            value_type = type_token.value

            self.advance()

            prompt = self.parse_expression()

            return InputNode(
                value_type,
                prompt
            )

        # variable or function call
        if token.type == "IDENTIFIER":

            name = token.value

            self.advance()
            
            if self.current().type == "DOT":

                self.advance()

                method_name = self.match(
                    "IDENTIFIER"
                ).value

                self.match("LPAREN")

                args = []

                if self.current().type != "RPAREN":

                    while True:

                        args.append(
                            self.parse_expression()
                        )

                        if self.current().type == "COMMA":
                            self.advance()
                            continue
        
                        break

                self.match("RPAREN")

                return MethodCallNode(
                    name,
                    method_name,
                    args
                )

            if self.current().type == "LPAREN":

                self.advance()

                args = []

                while (
                    self.current().type
                    != "RPAREN"
                ):
                    args.append(
                        self.parse_expression()
                    )

                    if (
                        self.current().type
                        == "COMMA"
                    ):
                        self.advance()

                self.match("RPAREN")

                return FunctionCallNode(
                    name,
                    args
                )

            if self.current().type == "LBRACKET":

                self.advance()

                index = self.parse_expression()

                self.match("RBRACKET")

                return IndexNode(
                    name,
                    index
                )

            return VariableNode(name)

        if token.type == "LPAREN":

            self.advance()

            expr = self.parse_expression()

            self.match("RPAREN")

            return expr
            
        if token.type == "LBRACKET":
            self.advance()
            elements = []
            if self.current().type != "RBRACKET":
                while True:
                    elements.append(
                        self.parse_expression()
                    )
                    if self.current().type == "COMMA":
                        self.advance()
                        continue
                    break
            self.match("RBRACKET")
            return ListNode(elements)

        from errors import AntiScriptError
        raise AntiScriptError(f"Unexpected token {self.current().type}")