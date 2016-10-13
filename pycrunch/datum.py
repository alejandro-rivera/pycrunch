import ast
from collections import defaultdict

class Node(object):

    def __init__(self, parent, node_type, expression=None, children=None):
        """
        :param parent: None for root, pointer to parent otherwise
        :param expression: ast.Node or str
        :param children: list of children
        """
        self.parent = parent
        self.expression = expression
        self.children = children
        self.type = node_type

    def __str__(self):
        return self.expression or 'None'

    def __repr__(self):
        return self.expression or 'None'


class FormulaParser(ast.NodeVisitor):

    def __init__(self, formula):
        # store nodes that need processing
        self.to_process = []
        # store all the leaf nodes
        self.leaf_nodes = []
        formula = self.pre_processing(formula)
        self.root = Node(
            parent=None,
            expression='1==1',
            node_type='module',
            children=None
        )
        children = []
        for node in ast.iter_child_nodes(ast.parse(formula)):
            tree_node = Node(parent=self.root, node_type='node', expression=node, children=None)
            children.append(tree_node)
        self.root.children = children
        self.to_process.extend(children)
        self.case_tree = defaultdict(list)

    def pre_processing(self, formula):
        # cleans some formula things
        formula = formula.replace('pdl.', '')
        formula = formula.replace('elif ', 'if ')
        return formula

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
        elif isinstance(node, ast.Str):
            return str(node.s)
        elif isinstance(node, ast.Compare):
            return self.unfold_compare(node)
        else:
            return 'What is this %s' % node

    def unfold_compare(self, node):
        nodes = ast.iter_child_nodes(node)
        expr = ''
        for nd in nodes:
            expr += self.translate_node(nd)
        return expr

    def visit_if(self, node):
        """
        Node with children
        """
        test = node.test
        operator = None
        try:
            # translate the operator to it's textual val
            operator = self.translate_node(test.op)
            # process operator here, don't do it recursively
            del test.op
            values = test.values
            result = []
            for val in values:
                result.append(self.unfold_compare(val))
            if_return = operator.join(result)
        except:
            pass
        # Note: for now only support 1 assignment on else, no nested
        # conditions under else supported now
        orelse = node.orelse
        # make sure we don't process this again in iter_child
        del node.orelse
        if orelse:
            else_return = self.visit_assign(orelse[0])
        else:
            else_return = None
        if not operator:
            if_return = self.unfold_compare(test)
        return if_return, else_return

    def visit_assign(self, node):
        """
        Leaf node
        """
        expression = list(ast.iter_child_nodes(node))
        var = getattr(expression[0], 'id')
        # this might be another variable
        value = self.translate_node(expression[1])
        return "%s=%s" % (var, value)

    def process_node(self, tree_node):
        """
        Solves the expression in a tree_node ot a string and
        ands it's children
        """
        node = tree_node.expression
        children = []
        # first update the expression attribute
        if isinstance(node, ast.If):
            # orelse if exists is a direct child of if node
            # but with node_type = else
            tree_node.expression, orelse = self.visit_if(node)
            for _node in ast.iter_child_nodes(node):
                new_tree_node = Node(parent=tree_node, node_type='node', expression=_node, children=None)
                children.append(new_tree_node)
            if orelse:
                # create a new node, assign the already processed expression
                else_node = Node(parent=tree_node, node_type='else', expression=orelse)
                children.append(else_node)
                self.leaf_nodes.append(else_node)
            tree_node.children = children
            self.to_process.extend(children)
        elif isinstance(node, ast.Assign):
            tree_node.expression = self.visit_assign(node)
            # append leaf node to self.leaf_nodes
            self.leaf_nodes.append(tree_node)

    def walk(self):
        """
        takes care of dealing with all the nodes in an AST
        """
        while self.to_process:
            # pop from start
            tree_node = self.to_process.pop(0)
            self.process_node(tree_node)

    def build_dict(self):
        for leaf in self.leaf_nodes:
            node = leaf
            key = node.expression
            new_conditional = []
            while node.parent:
                modifier = ''
                if node.type == 'else':
                    modifier = '!'
                node = node.parent
                new_conditional.append(modifier + node.expression)
            # join all sub-ifs with and
            new_conditional = ' and '.join(new_conditional)
            # finally append the list to the conditions list
            self.case_tree[key].append(new_conditional)

    def run(self):
        self.walk()
        self.build_dict()


# TEST FUNCTIONS ==================================================================================================
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
                    ast_visit(item, level=level + 1)
        elif isinstance(value, ast.AST):
            ast_visit(value, level=level + 1)


import pprint
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
        if deeper == 91232:
            test = 5
            if avern > 8:
                test = 3
    if combo < 1:
        test = 4
else:
    test = 5
"""

# formula = """
# if pdl.age == 1 and pdl.size == 2 and pdl.country == 3:
#     test = 1
# """
#
# formula = """
# if pdl.size == 1 and pdl.size == 2 and pdl.country == 3:
#     if pdl.gender == 1:
#         test = 1
# elif pdl.age == 15:
#     if pdl.gender == 2:
#         test = 2
# else:
#     test = 3
# """


# big_ass_formula = """
# if pdl.race == 3 and pdl.e14_presvote12 == 1 and pdl.age >= 18 and pdl.age <= 34: polistrata_hisp = 1
# if pdl.race == 3 and pdl.e14_presvote12 == 1  and pdl.age >=35: polistrata_hisp = 2
# if pdl.race == 3 and  pdl.e14_presvote12 in [3,4] and pdl.age >= 18 and pdl.age <= 34: polistrata_hisp = 3
# if pdl.race == 3 and pdl.e14_presvote12 in [3,4] and pdl.age >=35: polistrata_hisp = 4
# if pdl.race == 3 and pdl.e14_presvote12 == 2 and pdl.age >= 18 and pdl.age <= 34: polistrata_hisp = 5
# if pdl.race == 3 and pdl.e14_presvote12 == 2 and pdl.age >=35: polistrata_hisp = 6
# elif pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 1 and pdl.gender == 2 and pdl.age >= 18 and pdl.age <30 and pdl.educ in [1,2,3,4]: polistrata_hisp =  7
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 1 and pdl.gender == 2 and pdl.age >= 18 and pdl.age <30 and pdl.educ in [5,6]: polistrata_hisp =  8
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 1 and pdl.gender == 1 and pdl.age >= 18 and pdl.age <30 and pdl.educ in [1,2,3,4]: polistrata_hisp =  9
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 1 and pdl.gender == 1 and pdl.age >= 18 and pdl.age <30 and pdl.educ in [5,6]: polistrata_hisp =  10
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 1 and pdl.gender == 2 and pdl.age >= 30 and pdl.age <= 44 and pdl.educ in [1,2,3,4]: polistrata_hisp =  11
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 1 and pdl.gender == 2 and pdl.age >= 30 and pdl.age <= 44 and pdl.educ in [5,6]: polistrata_hisp =  12
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 1 and pdl.gender == 1 and pdl.age >= 30 and pdl.age <= 44 and pdl.educ in [1,2,3,4]: polistrata_hisp =  13
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 1 and pdl.gender == 1 and pdl.age >= 30 and pdl.age <= 44 and pdl.educ in [5,6]: polistrata_hisp =  14
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 1 and pdl.gender == 2 and pdl.age >= 45 and pdl.age <= 64 and pdl.educ in [1,2,3,4]: polistrata_hisp =  15
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 1 and pdl.gender == 2 and pdl.age >= 45 and pdl.age <= 64 and pdl.educ in [5,6]: polistrata_hisp =  16
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 1 and pdl.gender == 1 and pdl.age >= 45 and pdl.age <= 64 and pdl.educ in [1,2,3,4]: polistrata_hisp =  17
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 1 and pdl.gender == 1 and pdl.age >= 45 and pdl.age <= 64 and pdl.educ in [5,6]: polistrata_hisp =  18
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 1 and pdl.gender == 2 and pdl.age >=65 and pdl.educ in [1,2,3,4]: polistrata_hisp =  19
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 1 and pdl.gender == 2 and pdl.age >=65  and pdl.educ in [5,6]: polistrata_hisp =  20
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 1 and pdl.gender == 1 and pdl.age >= 45 and pdl.age <= 64 and pdl.educ in [1,2,3,4]: polistrata_hisp =  21
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 1 and pdl.gender == 1 and pdl.age >= 45 and pdl.age <= 64 and pdl.educ in [5,6]: polistrata_hisp =  22
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == [3,4] and pdl.gender == 2 and pdl.age >= 18 and pdl.age <30 and pdl.educ in [1,2,3,4]: polistrata_hisp =  23
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 ==  [3,4] and pdl.gender == 2 and pdl.age >= 18 and pdl.age <30 and pdl.educ in [5,6]: polistrata_hisp =  24
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 ==  [3,4] and pdl.gender == 1 and pdl.age >= 18 and pdl.age <30 and pdl.educ in [1,2,3,4]: polistrata_hisp =  25
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == [3,4] and pdl.gender == 1 and pdl.age >= 18 and pdl.age <30 and pdl.educ in [5,6]: polistrata_hisp =  26
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == [3,4] and pdl.gender == 2 and pdl.age >= 30 and pdl.age <= 44 and pdl.educ in [1,2,3,4]: polistrata_hisp =  27
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == [3,4] and pdl.gender == 2 and pdl.age >= 30 and pdl.age <= 44 and pdl.educ in [5,6]: polistrata_hisp =  28
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == [3,4] and pdl.gender == 1 and pdl.age >= 30 and pdl.age <= 44 and pdl.educ in [1,2,3,4]: polistrata_hisp =  29
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == [3,4] and pdl.gender == 1 and pdl.age >= 30 and pdl.age <= 44 and pdl.educ in [5,6]: polistrata_hisp =  30
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == [3,4] and pdl.gender == 2 and pdl.age >= 45 and pdl.age <= 64 and pdl.educ in [1,2,3,4]: polistrata_hisp =  31
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == [3,4] and pdl.gender == 2 and pdl.age >= 45 and pdl.age <= 64 and pdl.educ in [5,6]: polistrata_hisp =  32
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == [3,4] and pdl.gender == 1 and pdl.age >= 45 and pdl.age <= 64 and pdl.educ in [1,2,3,4]: polistrata_hisp =  33
# elif pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == [3,4] and pdl.gender == 1 and pdl.age >= 45 and pdl.age <= 64 and pdl.educ in [5,6]: polistrata_hisp =  34
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == [3,4] and pdl.gender == 2 and pdl.age >=65 and pdl.educ in [1,2,3,4]: polistrata_hisp =  35
# elif pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == [3,4] and pdl.gender == 2 and pdl.age >=65  and pdl.educ in [5,6]: polistrata_hisp =  36
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == [3,4] and pdl.gender == 1 and pdl.age >= 45 and pdl.age <= 64 and pdl.educ in [1,2,3,4]: polistrata_hisp =  37
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == [3,4] and pdl.gender == 1 and pdl.age >= 45 and pdl.age <= 64 and pdl.educ in [5,6]: polistrata_hisp =  38
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 2 and pdl.gender == 2 and pdl.age >= 18 and pdl.age <30 and pdl.educ in [1,2,3,4]: polistrata_hisp =  39
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 ==  2 and pdl.gender == 2 and pdl.age >= 18 and pdl.age <30 and pdl.educ in [5,6]: polistrata_hisp =  40
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 ==  2 and pdl.gender == 1 and pdl.age >= 18 and pdl.age <30 and pdl.educ in [1,2,3,4]: polistrata_hisp =  41
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 2 and pdl.gender == 1 and pdl.age >= 18 and pdl.age <30 and pdl.educ in [5,6]: polistrata_hisp =  42
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 2 and pdl.gender == 2 and pdl.age >= 30 and pdl.age <= 44 and pdl.educ in [1,2,3,4]: polistrata_hisp =  43
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 2 and pdl.gender == 2 and pdl.age >= 30 and pdl.age <= 44 and pdl.educ in [5,6]: polistrata_hisp =  44
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 2 and pdl.gender == 1 and pdl.age >= 30 and pdl.age <= 44 and pdl.educ in [1,2,3,4]: polistrata_hisp =  45
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 2 and pdl.gender == 1 and pdl.age >= 30 and pdl.age <= 44 and pdl.educ in [5,6]: polistrata_hisp =  46
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 2 and pdl.gender == 2 and pdl.age >= 45 and pdl.age <= 64 and pdl.educ in [1,2,3,4]: polistrata_hisp =  47
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 2 and pdl.gender == 2 and pdl.age >= 45 and pdl.age <= 64 and pdl.educ in [5,6]: polistrata_hisp =  48
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 2 and pdl.gender == 1 and pdl.age >= 45 and pdl.age <= 64 and pdl.educ in [1,2,3,4]: polistrata_hisp =  49
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 2 and pdl.gender == 1 and pdl.age >= 45 and pdl.age <= 64 and pdl.educ in [5,6]: polistrata_hisp =  50
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 2 and pdl.gender == 2 and pdl.age >=65 and pdl.educ in [1,2,3,4]: polistrata_hisp =  51
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 2 and pdl.gender == 2 and pdl.age >=65  and pdl.educ in [5,6]: polistrata_hisp =  52
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 2 and pdl.gender == 1 and pdl.age >=65 and pdl.educ in [1,2,3,4]: polistrata_hisp =  53
# if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 2 and pdl.gender == 1 and pdl.age >=65 and pdl.educ in [5,6]: polistrata_hisp =  54
# """


if __name__ == '__main__':
    # ast_visit(ast.parse(formula))

    v = FormulaParser(formula=formula)
    v.run()
    pp.pprint(v.case_tree)