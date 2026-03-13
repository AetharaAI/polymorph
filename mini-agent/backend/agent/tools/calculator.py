import math
import ast
import operator


# Safe math namespace
SAFE_MATH = {
    "abs": abs,
    "round": round,
    "min": min,
    "max": max,
    "sum": sum,
    "pow": pow,
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "log": math.log,
    "log10": math.log10,
    "log2": math.log2,
    "exp": math.exp,
    "pi": math.pi,
    "e": math.e,
    "tau": math.tau,
    "inf": math.inf,
    "nan": math.nan,
    "floor": math.floor,
    "ceil": math.ceil,
    "factorial": math.factorial,
    "gcd": math.gcd,
    "degrees": math.degrees,
    "radians": math.radians,
}


class SafeEval:
    """Safe expression evaluator."""

    SAFE_OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
        ast.Eq: operator.eq,
        ast.NotEq: operator.ne,
        ast.Lt: operator.lt,
        ast.LtE: operator.le,
        ast.Gt: operator.gt,
        ast.GtE: operator.ge,
    }

    SAFE_NAMES = SAFE_MATH.copy()

    def __init__(self):
        self.nodes = []

    def visit(self, node):
        method = f"visit_{type(node).__name__}"
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise ValueError(f"Unsafe expression: {type(node).__name__}")

    def visit_Module(self, node):
        if len(node.body) != 1:
            raise ValueError("Only single expression allowed")
        return self.visit(node.body[0])

    def visit_Expression(self, node):
        return self.visit(node.body)

    def visit_Expr(self, node):
        return self.visit(node.value)

    def visit_Constant(self, node):
        return node.value

    def visit_Num(self, node):
        return node.n

    def visit_Name(self, node):
        if node.id not in self.SAFE_NAMES:
            raise ValueError(f"Unknown name: {node.id}")
        return self.SAFE_NAMES[node.id]

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op_type = type(node.op)
        if op_type not in self.SAFE_OPERATORS:
            raise ValueError(f"Unsupported operator: {op_type.__name__}")
        return self.SAFE_OPERATORS[op_type](left, right)

    def visit_UnaryOp(self, node):
        operand = self.visit(node.operand)
        op_type = type(node.op)
        if op_type not in self.SAFE_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        return self.SAFE_OPERATORS[op_type](operand)

    def visit_Compare(self, node):
        left = self.visit(node.left)
        for op, comparator in zip(node.ops, node.comparators):
            right = self.visit(comparator)
            op_type = type(op)
            if op_type not in self.SAFE_OPERATORS:
                raise ValueError(f"Unsupported compare: {op_type.__name__}")
            if not self.SAFE_OPERATORS[op_type](left, right):
                return False
            left = right
        return True

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id not in self.SAFE_NAMES:
                raise ValueError(f"Unknown function: {node.func.id}")
            func = self.SAFE_NAMES[node.func.id]
            args = [self.visit(arg) for arg in node.args]
            return func(*args)
        raise ValueError("Only direct function calls allowed")


def calculate(expression: str) -> str:
    """Perform mathematical calculations safely."""
    try:
        # Validate expression
        expression = expression.strip()

        # Parse and evaluate
        tree = ast.parse(expression, mode="eval")
        evaluator = SafeEval()
        result = evaluator.visit(tree)

        # Format result
        if isinstance(result, float):
            if result == int(result):
                return str(int(result))
            return f"{result:.10f}".rstrip("0").rstrip(".")
        return str(result)

    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Error: Could not evaluate expression - {str(e)}"
