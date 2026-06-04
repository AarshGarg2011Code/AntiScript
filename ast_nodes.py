from dataclasses import dataclass


@dataclass
class NumberNode:
    value: int | float


@dataclass
class StringNode:
    value: str


@dataclass
class BooleanNode:
    value: bool


@dataclass
class VariableNode:
    name: str


@dataclass
class ListNode:
    elements: list


@dataclass
class BinaryOpNode:
    left: object
    operator: str
    right: object


@dataclass
class UnaryOpNode:
    operator: str
    operand: object


@dataclass
class FunctionCallNode:
    name: str
    args: list


@dataclass
class AssignmentNode:
    name: str
    value: object


@dataclass
class PrintNode:
    value: object


@dataclass
class ReturnNode:
    value: object


@dataclass
class BorrowNode:
    module_name: str


@dataclass
class IfNode:
    condition: object
    true_body: list
    false_body: list


@dataclass
class WhileNode:
    condition: object
    body: list


@dataclass
class RepeatNode:
    count: object
    body: list


@dataclass
class FunctionDefNode:
    name: str
    params: list
    body: list


@dataclass
class ProgramNode:
    statements: list


@dataclass
class MethodCallNode:
    def __init__(
        self,
        object_name,
        method_name,
        args
    ):
        self.object_name = object_name
        self.method_name = method_name
        self.args = args


@dataclass
class IndexNode:
    object_name: str
    index: object
    
    
@dataclass
class InputNode:
    value_type: str
    prompt: object