import unittest

from oil.plugins.aws.cloudfront import S3OriginAccessIdentityPlugin

class S3OriginAccessIdentityPluginTestCase(unittest.TestCase):

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

        plugin = S3OriginAccessIdentityPlugin()
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

        plugin = S3OriginAccessIdentityPlugin({})
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

        plugin = S3OriginAccessIdentityPlugin()
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

        plugin = S3OriginAccessIdentityPlugin()
        results = plugin.run(api_data_fixture)
        expected = [{
            'resource': 'None',
            'region': 'aws-global',
            'severity': 0,
            'message': 'No distributions found'
            }]

        self.assertCountEqual(results, expected)

    def test_no_origins(self):
        api_data_fixture = {
            'aws': {
                'cloudfront': {
                    'aws-global': {
                        'list_distributions': [
                            {
                                'ARN': 'anarn',
                                'Origins': {
                                    'Items': []
                                }
                            }
                        ]
                    }
                }
            }
        }

        plugin = S3OriginAccessIdentityPlugin()
        results = plugin.run(api_data_fixture)
        expected = [{
            'resource': 'anarn',
            'region': 'aws-global',
            'severity': 0,
            'message': 'No origins found for this distribution'
        }]

        self.assertCountEqual(results, expected)

    def test_no_s3_origin(self):
        api_data_fixture = {
            'aws': {
                'cloudfront': {
                    'aws-global': {
                        'list_distributions': [
                            {
                                'ARN': 'anarn',
                                'Origins': {
                                    'Items': [
                                        {
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                }
            }
        }

        plugin = S3OriginAccessIdentityPlugin()
        results = plugin.run(api_data_fixture)
        expected = [{
            'resource': 'anarn',
            'region': 'aws-global',
            'severity': 0,
            'message': 'Distribution does not have S3 origin configured'
        }]

        self.assertEqual(results, expected)

    def test_s3_origin_no_access_identity(self):
        api_data_fixture = {
            'aws': {
                'cloudfront': {
                    'aws-global': {
                        'list_distributions': [
                            {
                                'ARN': 'anarn',
                                'Origins': {
                                    'Items': [
                                        {
                                            'S3OriginConfig': {
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                }
            }
        }

        plugin = S3OriginAccessIdentityPlugin()
        results = plugin.run(api_data_fixture)
        expected = [{
            'resource': 'anarn',
            'region': 'aws-global',
            'severity': 2,
            'message': (
                'Distribution is using S3 origin without an origin '
                'access identity'
            )
        }]

        self.assertEqual(results, expected)

    def test_with_properly_configured_origin_access_identity(self):
        api_data_fixture = {
            'aws': {
                'cloudfront': {
                    'aws-global': {
                        'list_distributions': [
                            {
                                'ARN': 'anarn',
                                'Origins': {
                                    'Items': [
                                        {
                                            'S3OriginConfig': {
                                                'OriginAccessIdentity': 'oai'
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                }
            }
        }

        plugin = S3OriginAccessIdentityPlugin()
        results = plugin.run(api_data_fixture)
        expected = [{
            'resource': 'anarn',
            'region': 'aws-global',
            'severity': 0,
            'message': 'Distribution is using secure origin oai'
        }]

        self.assertEqual(results, expected)
