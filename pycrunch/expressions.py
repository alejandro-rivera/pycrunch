"""
This module provides basic support for converting expression strings (defined
in a python-like DSL) into crunch expression objects.

For example, the expression 'disposition == 0 or exit_status == 0' would
be transformed by this module's parser into:

        {
            'function': 'or',
            'args': [
                {
                    'function': '==',
                    'args': [
                        {
                            'variable': 'disposition'
                        },
                        {
                            'value': 0
                        }
                    ]
                },
                {
                    'function': '==',
                    'args': [
                        {
                            'variable': 'exit_status'
                        },
                        {
                            'value': 0
                        }
                    ]
                }
            ]
        }

Its important to note that the expression objects produced by this module's
parser are not ready for being sent to crunch, as they refer to variables
by `alias` rather than by `variable_id` (which is a URL). So, this module
also provides a `process_expr` function that creates an expression object
ready for the crunch API.
"""

import ast
import copy


NOT_IN = object()


def parse_expr(expr):

    def _parse(node, parent=None):
        obj = {}
        args = []
        op = None

        if isinstance(node, ast.AST):
            # Get the current node fields.
            fields = list(ast.iter_fields(node))

            # "Terminal" nodes. Recursion ends with these guys.
            if isinstance(node, ast.Name):
                _id = fields[0][1]
                return {
                    'variable': _id
                }
            elif isinstance(node, ast.Num) or isinstance(node, ast.Str):
                _val = fields[0][1]
                return {
                    'value': _val
                }
            elif isinstance(node, ast.Eq):
                return '=='
            elif isinstance(node, ast.NotEq):
                return '!='
            elif isinstance(node, ast.Lt):
                return '<'
            elif isinstance(node, ast.LtE):
                return '<='
            elif isinstance(node, ast.Gt):
                return '>'
            elif isinstance(node, ast.GtE):
                return '>='
            elif isinstance(node, ast.In):
                return 'in'
            elif isinstance(node, ast.NotIn):
                return NOT_IN
            elif isinstance(node, ast.List):
                _list = fields[0][1]
                if not (all(isinstance(el, ast.Str) for el in _list) or
                        all(isinstance(el, ast.Num) for el in _list)):
                    # Only list-of-int or list-of-str are currently supported
                    raise ValueError

                return {
                    'value': [
                        getattr(el, 's', None) or getattr(el, 'n')
                        for el in _list
                    ]
                }
            elif isinstance(node, ast.Attribute) \
                    and isinstance(parent, ast.Call):
                # The variable.
                _id_node = fields[0][1]
                if not isinstance(_id_node, ast.Name):
                    raise ValueError
                _id = _parse(_id_node, parent=node)

                # The 'method'
                crunch_method_map = {
                    'has_any': 'any',
                    'has_all': 'all'
                }
                method = fields[1][1]
                if method not in crunch_method_map.keys():
                    raise ValueError

                return _id, crunch_method_map[method]

            # "Non-terminal" nodes.
            else:
                for _name, _val in fields:
                    if not isinstance(node, ast.UnaryOp) and (
                            isinstance(_val, ast.BoolOp)
                            or isinstance(_val, ast.UnaryOp)
                            or isinstance(_val, ast.Compare)
                            or isinstance(_val, ast.Call)):
                        # Descend.
                        obj.update(_parse(_val, parent=node))
                    elif isinstance(_val, ast.And):
                        op = 'and'
                    elif isinstance(_val, ast.Or):
                        op = 'or'
                    elif isinstance(_val, ast.Not):
                        op = 'not'
                    elif _name == 'left':
                        left = _parse(_val, parent=node)
                        args.append(left)
                    elif _name == 'func' and isinstance(_val, ast.Attribute):
                        left, op = _parse(_val, parent=node)
                        args.append(left)
                    elif _name == 'ops':
                        if len(_val) != 1:
                            raise ValueError
                        op = _parse(_val[0], parent=node)
                    elif _name == 'comparators' or _name == 'args':  # right
                        if len(_val) != 1:
                            raise ValueError
                        right = _parse(_val[0], parent=node)

                        # In method calls, we only allow list-of-int parameters.
                        if _name == 'args':
                            if 'value' not in right \
                                    or not isinstance(right['value'], list):
                                raise ValueError

                        args.append(right)
                    elif _name in ('keywords', 'starargs', 'kwargs') and _val:
                        # We don't support these in method calls.
                        raise ValueError
                    elif _name == 'operand' and isinstance(node, ast.UnaryOp):
                        right = _parse(_val, parent=node)
                        args.append(right)
                    elif isinstance(_val, list):
                        for arg in _val:
                            args.append(_parse(arg, parent=node))

                if op:
                    if op is NOT_IN:
                        # Special treatment for the `not in` operator.
                        obj = {
                            'function': 'not',
                            'args': [
                                {
                                    'function': 'in',
                                    'args': []
                                }
                            ]
                        }
                    else:
                        obj = {
                            'function': op,
                            'args': []
                        }

                if args and 'args' in obj:
                    if op is NOT_IN:
                        # Special treatment for the `not in` operator.
                        obj['args'][0]['args'] = args
                    else:
                        obj['args'] = args

        return obj

    if expr is None:
        return dict()

    return _parse(ast.parse(expr, mode='eval'))


def process_expr(obj, ds):
    """
    Given a Crunch expression object (or objects) and a Dataset entity object
    (i.e. a Shoji entity), this function returns a new expression object
    (or a list of new expression objects) with all variable aliases
    transformed into variable URLs, just as the crunch API needs them to be.
    """

    def _process(obj, variables):
        for key, val in obj.items():
            if isinstance(val, dict):
                _process(val, variables)
            elif isinstance(val, list) or isinstance(val, tuple):
                for subitem in val:
                    _process(subitem, variables)
            elif key == 'variable':
                obj[key] = variables[val].entity.self
        return obj

    variables = ds.variables.by('alias')

    if isinstance(obj, list):
        return [
            _process(copy.deepcopy(element), variables) for element in obj
        ]
    else:
        return _process(copy.deepcopy(obj), variables)