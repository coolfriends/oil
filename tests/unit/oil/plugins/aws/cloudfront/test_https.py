import unittest

from oil.plugins.aws.cloudfront import HTTPSPlugin

class HTTPSPluginTestCase(unittest.TestCase):

    def test_can_be_initialized_and_run_with_no_config(self):
        data_fixture = {
            'aws': {
                'cloudfront': {
                    'aws-global': {
                        'list_distributions': [
                            {
                                'ARN': 'arn1',
                            }
                        ]
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
                    'aws-global': {
                        'list_distributions': [
                            {
                                'ARN': 'arn1',
                            }
                        ]
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
            'ARN': 'arn1',
            'ViewerProtocolPolicy': 'allow-all'
        }
        distribution2_fixture = {
            'ARN': 'arn2',
            'ViewerProtocolPolicy': 'allow-all'
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

        self.assertCountEqual(results, expected)

    def test_no_viewer_policy(self):
        api_data_fixture = {
            'aws': {
                'cloudfront': {
                    'aws-global': {
                        'list_distributions': [
                            {
                                'ARN': 'anarn'
                            }
                        ]
                    }
                }
            }
        }

        plugin = HTTPSPlugin()
        results = plugin.run(api_data_fixture)
        expected = [{
            'resource': 'anarn',
            'region': 'aws-global',
            'severity': 0,
            'message': 'No viewer policy found for this distribution'
        }]
        results_keys = list(results[0].keys())
        expected = [
            'resource',
            'severity',
            'message',
            'region'
        ]

        self.assertCountEqual(results_keys, expected)

    def test_unsupported_viewer_policy(self):
        api_data_fixture = {
            'aws': {
                'cloudfront': {
                    'aws-global': {
                        'list_distributions': [
                            {
                                'ARN': 'anarn',
                                'DefaultCacheBehavior': {
                                    'ViewerProtocolPolicy': 'unsupported-policy'
                                }
                            }
                        ]
                    }
                }
            }
        }

        plugin = HTTPSPlugin()
        results = plugin.run(api_data_fixture)
        expected = [{
            'resource': 'anarn',
            'region': 'aws-global',
            'severity': 3,
            'message': 'Unsupported ViewerProtocolPolicy of unsupported-policy'
        }]

        self.assertEqual(results, expected)

    def test_allow_all_viewer_policy(self):
        api_data_fixture = {
            'aws': {
                'cloudfront': {
                    'aws-global': {
                        'list_distributions': [
                            {
                                'ARN': 'anarn',
                                'DefaultCacheBehavior': {
                                    'ViewerProtocolPolicy': 'allow-all'
                                }
                            }
                        ]
                    }
                }
            }
        }

        plugin = HTTPSPlugin()
        results = plugin.run(api_data_fixture)
        expected = [{
            'resource': 'anarn',
            'region': 'aws-global',
            'severity': 2,
            'message': 'Distribution should only allow HTTPS traffic'
        }]

        self.assertEqual(results, expected)

    def test_redirect_to_https_viewer_policy(self):
        api_data_fixture = {
            'aws': {
                'cloudfront': {
                    'aws-global': {
                        'list_distributions': [
                            {
                                'ARN': 'anarn',
                                'DefaultCacheBehavior': {
                                    'ViewerProtocolPolicy': 'redirect-to-https'
                                }
                            }
                        ]
                    }
                }
            }
        }

        plugin = HTTPSPlugin()
        results = plugin.run(api_data_fixture)
        expected = [{
            'resource': 'anarn',
            'region': 'aws-global',
            'severity': 0,
            'message': (
                'Distribution is properly configured to redirect HTTP '
                'traffic to HTTPS'
            )
        }]

        self.assertEqual(results, expected)

    def test_https_only_viewer_policy(self):
        api_data_fixture = {
            'aws': {
                'cloudfront': {
                    'aws-global': {
                        'list_distributions': [
                            {
                                'ARN': 'anarn',
                                'DefaultCacheBehavior': {
                                    'ViewerProtocolPolicy': 'https-only'
                                }
                            }
                        ]
                    }
                }
            }
        }

        plugin = HTTPSPlugin()
        results = plugin.run(api_data_fixture)
        expected = [{
            'resource': 'anarn',
            'region': 'aws-global',
            'severity': 0,
            'message': (
                'Distribution is properly configured to only allow HTTPS traffic'
            )
        }]

        self.assertEqual(results, expected)
