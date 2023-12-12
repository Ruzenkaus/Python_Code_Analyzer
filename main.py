import ast
from typing import Dict, Union

class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self, assumptions: Dict[str, Union[int, float]]):
        self.result = {'dangerous_functions': [], 'errors': []}
        self.variables = assumptions

    def visit_Assign(self, node: ast.Assign) -> None:
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.variables[target.id] = self.visit(node.value)

    def visit_BinOp(self, node: ast.BinOp) -> Union[int, float, None]:
        left_value = self.visit(node.left)
        right_value = self.visit(node.right)

        if isinstance(node.op, ast.Div) and right_value == 0:
            self.result['errors'].append(f"Division by zero detected: {ast.dump(node)}")

        return None

    def visit_Num(self, node: ast.Num) -> Union[int, float]:
        return node.n

    def visit_Name(self, node: ast.Name) -> Union[int, float, None]:
        return self.variables.get(node.id, None)

    def visit_Call(self, node: ast.Call) -> str:
        dangerous_functions = ['eval', 'exec', 'input', 'os.system', 'subprocess.call']
        for func in dangerous_functions:
            if func in ast.dump(node):
                self.result['dangerous_functions'].append(f"Detected dangerous function: {func}")
        return str(node.func)

    def Analysis_Func(self, tree: ast.AST) -> Dict[str, str]:
        self.generic_visit(tree)
        self.visit(tree)
        return self.result


code = """

"""


assumptions = {'x': 0}
tree = ast.parse(code)
analyzer = CodeAnalyzer(assumptions)
result = analyzer.Analysis_Func(tree)

for category, items in result.items():
    print(f"{category.capitalize()}:\n")
    for item in items:
        print(item)
    print("\n" + "=" * 40 + "\n")
