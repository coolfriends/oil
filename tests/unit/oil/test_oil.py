import unittest
from unittest.mock import patch, MagicMock

from oil import Oil
from oil.barrels.aws import CloudFrontBarrel


class OilTestCase(unittest.TestCase):

    def test_can_take_sts_credentials(self):
        oil = Oil(
            aws_access_key_id='my_id',
            aws_secret_access_key='my_key',
            session_token='my_token',
        )
        self.assertEqual(oil.aws_access_key_id, 'my_id')
        self.assertEqual(oil.aws_secret_access_key, 'my_key')
        self.assertEqual(oil.session_token, 'my_token')

    def test_validates_good_kwargs(self):
        valid_args = {
            'aws_access_key_id': 'my_id',
            'aws_secret_access_key': 'my_key',
            'session_token': 'session_token',
        }
        oil = Oil()
        oil._validate_kwargs(**valid_args)

    def test_oil_throws_error_with_bad_kwargs(self):
        with self.assertRaises(RuntimeError):
            Oil(bad_arg='my_bad_arg')

    def test_validate_kwargs_throws_error_with_bad_kwargs(self):
        oil = Oil()
        with self.assertRaises(RuntimeError):
            oil._validate_kwargs(bad_arg='my_bad_arg')

    def test_unique_api_calls(self):
        oil = Oil()
        plugin_mock_1 = MagicMock()
        plugin_mock_1.requirements = {
            'distributions': ['aws', 'cloudfront', 'list_distributions'],
            'instances': ['aws', 'ec2', 'describe_instances'],
        }

        plugin_mock_2 = MagicMock()
        plugin_mock_2.requirements = {
            'distributions': ['aws', 'cloudfront', 'list_distributions'],
            'other_distributions': ['aws', 'cloudfront', 'other_distributions'],
            'instances': ['aws', 'ec2', 'describe_instances'],
        }

        oil.plugins = {
            'aws': {
                'cloudfront': {
                    'plugin_1': plugin_mock_1,
                    'plugin_2': plugin_mock_2,
                }
            }
        }

        calls = oil._unique_api_calls()
        self.assertEqual(
            calls['aws']['cloudfront'],
            set(['list_distributions', 'other_distributions'])
        )
        self.assertEqual(
            calls['aws']['ec2'],
            set(['describe_instances'])
        )

    @patch('oil.Oil.get_barrel')
    def test_collect_api_data_organizes_data_correctly(self, get_barrel_mock):
        barrel_mock = MagicMock()
        barrel_mock.tap.return_value = {
            'any_region': []
        }
        get_barrel_mock.return_value = barrel_mock

        expected = {
            'aws': {
                'cloudfront': {
                    'any_region': {
                        'list_distributions': []
                    }
                }
            }
        }

        oil = Oil()
        oil._collect_api_data('aws', 'cloudfront', 'list_distributions')
        self.assertEqual(oil.cached_api_data, expected)
