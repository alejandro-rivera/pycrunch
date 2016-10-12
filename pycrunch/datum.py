import pprint
import ast

pp = pprint.PrettyPrinter(indent=2)


class Node(object):

    def __init__(self, parent, expression, children=None):
        """
        :param parent: None for root, pointer to parent otherwise
        :param expression: ast.Node or str
        :param children: list of children
        """
        self.parent = parent
        self.expression = expression
        if not children:
            self.children = []


class Tree(object):

    def __init__(self, root):
        self.root = root


class FormulaParser(ast.NodeVisitor):

    def translate_node(self, node):
        if isinstance(node, ast.Eq):
            return ' == '
        elif isinstance(node, ast.NotEq):
            return ' != '
        elif isinstance(node, ast.Lt):
            return ' < '
        elif isinstance(node, ast.LtE):
            return ' <= '
        elif isinstance(node, ast.Gt):
            return ' > '
        elif isinstance(node, ast.GtE):
            return ' >= '
        elif isinstance(node, ast.In):
            return ' in '
        elif isinstance(node, ast.Not):
            return ' not '
        elif isinstance(node, ast.NotIn):
            return " not in "
        elif isinstance(node, ast.List):
            values = [x.s for x in ast.iter_child_nodes(node) if type(x) == ast.Str]
            if not values:
                values = [x.n for x in ast.iter_child_nodes(node) if type(x) == ast.Num]
            return "%s" % [n for n in values]
        elif isinstance(node, ast.And):
            return ' and '
        elif isinstance(node, ast.Or):
            return ' or '
        elif isinstance(node, ast.Not):
            return ' not '
        elif isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Num):
            return str(node.n)
        else:
            return 'What is this %s' % node

    def unfold_compare(self, node):
        nodes = ast.iter_child_nodes(node)
        expr = ''
        for nd in nodes:
            expr += self.translate_node(nd)
        return expr

    def visit_If(self, node):
        """
        Node with children
        """
        test = node.test
        # body = node.body
        # orelse = node.orelse
        print("IF %s" % self.unfold_compare(test))
        self.generic_visit(node)

    def visit_Assign(self, node):
        """
        Leaf node
        """
        expression = list(ast.iter_child_nodes(node))
        var = getattr(expression[0], 'id')
        # this might be another variable
        value = getattr(expression[1], 'n')
        print("LEAF NODE: %s = %s" % (var, value))

    def generic_visit(self, node):
        for field, value in ast.iter_fields(node):
            # value
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        self.visit(item)
            elif isinstance(value, ast.AST):
                self.visit(value)
