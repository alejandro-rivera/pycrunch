import pprint
import re
import ast
from datum import FormulaParser

pp = pprint.PrettyPrinter(indent=2)

formula = """
if age > 15:
    if size == 3:
        test = 1
    if size == 4:
        test = 2
if sex == 'male':
    if combo > 1:
        test = 3
        if deeper is None:
            test = -1
            if avern:
                test = None
    elif combo < 1:
        test = 4
    else:
        test = 5
else:
    test = -1
"""


formula = """
if age > 15:
    test = 1
else:
    test = 5
"""

formula = """
if age > 1:
    my_var = 1
if size < 15:
    my_var = 2
"""


def promote_assignments(conditional):
    """
    moves assignments of type var = val to the end of the immediate
    previous conditional
        if test == 1:
            value = 1

        if test == 1: value = 1

    """
    regexp = re.compile(r':\s*\n\s+([^=:]+=[^=\n]+\n)')
    # replace first match group
    return re.sub(regexp, r': \1', conditional)


def str_node(node):
    if isinstance(node, ast.AST):
        fields = [(name, str_node(val)) for name, val in ast.iter_fields(node) if name not in ('left', 'right')]
        rv = '%s(%s' % (node.__class__.__name__, ', '.join('%s=%s' % field for field in fields))
        return rv + ')'
    else:
        return repr(node)


def ast_visit(node, level=0):
    print('  ' * level + str_node(node))
    for field, value in ast.iter_fields(node):
        if isinstance(value, list):
            for item in value:
                if isinstance(item, ast.AST):
                    ast_visit(item, level=level+1)
        elif isinstance(value, ast.AST):
            ast_visit(value, level=level+1)




# ast_visit(ast.parse(formula))

v = FormulaParser()
p = ast.parse(formula)
v.visit(p)
