# interpreter.py
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
import importlib.util
from ast_nodes import *
from runtime import ReturnSignal, RuntimeErrorAnti
from runtime import Scope


class Interpreter:

    def __init__(self, runtime):
        self.runtime = runtime
        
    def visit_IndexNode(self, node):
        target = self.runtime.get(
            node.object_name
        )
        index = self.visit(
            node.index
        )
        return target[index]

    # =====================
    # ENTRY
    # =====================

    def run(self, program):
        return self.visit(program)

    # =====================
    # DISPATCH
    # =====================

    def visit(self, node):

        method_name = f"visit_{type(node).__name__}"

        method = getattr(
            self,
            method_name,
            self.no_visit
        )
        
        if node is None:
            print("WARNING: None node visited")
            return None

        return method(node)

    def no_visit(self, node):
        raise Exception(
            f"No visitor for {type(node).__name__}"
        )

    # =====================
    # PROGRAM
    # =====================

    def visit_ProgramNode(self, node):

        result = None

        for statement in node.statements:
            result = self.visit(statement)

        return result

    # =====================
    # LITERALS
    # =====================

    def visit_NumberNode(self, node):
        return node.value

    def visit_StringNode(self, node):
        return node.value

    def visit_BooleanNode(self, node):
        return node.value

    def visit_ListNode(self, node):
        return [
            self.visit(item)
            for item in node.elements
        ]

    # =====================
    # VARIABLES
    # =====================

    def visit_VariableNode(self, node):
        return self.runtime.get(node.name)

    def visit_AssignmentNode(self, node):

        value = self.visit(node.value)

        self.runtime.set(
            node.name,
            value
        )

        return value

    # =====================
    # PRINT
    # =====================

    def visit_PrintNode(self, node):

        value = self.visit(node.value)

        print(value)

        return value

    # =====================
    # INPUT
    # =====================     
    def visit_InputNode(self, node):

        prompt = self.visit(
            node.prompt
        )

        result = input(
            str(prompt)
        )

        if node.value_type == "text":
            return result

        if node.value_type == "number":
            return int(result)

        if node.value_type == "decimal":
            return float(result)

        if node.value_type == "truth":

            result = result.lower()

            return result in (
                "true",
                "yes",
                "1",
                "y"
            )

        return result

    # =====================
    # MATH / COMPARISON
    # =====================

    def visit_BinaryOpNode(self, node):

        left = self.visit(node.left)
        right = self.visit(node.right)

        op = node.operator

        if op == "+":

            if (
                isinstance(left, str)
                or isinstance(right, str)
            ):
                return str(left) + str(right)

            return left + right

        if op == "-":
            return left - right

        if op == "*":
            return left * right

        if op == "/":
            return left / right

        if op == "==":
            return left == right

        if op == "!=":
            return left != right

        if op == ">":
            return left > right

        if op == "<":
            return left < right
            
        if op == ">=":
            return left >= right

        if op == "<=":
            return left <= right

        if op == "and":
            return bool(left) and bool(right)

        if op == "or":
            return bool(left) or bool(right)

        raise RuntimeErrorAnti(
            f"Unknown operator {op}"
        )

    def visit_UnaryOpNode(self, node):

        value = self.visit(
            node.operand
        )

        if node.operator == "-":
            return -value

        if node.operator == "not":
            return not value

        raise RuntimeErrorAnti(
            f"Unknown unary operator {node.operator}"
        )

    # =====================
    # IF
    # =====================

    def visit_IfNode(self, node):

        condition = self.visit(
            node.condition
        )

        if condition:

            for stmt in node.true_body:
                self.visit(stmt)

        else:

            for stmt in node.false_body:
                self.visit(stmt)

    # =====================
    # REPEAT
    # =====================

    def visit_RepeatNode(self, node):

        count = int(
            self.visit(node.count)
        )

        for _ in range(count):

            for stmt in node.body:
                self.visit(stmt)
                
    def visit_WhileNode(self, node):

        while self.visit(
            node.condition
        ):

            for stmt in node.body:
                self.visit(stmt)

    # =====================
    # FUNCTIONS
    # =====================

    def visit_FunctionDefNode(self, node):

        self.runtime.functions[
            node.name
        ] = node

        return None

    def visit_FunctionCallNode(self, node):

    # =====================
    # NATIVE PYTHON FUNCTIONS
    # =====================

        if (
            node.name
            in self.runtime.native_functions
        ):
    
            args = [
                self.visit(arg)
                for arg in node.args
            ]

            return (
                self.runtime.native_functions[
                    node.name
                ](*args)
            )

    # =====================
    # BUILT-IN CONVERSIONS
    # =====================

        if node.name == "number":

            value = self.visit(
                node.args[0]
            )

            return int(value)
    
        if node.name == "decimal":

            value = self.visit(
                node.args[0]
            )
    
            return float(value)

        if node.name == "text":

            value = self.visit(
                node.args[0]
            )

            return str(value)

        if node.name == "truth":

            value = self.visit(
                node.args[0]
            )

            if isinstance(value, str):
    
                value = value.lower()

                if value in (
                    "false",
                    "no",
                    "nope",
                    "0"
                ):
                    return False

                if value in (
                    "true",
                    "yes",
                    "absolutely",
                    "1"
                ):
                    return True
    
            return bool(value)

    # =====================
    # USER FUNCTIONS
    # =====================

        if (
            node.name
            not in self.runtime.functions
        ):
            raise RuntimeErrorAnti(
                f"Function '{node.name}' does not exist."
            )

        func = self.runtime.functions[
            node.name
        ]

        values = [
            self.visit(arg)
            for arg in node.args
        ]

        old_scope = (
            self.runtime.global_scope
        )

        function_scope = Scope(
            parent=old_scope
        )

        self.runtime.global_scope = (
            function_scope
        )

        try:
    
            for name, value in zip(
                func.params,
                values
            ):
    
                function_scope.set(
                    name,
                    value
                )

            for stmt in func.body:
                self.visit(stmt)

        except ReturnSignal as r:

            self.runtime.global_scope = (
                old_scope
            )

            return r.value

        self.runtime.global_scope = (
            old_scope
        )

        return None

    # =====================
    # RETURN
    # =====================

    def visit_ReturnNode(self, node):

        value = self.visit(
            node.value
        )

        raise ReturnSignal(value)

    # =====================
    # MODULES
    # =====================

    def visit_BorrowNode(self, node):
        module_name = node.module_name

        # Already loaded?
        if module_name in self.runtime.loaded_modules:
            return

        anti_path = os.path.join(
            BASE_DIR,
            "modules",
            "anti",
            f"{module_name}.anti"
        )

        py_path = os.path.join(
            BASE_DIR,
            "modules",
            "py",
            f"{module_name}.py"
        )

        if os.path.exists(anti_path):

            module_path = anti_path
            module_type = "anti"

        elif os.path.exists(py_path):

            module_path = py_path
            module_type = "py"

        else:
    
            raise RuntimeErrorAnti(
                f"Module '{module_name}' not found."
            )

        # IMPORTANT:
        # Mark as loaded BEFORE execution
        # to prevent recursive imports
        self.runtime.loaded_modules.add(
            module_name
        )

        # =====================
        # AntiScript module
        # =====================

        if module_type == "anti":

            from lexer import Lexer
            from parser import Parser

            with open(
                module_path,
                "r",
                encoding="utf-8"
            ) as f:

                source = f.read()

            lexer = Lexer(source)

            tokens = lexer.tokenize()

            parser = Parser(tokens)

            ast = parser.parse()

            self.visit(ast)

        # =====================
        # Python module
        # =====================

        else:

            spec = (
                importlib.util.spec_from_file_location(
                    module_name,
                    module_path
                )
            )

            module = (
                importlib.util.module_from_spec(
                    spec
                )
            )

            spec.loader.exec_module(
                module
            )

            for name in dir(module):

                if name.startswith("_"):
                    continue

                obj = getattr(
                    module,
                    name
                )
    
                if callable(obj):

                    self.runtime.native_functions[
                        name
                    ] = obj