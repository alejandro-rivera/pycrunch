from pycrunch.expressions import parse_expr
from pycrunch.expressions import process_expr


def create_categorical(dataset, categories, rules, name, alias, description=''):
    """
    method for creating a categorical variable
    """

    if not ((len(categories) - 1) <= len(rules) <= len(categories)):
        raise ValueError(
            'Amount of rules should match categories (or categories -1')

    if not hasattr(dataset, 'variables'):
        dataset.refresh()

    args = [{
        'column': [c['id'] for c in categories],
        'type': {
            'value': {
                'class': 'categorical',
                'categories': categories}}}]

    more_args = []
    for rule in rules:
        more_args.append(parse_expr(rule))

    more_args = process_expr(more_args, dataset)

    expr = dict(function='case', args=args + more_args)

    payload = dict(element='shoji:entity',
                   body=dict(alias=alias,
                             name=name,
                             expr=expr,
                             description=description))

    return dataset.variables.create(payload)
