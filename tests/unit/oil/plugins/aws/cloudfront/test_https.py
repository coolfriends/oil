import unittest

from oil.plugins.aws.cloudfront import HTTPSPlugin

class HTTPSPluginTestCase(unittest.TestCase):

    def test_can_be_initialized_and_run_with_no_config(self):
        data_fixture = {
            'aws': {
                'cloudfront': {
                    'aws-global': {
                        'list_distributions': [{}]
                    }
                }
            }
        }

        plugin = HTTPSPlugin()
        results = plugin.run(data_fixture)
        results_keys = list(results[0].keys())
        expected = [
            'resource',
            'severity',
            'message',
            'region'
        ]

        self.assertCountEqual(results_keys, expected)

    def test_can_be_initialized_and_run_with_empty_config(self):
        data_fixture = {
            'aws': {
                'cloudfront': {
                    'us-east-1': {
                        'list_distributions': [{}]
                    }
                }
            }
        }

        plugin = HTTPSPlugin({})
        results = plugin.run(data_fixture)
        results_keys = list(results[0].keys())
        expected = [
            'resource',
            'severity',
            'message',
            'region'
        ]

        self.assertCountEqual(results_keys, expected)

    def test_creates_results_with_correct_fields_for_multiple_distributions(self):
        distribution1_fixture = {
        }
        distribution2_fixture = {
        }

        distributions = [distribution1_fixture, distribution2_fixture]
        data_fixture = {
            'aws': {
                'cloudfront': {
                    'aws-global': {
                        'list_distributions': distributions
                    }
                }
            }
        }

        plugin = HTTPSPlugin()
        results = plugin.run(data_fixture)
        results_keys = list(results[0].keys())
        expected = [
            'resource',
            'severity',
            'message',
            'region'
        ]

        self.assertCountEqual(results_keys, expected)

    def test_only_one_sensible_result_if_no_distributions(self):
        api_data_fixture = {
            'aws': {
                'cloudfront': {
                    'aws-global': {
                        'list_distributions': []
                    }
                }
            }
        }

        plugin = HTTPSPlugin()
        results = plugin.run(api_data_fixture)
        expected = [{
            'resource': 'None',
            'region': 'aws-global',
            'severity': 0,
            'message': 'No distributions found'
            }]
        results_keys = list(results[0].keys())
        expected = [
            'resource',
            'severity',
            'message',
            'region'
        ]

        self.assertCountEqual(results_keys, expected)
