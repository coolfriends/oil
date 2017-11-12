import unittest
from unittest.mock import patch, MagicMock

from oil import Oil
from oil.barrels.aws import CloudFrontBarrel


class OilTestCase(unittest.TestCase):

    def test_providers_are_default_with_no_config_passed(self):
        oil = Oil()
        providers = oil.providers
        self.assertEqual(providers, ['aws'])

        self.assertCountEqual(oil.services('aws'), ['ec2', 'cloudfront'])

    def test_add_config_post_initialization_configures_plugins(self):
        oil = Oil()
        config = {
            'aws': {
                'cloudfront': {
                    'plugins': [
                        {
                            'name': 'tls_protocol'
                        }
                    ]
                }
            }
        }

        oil.configure(config)
        self.assertEqual(oil.config, config)

        plugin = oil.plugins[0]
        self.assertEqual(plugin.name, 'tls_protocol')

    def test_services_throws_error_with_unsupported_provider(self):
        oil = Oil()
        with self.assertRaises(RuntimeError):
            services = oil.services('unsupported_provider')

    def test_services_empty_with_no_services(self):
        config = {
            'aws': {}
        }
        oil = Oil(config)
        with self.assertRaises(RuntimeError):
            services = oil.services('unsupported_provider')

    def test_loading_plugins_throws_error_if_provider_is_not_registered(self):
        config = {
            'unsupported_provider': {
                'this': {
                    'plugins': []
                }
            }
        }

        with self.assertRaises(RuntimeError):
            oil = Oil(config)

    def test_loading_plugins_throws_error_if_service_is_not_registered(self):
        config = {
            'aws': {
                'unsupported_service': {
                    'plugins': []
                }
            }
        }

        with self.assertRaises(RuntimeError):
            oil = Oil(config)

    def test_loading_plugins_throws_error_if_plugin_is_not_registered(self):
        config = {
            'aws': {
                'cloudfront': {
                    'plugins': [
                        {
                            'name': 'fake_plugin'
                        }
                    ]
                }
            }
        }

        with self.assertRaises(RuntimeError):
            oil = Oil(config)

    def test_loading_barrels_can_find_good_barrel(self):
        plugin_mock = MagicMock()
        plugin_mock.provider = 'good_provider'
        plugin_mock.service = 'good_service'
        barrel_mock = MagicMock()
        barrel_mock.provider = 'good_provider'
        barrel_mock.service = 'good_service'
        barrel_wrapper_mock = MagicMock()
        barrel_wrapper_mock.provider = 'good_provider'
        barrel_wrapper_mock.service = 'good_service'
        barrel_wrapper_mock.return_value = barrel_mock
        oil = Oil()
        oil.plugins = [plugin_mock]
        oil.available_barrels = [barrel_wrapper_mock]

        oil._load_barrels()
        self.assertEqual(oil.barrels[0].service, barrel_mock.service)

    def test_loading_barrels_throws_error_if_barrel_not_found(self):
        plugin_mock = MagicMock()
        plugin_mock.provider = 'good_provider'
        plugin_mock.service = 'good_service'
        oil = Oil()
        oil.plugins = [plugin_mock]
        oil.available_barrels = []

        with self.assertRaises(RuntimeError):
            oil._load_barrels()

    def test_get_barrel_maps_cloudfront_to_correct_barrel(self):
        config = {
            'aws': {
                'cloudfront': {
                    'plugins': [
                        {
                            'name': 'tls_protocol'
                        }
                    ]
                }
            }
        }

        oil = Oil(config)
        barrel = oil.get_barrel('aws', 'cloudfront')

        self.assertIsInstance(barrel, CloudFrontBarrel)

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

        oil.plugins = [
            plugin_mock_1,
            plugin_mock_2,
        ]

        calls = oil._unique_api_calls()
        self.assertEqual(
            calls['aws']['cloudfront'],
            set(['list_distributions', 'other_distributions'])
        )
        self.assertEqual(
            calls['aws']['ec2'],
            set(['describe_instances'])
        )




    def test_get_barrel_raises_runtime_error_on_fail(self):
        config = {
            'aws': {
                'cloudfront': {
                    'plugins': [
                        {
                            'name': 'tls_protocol'
                        }
                    ]
                }
            }
        }

        oil = Oil(config)
        with self.assertRaises(RuntimeError):
            barrel = oil.get_barrel('aws', 'not_a_service')

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
