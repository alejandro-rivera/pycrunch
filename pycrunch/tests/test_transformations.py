from unittest import TestCase
from unittest import mock

from pycrunch.transformations import create_categorical


categories = [
    {"id": 3, "name": "Hipsters", "numeric_value": None, "missing": False},
    {"id": 1, "name": "Techies", "numeric_value": None, "missing": False},
    {"id": 2, "name": "Yuppies", "numeric_value": None, "missing": False}]

rules = ['gender == 1', 'gender == 2']


class TestCreateCategorical(TestCase):

    ds_url = 'http://test.crunch.io/api/datasets/123/'

    def test_create_categorical(self):
        var_id = '0001'
        var_type = 'categorical'
        var_url = '%svariables/%s/' % (self.ds_url, var_id)

        # Mocking setup.
        def _get(*args):
            if args[0] == 'id':
                return var_id
            if args[0] == 'type':
                return var_type
            return args[0]

        ds = mock.MagicMock()
        ds.self = self.ds_url
        _var_mock = mock.MagicMock()
        _var_mock.entity.self = var_url
        _var_mock.__getitem__.side_effect = _get
        _var_mock.get.side_effect = _get
        ds.variables.by.return_value = {
            'gender': _var_mock
        }

        test = create_categorical(ds, categories, rules, 'name', 'alias', 'description')
        call = ds.variables.create.call_args_list[0][0][0]
        payload = {
          "body": {
            "name": "name",
            "alias": "alias",
            "description": "description",
            "expr": {
              "function": "case",
              "args": [
                {
                  "column": [
                    3,
                    1,
                    2
                  ],
                  "type": {
                    "value": {
                      "categories": [
                        {
                          "name": "Hipsters",
                          "id": 3,
                          "numeric_value": None,
                          "missing": False
                        },
                        {
                          "name": "Techies",
                          "id": 1,
                          "numeric_value": None,
                          "missing": False
                        },
                        {
                          "name": "Yuppies",
                          "id": 2,
                          "numeric_value": None,
                          "missing": False
                        }
                      ],
                      "class": "categorical"
                    }
                  }
                },
                {
                  "function": "==",
                  "args": [
                    {
                      "variable": "http://test.crunch.io/api/datasets/123/variables/0001/"
                    },
                    {
                      "value": 1
                    }
                  ]
                },
                {
                  "function": "==",
                  "args": [
                    {
                      "variable": "http://test.crunch.io/api/datasets/123/variables/0001/"
                    },
                    {
                      "value": 2
                    }
                  ]
                }
              ]
            }
          },
          "element": "shoji:entity"
        }
        assert call == payload
