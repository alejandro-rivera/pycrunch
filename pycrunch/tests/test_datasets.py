import json

from unittest import TestCase
from unittest import mock

from pycrunch.datasets import exclusion


class TestExclusionFilters(TestCase):

    ds_url = 'http://test.crunch.io/api/datasets/123/'

    def test_apply_exclusion(self):
        """
        Tests that the proper PATCH request is sent to Crunch in order to
        apply an exclusion filter to a dataset.
        """
        var_id = '0001'
        var_type = 'numeric'
        var_url = '%svariables/%s/' % (self.ds_url, var_id)

        # Mocking setup.
        def _get(*args):
            if args[0] == 'id':
                return var_id
            if args[0] == 'type':
                return var_type
            return args[0]

        ds = mock.MagicMock()
        ds.fragments.exclusion = '%sexclusion/' % self.ds_url
        ds.self = self.ds_url
        _var_mock = mock.MagicMock()
        _var_mock.entity.self = var_url
        _var_mock.__getitem__.side_effect = _get
        _var_mock.get.side_effect = _get
        ds.variables.by.return_value = {
            'disposition': _var_mock
        }

        # Action!
        exclusion_filter = 'disposition != 0'
        exclusion(ds, exclusion_filter)

        # Ensure .patch was called the right way.
        assert len(ds.session.patch.call_args_list) == 1

        call = ds.session.patch.call_args_list[0]
        assert call[0][0] == ds.fragments.exclusion

        expected_expr_obj = {
            'expression': {
                'function': '!=',
                'args': [
                    {'variable': var_url},  # Crunch needs variable URLs!
                    {'value': 0}
                ]
            }
        }
        assert json.loads(call[1]['data']) == expected_expr_obj

    def test_remove_exclusion(self):
        """
        Tests that the proper PATCH request is sent to Crunch in order to
        clear (i.e. remove) the exclusion filter from a dataset.
        """
        ds = mock.MagicMock()
        ds.fragments.exclusion = '%sexclusion/' % self.ds_url

        exclusion(ds)

        ds.session.patch.assert_called_once_with(
            ds.fragments.exclusion,
            data=json.dumps({'expression': {}})
        )
