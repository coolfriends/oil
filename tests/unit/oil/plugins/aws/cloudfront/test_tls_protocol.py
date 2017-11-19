import unittest

from oil.plugins.aws.cloudfront import TLSProtocolPlugin


class TLSProtocolPluginTestCase(unittest.TestCase):

    def test_can_be_initialized_and_run_with_no_config(self):
        data_fixture = {
            'aws': {
                'cloudfront': {
                    'aws-global': {
                        'list_distributions': [
                        ]
                    }
                }
            }
        }

        plugin = TLSProtocolPlugin({})
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
                        'list_distributions': []
                    }
                }
            }
        }

        plugin = TLSProtocolPlugin({})
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
        }
        distribution2_fixture = {
            'ARN': 'arn2',
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

        plugin = TLSProtocolPlugin({})
        results = plugin.run(data_fixture)
        results_keys = list(results[0].keys())
        expected = [
            'resource',
            'severity',
            'message',
            'region'
        ]

        self.assertCountEqual(results_keys, expected)

    def test_no_distributions(self):
        api_data_fixture = {
            'aws': {
                'cloudfront': {
                    'aws-global': {
                        'list_distributions': []
                    }
                }
            }
        }

        plugin = TLSProtocolPlugin({})
        results = plugin.run(api_data_fixture)
        expected = [{
            'resource': 'None',
            'region': 'aws-global',
            'severity': 0,
            'message': 'No distributions found'
            }]

        self.assertEqual(results, expected)

    def test_no_protocol_version(self):
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

        plugin = TLSProtocolPlugin({})
        results = plugin.run(api_data_fixture)
        expected = [{
            'resource': 'anarn',
            'region': 'aws-global',
            'severity': 3,
            'message': 'No protocol version found'
        }]

        self.assertEqual(results, expected)

    def test_severity_2_protocol(self):
        api_data_fixture = {
            'aws': {
                'cloudfront': {
                    'aws-global': {
                        'list_distributions': [
                            {
                                'ARN': 'anarn',
                                'ViewerCertificate': {
                                    'MinimumProtocolVersion': 'SSLv3'
                                }
                            }
                        ]
                    }
                }
            }
        }

        plugin = TLSProtocolPlugin({})
        results = plugin.run(api_data_fixture)
        expected = [{
            'resource': 'anarn',
            'region': 'aws-global',
            'severity': 2,
            'message': 'SSLv3 is insecure'
        }]

        self.assertEqual(results, expected)

    def test_severity_1_protocol(self):
        api_data_fixture = {
            'aws': {
                'cloudfront': {
                    'aws-global': {
                        'list_distributions': [
                            {
                                'ARN': 'anarn',
                                'ViewerCertificate': {
                                    'MinimumProtocolVersion': 'TLSv1'
                                }
                            }
                        ]
                    }
                }
            }
        }

        plugin = TLSProtocolPlugin({})
        results = plugin.run(api_data_fixture)
        expected = [{
            'resource': 'anarn',
            'region': 'aws-global',
            'severity': 1,
            'message': 'TLSv1 is not considered best practice'
        }]

        self.assertEqual(results, expected)

    def test_severity_0_protocol(self):
        api_data_fixture = {
            'aws': {
                'cloudfront': {
                    'aws-global': {
                        'list_distributions': [
                            {
                                'ARN': 'anarn',
                                'ViewerCertificate': {
                                    'MinimumProtocolVersion': 'TLSv1.1_2016'
                                }
                            }
                        ]
                    }
                }
            }
        }

        plugin = TLSProtocolPlugin({})
        results = plugin.run(api_data_fixture)
        expected = [{
            'resource': 'anarn',
            'region': 'aws-global',
            'severity': 0,
            'message': 'TLSv1.1_2016 is secure and considered best practice'
        }]

        self.assertEqual(results, expected)

    def test_unexpected_protocol(self):
        api_data_fixture = {
            'aws': {
                'cloudfront': {
                    'aws-global': {
                        'list_distributions': [
                            {
                                'ARN': 'anarn',
                                'ViewerCertificate': {
                                    'MinimumProtocolVersion': 'not-expected'
                                }
                            }
                        ]
                    }
                }
            }
        }

        plugin = TLSProtocolPlugin({})
        results = plugin.run(api_data_fixture)
        expected = [{
            'resource': 'anarn',
            'region': 'aws-global',
            'severity': 3,
            'message': 'not-expected is an unexpected protocol'
        }]

        self.assertEqual(results, expected)
