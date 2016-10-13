import pytest
from unittest import mock
from unittest import TestCase

from pycrunch.datasets import parse_expr
from pycrunch.datasets import process_expr


class TestExpressionParsing(TestCase):

    def test_parse_equal_int(self):
        expr = "age == 1"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '==',
            'args': [
                {
                    'variable': 'age'
                },
                {
                    'value': 1
                }
            ]
        }

        # Reversed.
        expr = "1 == age"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '==',
            'args': [
                {
                    'value': 1
                },
                {
                    'variable': 'age'
                }
            ]
        }

    def test_parse_equal_string(self):
        expr = "name == 'John Doe'"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '==',
            'args': [
                {
                    'variable': 'name'
                },
                {
                    'value': 'John Doe'
                }
            ]
        }

        # Reversed.
        expr = "'John Doe' == name"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '==',
            'args': [
                {
                    'value': 'John Doe'
                },
                {
                    'variable': 'name'
                }
            ]
        }

    def test_parse_notequal_int(self):
        expr = "age != 1"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '!=',
            'args': [
                {
                    'variable': 'age'
                },
                {
                    'value': 1
                }
            ]
        }

        # Reversed.
        expr = "1 != age"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '!=',
            'args': [
                {
                    'value': 1
                },
                {
                    'variable': 'age'
                }
            ]
        }

    def test_parse_notequal_string(self):
        expr = "name != 'John Doe'"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '!=',
            'args': [
                {
                    'variable': 'name'
                },
                {
                    'value': 'John Doe'
                }
            ]
        }

        # Reversed.
        expr = "'John Doe' != name"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '!=',
            'args': [
                {
                    'value': 'John Doe'
                },
                {
                    'variable': 'name'
                }
            ]
        }

    def test_parse_less_than(self):
        expr = "caseid < 1234"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '<',
            'args': [
                {
                    'variable': 'caseid'
                },
                {
                    'value': 1234
                }
            ]
        }

        # Reversed.
        expr = "1234 < caseid"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '<',
            'args': [
                {
                    'value': 1234
                },
                {
                    'variable': 'caseid'
                }
            ]
        }

    def test_parse_less_than_equal(self):
        expr = "caseid <= 1234"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '<=',
            'args': [
                {
                    'variable': 'caseid'
                },
                {
                    'value': 1234
                }
            ]
        }

        # Reversed.
        expr = "1234 <= caseid"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '<=',
            'args': [
                {
                    'value': 1234
                },
                {
                    'variable': 'caseid'
                }
            ]
        }

    def test_parse_greater_than(self):
        expr = "caseid > 1234"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '>',
            'args': [
                {
                    'variable': 'caseid'
                },
                {
                    'value': 1234
                }
            ]
        }

        # Reversed.
        expr = "1234 > caseid"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '>',
            'args': [
                {
                    'value': 1234
                },
                {
                    'variable': 'caseid'
                }
            ]
        }

    def test_parse_greater_than_equal(self):
        expr = "caseid >= 1234"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '>=',
            'args': [
                {
                    'variable': 'caseid'
                },
                {
                    'value': 1234
                }
            ]
        }

        # Reversed.
        expr = "1234 >= caseid"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '>=',
            'args': [
                {
                    'value': 1234
                },
                {
                    'variable': 'caseid'
                }
            ]
        }

    def test_parse_compare_variable_against_another_variable(self):
        expr = "starttdate == arrivedate"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '==',
            'args': [
                {
                    'variable': 'starttdate'
                },
                {
                    'variable': 'arrivedate'
                }
            ]
        }

        expr = "starttdate != arrivedate"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '!=',
            'args': [
                {
                    'variable': 'starttdate'
                },
                {
                    'variable': 'arrivedate'
                }
            ]
        }

        expr = "starttdate < arrivedate"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '<',
            'args': [
                {
                    'variable': 'starttdate'
                },
                {
                    'variable': 'arrivedate'
                }
            ]
        }

        expr = "starttdate <= arrivedate"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '<=',
            'args': [
                {
                    'variable': 'starttdate'
                },
                {
                    'variable': 'arrivedate'
                }
            ]
        }

        expr = "starttdate > arrivedate"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '>',
            'args': [
                {
                    'variable': 'starttdate'
                },
                {
                    'variable': 'arrivedate'
                }
            ]
        }

        expr = "starttdate >= arrivedate"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': '>=',
            'args': [
                {
                    'variable': 'starttdate'
                },
                {
                    'variable': 'arrivedate'
                }
            ]
        }

    def test_parse_multiple_boolean_conditions(self):
        expr = '(identity == 1 and caseid <= surveyid) or identity >= 2'
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'or',
            'args': [
                {
                    'function': 'and',
                    'args': [
                        {
                            'function': '==',
                            'args': [
                                {
                                    'variable': 'identity'
                                },
                                {
                                    'value': 1
                                }
                            ]
                        },
                        {
                            'function': '<=',
                            'args': [
                                {
                                    'variable': 'caseid'
                                },
                                {
                                    'variable': 'surveyid'
                                }
                            ]
                        }
                    ]
                },
                {
                    'function': '>=',
                    'args': [
                        {
                            'variable': 'identity'
                        },
                        {
                            'value': 2
                        }
                    ]
                }
            ]
        }

    def test_parse_value_in_list(self):
        expr = "web_browser in ['abc', 'dfg', 'hij']"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'in',
            'args': [
                {
                    'variable': 'web_browser'
                },
                {
                    'value': ['abc', 'dfg', 'hij']
                }
            ]
        }

        # Tuples should also be supported.
        expr = "web_browser in ('abc', 'dfg', 'hij')"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'in',
            'args': [
                {
                    'variable': 'web_browser'
                },
                {
                    'value': ['abc', 'dfg', 'hij']
                }
            ]
        }

    def test_parse_value_not_in_list(self):
        expr = 'country not in [1, 2, 3]'
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'not',
            'args': [
                {
                    'function': 'in',
                    'args': [
                        {
                            'variable': 'country'
                        },
                        {
                            'value': [1, 2, 3]
                        }
                    ]
                }
            ]
        }

        # Tuples should also be supported.
        expr = 'country not in (1, 2, 3)'
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'not',
            'args': [
                {
                    'function': 'in',
                    'args': [
                        {
                            'variable': 'country'
                        },
                        {
                            'value': [1, 2, 3]
                        }
                    ]
                }
            ]
        }

    def test_parse_omnibus_rule_1(self):
        # 'text': 'diposition code 0 (screenouts)',
        # 'index_mapper': intersection(
        #        [{'disposition': [0]}, {'exit_status': [0]}])})
        expr = "disposition == 0 and exit_status == 0"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'and',
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

    def test_parse_has_any(self):
        expr = 'Q2.has_any([1, 2, 3])'
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'any',
            'args': [
                {
                    'variable': 'Q2'
                },
                {
                    'value': [1, 2, 3]
                }
            ]
        }

        expr = 'Q2.has_any((1, 2, 3))'
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'any',
            'args': [
                {
                    'variable': 'Q2'
                },
                {
                    'value': [1, 2, 3]
                }
            ]
        }

        expr = 'Q2.has_any(1)'
        with pytest.raises(ValueError):
            parse_expr(expr)

        expr = 'Q2.has_any(Q3)'
        with pytest.raises(ValueError):
            parse_expr(expr)

    def test_parse_has_all(self):
        expr = 'Q2.has_all([1, 2, 3])'
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'all',
            'args': [
                {
                    'variable': 'Q2'
                },
                {
                    'value': [1, 2, 3]
                }
            ]
        }

        expr = 'Q2.has_all((1, 2, 3))'
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'all',
            'args': [
                {
                    'variable': 'Q2'
                },
                {
                    'value': [1, 2, 3]
                }
            ]
        }

        expr = 'Q2.has_all(1)'
        with pytest.raises(ValueError):
            parse_expr(expr)

        expr = 'Q2.has_all(Q3)'
        with pytest.raises(ValueError):
            parse_expr(expr)

    def test_parse_has_count(self):
        expr = 'Q2.has_count(1)'
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'has_count',
            'args': [
                {
                    'variable': 'Q2'
                },
                {
                    'value': 1
                }
            ]
        }

        expr = 'Q2.has_count(1, 2)'
        with pytest.raises(ValueError):
            parse_expr(expr)

        expr = 'Q2.has_count([1,2])'
        with pytest.raises(ValueError):
            parse_expr(expr)

    def test_parse_omnibus_rule_2_complex(self):
        # Lets combine this with the previous one:
        # 'text': 'diposition code 0 (quotafull)',
        # 'index_mapper': intersection(
        #     [{'disposition': [0]}, {'exit_status': [1]}])
        expr = "(disposition == 0 and exit_status == 1) or " \
               "(disposition == 0 and exit_status == 0)"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'or',
            'args': [{
                    'function': 'and',
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
                                    'value': 1
                                }
                            ]
                        }
                    ]
                },
                {
                    'function': 'and',
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
            ]}

    def test_parse_omnibus_has_any(self):
        # 'text': 'CompanyTurnover is NA',
        # 'index_mapper': {'CompanyTurnover': has_any([99])}},

        # 'text': 'Not Private Sector',
        # 'index_mapper': {'sector': has_any([2, 3, 98, 99])}},
        expr = "CompanyTurnover.has_any([99])"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'any',
            'args': [
                {
                    'variable': 'CompanyTurnover'
                },
                {
                    'value': [99]
                }
            ]
        }

        expr = "sector.has_any([2, 3, 98, 99])"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'any',
            'args': [
                {
                    'variable': 'sector'
                },
                {
                    'value': [2, 3, 98, 99]
                }
            ]
        }

    def test_parse_negated_expr(self):
        expr = "not (age == 1)"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'not',
            'args': [
                {
                    'function': '==',
                    'args': [
                        {
                            'variable': 'age'
                        },
                        {
                            'value': 1
                        }
                    ]
                }
            ]
        }

    def test_parse_negated_method_call(self):
        expr = 'not Q2.has_any([1, 2, 3])'
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'not',
            'args': [
                {
                    'function': 'any',
                    'args': [
                        {
                            'variable': 'Q2'
                        },
                        {
                            'value': [1, 2, 3]
                        }
                    ]
                }
            ]
        }

        expr = 'not Q2.has_all([1, 2, 3])'
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'not',
            'args': [
                {
                    'function': 'all',
                    'args': [
                        {
                            'variable': 'Q2'
                        },
                        {
                            'value': [1, 2, 3]
                        }
                    ]
                }
            ]
        }

    def test_parse_duplicates_method(self):
        expr = "identity.duplicates()"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'duplicates',
            'args': [
                {
                    'variable': 'identity'
                }
            ]
        }

        # Negated.
        expr = "not identity.duplicates()"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'not',
            'args': [
                {
                    'function': 'duplicates',
                    'args': [
                        {
                            'variable': 'identity'
                        }
                    ]
                }
            ]
        }

        # Parameters not allowed.
        with pytest.raises(ValueError):
            parse_expr("identity.duplicates([1,2,3])")

        with pytest.raises(ValueError):
            parse_expr("identity.duplicates(1)")

        with pytest.raises(ValueError):
            parse_expr("identity.duplicates('hello')")

        with pytest.raises(ValueError):
            parse_expr("identity.duplicates(False)")

    def test_parse_helper_functions(self):
        # One variable.
        expr = "valid(birthyear)"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'is_valid',
            'args': [
                {
                    'variable': 'birthyear'
                }
            ]
        }

        expr = "missing(birthyear)"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'is_missing',
            'args': [
                {
                    'variable': 'birthyear'
                }
            ]
        }

        # One variable, negated.
        expr = "not valid(birthyear)"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'not',
            'args': [
                {
                    'function': 'is_valid',
                    'args': [
                        {
                            'variable': 'birthyear'
                        }
                    ]
                }
            ]
        }

        expr = "not missing(birthyear)"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'not',
            'args': [
                {
                    'function': 'is_missing',
                    'args': [
                        {
                            'variable': 'birthyear'
                        }
                    ]
                }
            ]
        }

        # Multiple variables.
        expr = "valid(birthyear, birthmonth)"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'and',
            'args': [
                {
                    'function': 'is_valid',
                    'args': [
                        {
                            'variable': 'birthyear'
                        }
                    ]
                },
                {
                    'function': 'is_valid',
                    'args': [
                        {
                            'variable': 'birthmonth'
                        }
                    ]
                }
            ]
        }

        expr = "missing(birthyear, birthmonth)"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'and',
            'args': [
                {
                    'function': 'is_missing',
                    'args': [
                        {
                            'variable': 'birthyear'
                        }
                    ]
                },
                {
                    'function': 'is_missing',
                    'args': [
                        {
                            'variable': 'birthmonth'
                        }
                    ]
                }
            ]
        }

        # Multiple variables, negated.
        expr = "not valid(birthyear, birthmonth)"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'not',
            'args': [
                {
                    'function': 'and',
                    'args': [
                        {
                            'function': 'is_valid',
                            'args': [
                                {
                                    'variable': 'birthyear'
                                }
                            ]
                        },
                        {
                            'function': 'is_valid',
                            'args': [
                                {
                                    'variable': 'birthmonth'
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        expr = "not missing(birthyear, birthmonth)"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'not',
            'args': [
                {
                    'function': 'and',
                    'args': [
                        {
                            'function': 'is_missing',
                            'args': [
                                {
                                    'variable': 'birthyear'
                                }
                            ]
                        },
                        {
                            'function': 'is_missing',
                            'args': [
                                {
                                    'variable': 'birthmonth'
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        # More advanced combinations.
        expr = "caseid < 12345 and missing(birthyear, birthmonth)"
        expr_obj = parse_expr(expr)
        assert expr_obj == {
            'function': 'and',
            'args': [
                {
                    'function': '<',
                    'args': [
                        {
                            'variable': 'caseid'
                        },
                        {
                            'value': 12345
                        }
                    ]
                },
                {
                    'function': 'and',
                    'args': [
                        {
                            'function': 'is_missing',
                            'args': [
                                {
                                    'variable': 'birthyear'
                                }
                            ]
                        },
                        {
                            'function': 'is_missing',
                            'args': [
                                {
                                    'variable': 'birthmonth'
                                }
                            ]
                        }
                    ]
                }
            ]
        }


# 'diposition code 0 (incompletes)':
# intersection(
#     [{'disposition': not_any([1])},
#      union([{'exit_status': has_count(0)},
#             {'exit_status': is_ge(1)}])
#      ]
# )




# 'text': 'sta: nicht aus Deutschland',
# 'index_mapper': {'sta': has_any([17])}},

# 'text': '(age >= 18) & profile_julesage is NaN',
#             'index_mapper': intersection(
#                 [
#                     {'age': is_ge(18)},
#                     {'profile_julesage': has_count(0)}])},

#'text': '(age >= 18) & profile_bpcagesex is NaN',
# 'index_mapper': intersection(
#     [{'age': is_ge(18)}, {'profile_bpcagesex': has_count(0)}])}],

# 'text': 'LONDON 18 NAN (profile_bpcagesex)',
# 'index_mapper': intersection(
#     [{'age': is_ge(18)}, {'profile_bpcagesex': has_count(0)}])},

# 'text': 'profile_GOR not code 11',
# 'index_mapper': {'profile_GOR': not_any([11])}}],

# 'text': '(age >= 18) & profile_julesage is NaN',
# 'index_mapper': intersection(
#     [{'age': is_ge(18)}, {'profile_julesage': has_count(0)}])},


# 'text': 'Not the right decision maker',
# 'index_mapper': {'DecisionMaking2': not_any(frange('1-10'))}},

# 'text': 'Duplicate identity',
# 'columns': 'identity',
# 'duplicated': True}])


# {  Drop anything missing (not asked/skipped/don't know/missing)
#     'text': 'DE PET OWNER NaN',
#     'columns': [
#                 'age_omnibus_18', 'gender',
#                 'nielsenregion', ''],
#     'dropna': True}


# { 'text': 'pets_omnibus not codes 1-4',
#     'index_mapper': {'pets_omnibus': not_any([1, 2, 3, 4])}}]


class TestExpressionProcessing(TestCase):

    @staticmethod
    def _build_get_func(**kwargs):
        props = {}
        props.update(kwargs)

        def _get(*args):
            return props.get(args[0], args[0])

        return _get

    def test_transform_alias_to_var_id(self):
        ds_url = 'http://test.crunch.io/api/datasets/123/'
        var_id = '0001'
        var_type = 'numeric'
        var_url = '%svariables/%s/' % (ds_url, var_id)

        # Mock the dataset.
        _get_func = self._build_get_func(id=var_id, type=var_type)
        ds = mock.MagicMock()
        ds.self = ds_url
        _var_mock = mock.MagicMock()
        _var_mock.entity.self = var_url
        _var_mock.__getitem__.side_effect = _get_func
        _var_mock.get.side_effect = _get_func
        ds.variables.by.return_value = {
            'age': _var_mock
        }

        expr_obj = process_expr(parse_expr('age == 1'), ds)

        assert expr_obj == {
            'function': '==',
            'args': [
                {
                    'variable': var_url
                },
                {
                    'value': 1
                }
            ]
        }

    def test_array_expansion_single_subvariable(self):
        ds_url = 'http://test.crunch.io/api/datasets/123/'
        var_id = '0001'
        var_type = 'categorical_array'
        var_url = '%svariables/%s/' % (ds_url, var_id)
        subvariables = [
            '%ssubvariables/0001/' % var_url
        ]

        # Mock the dataset.
        _get_func = self._build_get_func(
            id=var_id, type=var_type, subvariables=subvariables
        )
        ds = mock.MagicMock()
        ds.self = ds_url
        _var_mock = mock.MagicMock()
        _var_mock.entity.self = var_url
        _var_mock.__getitem__.side_effect = _get_func
        _var_mock.get.side_effect = _get_func

        _var_mock.subvariables = subvariables
        ds.variables.by.return_value = {
            'hobbies': _var_mock
        }

        # Single value.
        expr_obj = process_expr(parse_expr('hobbies.has_any([32766])'), ds)
        assert expr_obj == {
            'function': 'in',
            'args': [
                {
                    'variable': subvariables[0]
                },
                {
                    'value': [32766]
                }
            ]
        }

        expr_obj = process_expr(parse_expr('hobbies.has_all([32766])'), ds)
        assert expr_obj == {
            'function': '==',
            'args': [
                {
                    'variable': subvariables[0]
                },
                {
                    'value': 32766
                }
            ]
        }

        # Negated.
        expr_obj = process_expr(parse_expr('not hobbies.has_any([32766])'), ds)
        assert expr_obj == {
            'function': 'not',
            'args': [
                {
                    'function': 'in',
                    'args': [
                        {
                            'variable': subvariables[0]
                        },
                        {
                            'value': [32766]
                        }
                    ]
                }

            ]
        }

        expr_obj = process_expr(parse_expr('not hobbies.has_all([32766])'), ds)
        assert expr_obj == {
            'function': 'not',
            'args': [
                {
                    'function': '==',
                    'args': [
                        {
                            'variable': subvariables[0]
                        },
                        {
                            'value': 32766
                        }
                    ]
                }

            ]
        }

        # Multiple values.
        expr_obj = process_expr(parse_expr('hobbies.has_any([32766, 32767])'), ds)
        assert expr_obj == {
            'function': 'in',
            'args': [
                {
                    'variable': subvariables[0]
                },
                {
                    'value': [32766, 32767]
                }
            ]
        }

        with pytest.raises(ValueError):
            process_expr(parse_expr('hobbies.has_all([32766, 32767])'), ds)

    def test_array_expansion_multiple_subvariables(self):
        ds_url = 'http://test.crunch.io/api/datasets/123/'
        var_id = '0001'
        var_type = 'categorical_array'
        var_url = '%svariables/%s/' % (ds_url, var_id)
        subvariables = [
            '%ssubvariables/0001/' % var_url,
            '%ssubvariables/0002/' % var_url,
            '%ssubvariables/0003/' % var_url,
            '%ssubvariables/0004/' % var_url
        ]

        # Mock the dataset.
        _get_func = self._build_get_func(
            id=var_id, type=var_type, subvariables=subvariables
        )
        ds = mock.MagicMock()
        ds.self = ds_url
        _var_mock = mock.MagicMock()
        _var_mock.entity.self = var_url
        _var_mock.__getitem__.side_effect = _get_func
        _var_mock.get.side_effect = _get_func

        _var_mock.subvariables = subvariables
        ds.variables.by.return_value = {
            'hobbies': _var_mock
        }

        # Single values.
        expr = 'hobbies.has_any([32766])'
        expr_obj = process_expr(parse_expr(expr), ds)
        assert expr_obj == {
            'function': 'or',
            'args': [
                {
                    'function': 'in',
                    'args': [
                        {
                            'variable': subvariables[0]
                        },
                        {
                            'value': [32766]
                        }
                    ]
                },
                {
                    'function': 'or',
                    'args': [
                        {
                            'function': 'in',
                            'args': [
                                {
                                    'variable': subvariables[1]
                                },
                                {
                                    'value': [32766]
                                }
                            ]
                        },
                        {
                            'function': 'or',
                            'args': [
                                {
                                    'function': 'in',
                                    'args': [
                                        {
                                            'variable': subvariables[2]
                                        },
                                        {
                                            'value': [32766]
                                        }
                                    ]
                                },
                                {
                                    'function': 'in',
                                    'args': [
                                        {
                                            'variable': subvariables[3]
                                        },
                                        {
                                            'value': [32766]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        expr = 'hobbies.has_all([32766])'
        expr_obj = process_expr(parse_expr(expr), ds)
        assert expr_obj == {
            'function': 'and',
            'args': [
                {
                    'function': '==',
                    'args': [
                        {
                            'variable': subvariables[0]
                        },
                        {
                            'value': 32766
                        }
                    ]
                },
                {
                    'function': 'and',
                    'args': [
                        {
                            'function': '==',
                            'args': [
                                {
                                    'variable': subvariables[1]
                                },
                                {
                                    'value': 32766
                                }
                            ]
                        },
                        {
                            'function': 'and',
                            'args': [
                                {
                                    'function': '==',
                                    'args': [
                                        {
                                            'variable': subvariables[2]
                                        },
                                        {
                                            'value': 32766
                                        }
                                    ]
                                },
                                {
                                    'function': '==',
                                    'args': [
                                        {
                                            'variable': subvariables[3]
                                        },
                                        {
                                            'value': 32766
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        # Negated.
        expr = 'not hobbies.has_any([32766])'
        expr_obj = process_expr(parse_expr(expr), ds)
        assert expr_obj == {
            'function': 'not',
            'args': [
                {
                    'function': 'or',
                    'args': [
                        {
                            'function': 'in',
                            'args': [
                                {
                                    'variable': subvariables[0]
                                },
                                {
                                    'value': [32766]
                                }
                            ]
                        },
                        {
                            'function': 'or',
                            'args': [
                                {
                                    'function': 'in',
                                    'args': [
                                        {
                                            'variable': subvariables[1]
                                        },
                                        {
                                            'value': [32766]
                                        }
                                    ]
                                },
                                {
                                    'function': 'or',
                                    'args': [
                                        {
                                            'function': 'in',
                                            'args': [
                                                {
                                                    'variable': subvariables[2]
                                                },
                                                {
                                                    'value': [32766]
                                                }
                                            ]
                                        },
                                        {
                                            'function': 'in',
                                            'args': [
                                                {
                                                    'variable': subvariables[3]
                                                },
                                                {
                                                    'value': [32766]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        expr = 'not hobbies.has_all([32766])'
        expr_obj = process_expr(parse_expr(expr), ds)
        assert expr_obj == {
            'function': 'not',
            'args': [
                {
                    'function': 'and',
                    'args': [
                        {
                            'function': '==',
                            'args': [
                                {
                                    'variable': subvariables[0]
                                },
                                {
                                    'value': 32766
                                }
                            ]
                        },
                        {
                            'function': 'and',
                            'args': [
                                {
                                    'function': '==',
                                    'args': [
                                        {
                                            'variable': subvariables[1]
                                        },
                                        {
                                            'value': 32766
                                        }
                                    ]
                                },
                                {
                                    'function': 'and',
                                    'args': [
                                        {
                                            'function': '==',
                                            'args': [
                                                {
                                                    'variable': subvariables[2]
                                                },
                                                {
                                                    'value': 32766
                                                }
                                            ]
                                        },
                                        {
                                            'function': '==',
                                            'args': [
                                                {
                                                    'variable': subvariables[3]
                                                },
                                                {
                                                    'value': 32766
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        # Multiple values.
        expr = 'hobbies.has_any([32766, 32767])'
        expr_obj = process_expr(parse_expr(expr), ds)
        assert expr_obj == {
            'function': 'or',
            'args': [
                {
                    'function': 'in',
                    'args': [
                        {
                            'variable': subvariables[0]
                        },
                        {
                            'value': [32766, 32767]
                        }
                    ]
                },
                {
                    'function': 'or',
                    'args': [
                        {
                            'function': 'in',
                            'args': [
                                {
                                    'variable': subvariables[1]
                                },
                                {
                                    'value': [32766, 32767]
                                }
                            ]
                        },
                        {
                            'function': 'or',
                            'args': [
                                {
                                    'function': 'in',
                                    'args': [
                                        {
                                            'variable': subvariables[2]
                                        },
                                        {
                                            'value': [32766, 32767]
                                        }
                                    ]
                                },
                                {
                                    'function': 'in',
                                    'args': [
                                        {
                                            'variable': subvariables[3]
                                        },
                                        {
                                            'value': [32766, 32767]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        # Multiple values, negated
        expr = 'not hobbies.has_any([32766, 32767])'
        expr_obj = process_expr(parse_expr(expr), ds)
        assert expr_obj == {
            'function': 'not',
            'args': [
                {
                    'function': 'or',
                    'args': [
                        {
                            'function': 'in',
                            'args': [
                                {
                                    'variable': subvariables[0]
                                },
                                {
                                    'value': [32766, 32767]
                                }
                            ]
                        },
                        {
                            'function': 'or',
                            'args': [
                                {
                                    'function': 'in',
                                    'args': [
                                        {
                                            'variable': subvariables[1]
                                        },
                                        {
                                            'value': [32766, 32767]
                                        }
                                    ]
                                },
                                {
                                    'function': 'or',
                                    'args': [
                                        {
                                            'function': 'in',
                                            'args': [
                                                {
                                                    'variable': subvariables[2]
                                                },
                                                {
                                                    'value': [32766, 32767]
                                                }
                                            ]
                                        },
                                        {
                                            'function': 'in',
                                            'args': [
                                                {
                                                    'variable': subvariables[3]
                                                },
                                                {
                                                    'value': [32766, 32767]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

    def test_valid_and_missing_funcs_for_arrays(self):
        ds_url = 'http://test.crunch.io/api/datasets/123/'
        var_id = '0001'
        var_type = 'categorical_array'
        var_url = '%svariables/%s/' % (ds_url, var_id)
        subvariables = [
            '%ssubvariables/0001/' % var_url,
            '%ssubvariables/0002/' % var_url,
            '%ssubvariables/0003/' % var_url,
            '%ssubvariables/0004/' % var_url
        ]

        # Mock the dataset.
        _get_func = self._build_get_func(
            id=var_id, type=var_type, subvariables=subvariables
        )
        ds = mock.MagicMock()
        ds.self = ds_url
        _var_mock = mock.MagicMock()
        _var_mock.entity.self = var_url
        _var_mock.__getitem__.side_effect = _get_func
        _var_mock.get.side_effect = _get_func

        _var_mock.subvariables = subvariables
        ds.variables.by.return_value = {
            'hobbies': _var_mock
        }

        expr = 'valid(hobbies)'
        expr_obj = process_expr(parse_expr(expr), ds)
        assert expr_obj == {
            'function': 'all_valid',
            'args': [
                {
                    'variable': var_url
                }
            ]
        }

        expr = 'not valid(hobbies)'
        expr_obj = process_expr(parse_expr(expr), ds)
        assert expr_obj == {
            'function': 'not',
            'args': [
                {
                    'function': 'all_valid',
                    'args': [
                        {
                            'variable': var_url
                        }
                    ]
                }
            ]
        }

        expr = 'missing(hobbies)'
        expr_obj = process_expr(parse_expr(expr), ds)
        assert expr_obj == {
            'function': 'all_missing',
            'args': [
                {
                    'variable': var_url
                }
            ]
        }

        expr = 'not missing(hobbies)'
        expr_obj = process_expr(parse_expr(expr), ds)
        assert expr_obj == {
            'function': 'not',
            'args': [
                {
                    'function': 'all_missing',
                    'args': [
                        {
                            'variable': var_url
                        }
                    ]
                }
            ]
        }
