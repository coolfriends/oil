import unittest

from oil.plugins import Plugin


class PluginTestCase(unittest.TestCase):
    def test_collect_throws_error_with_bad_provider_for_requirement(self):
        plugin = Plugin({})
        plugin.requirements = {
            'any-requirement-name': ['bad-provider', 'any-service', 'any-call']
        }
        api_data_fixture = {
            'good-provider': {
                'any-service': {
                    'any-region': {
                        'any-call': []
                    }
                }
            }
        }

        with self.assertRaises(RuntimeError):
            plugin.collect_requirements(api_data_fixture)

    def test_collect_throws_error_with_bad_service_for_requirement(self):
        plugin = Plugin({})

        plugin.requirements = {
            'any-requirement-name': ['good-provider', 'bad-service', 'any-call']
        }
        api_data_fixture = {
            'good-provider': {
                'good-service': {
                    'any-region': {
                        'any-call': []
                    }
                }
            }
        }

        with self.assertRaises(RuntimeError):
            plugin.collect_requirements(api_data_fixture)

    def test_collect_throws_error_with_bad_call_for_requirement(self):
        plugin = Plugin({})

        plugin.requirements = {
            'any-requirement-name': ['good-provider', 'good-service', 'bad-call']
        }
        api_data_fixture = {
            'good-provider': {
                'good-service': {
                    'any-region': {
                        'good-call': []
                    }
                }
            }
        }

        with self.assertRaises(RuntimeError) as cm:
            collected_data = plugin.collect_requirements(api_data_fixture)

    def test_can_collect_and_name_requirements_from_api_data_empty_call(self):
        plugin = Plugin({})
        plugin.requirements = {
            'any-requirement-name': ['any-provider', 'any-service', 'any-call']
        }
        api_data_fixture = {
            'any-provider': {
                'any-service': {
                    'any-region': {
                        'any-call': []
                    }
                }
            }
        }

        collected_data = plugin.collect_requirements(api_data_fixture)
        expected = {
            'any-requirement-name': {
                'any-region': []
            }
        }
        self.assertEqual(collected_data, expected)

    def test_can_collect_requirements_from_api_data_using_call_data(self):
        plugin = Plugin({})
        plugin.requirements = {
            'any-requirement-name': ['any-provider', 'any-service', 'any-call']
        }
        api_data_fixture = {
            'any-provider': {
                'any-service': {
                    'any-region': {
                        'any-call': [
                            {
                                'any-key': 'any-value'
                            }
                        ]
                    }
                }
            }
        }

        collected_data = plugin.collect_requirements(api_data_fixture)
        expected = {
            'any-requirement-name': {
                'any-region': [
                    {
                        'any-key': 'any-value'
                    }
                ]
            }
        }
        self.assertEqual(collected_data, expected)
