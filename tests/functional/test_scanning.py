"""
These tests require functioning AWS access keys. That means the following
environment variables must be set. Necessary permissions for running these
tests should be documented. Functional tests also should NOT run unless
specified.

AWS_SECRET_ACCESS_KEY
AWS_ACCESS_KEY_ID
"""


import os
import unittest
from oil import Oil


@unittest.skipIf(os.environ.get('OIL_FUNCTIONAL_TESTS', 'False') != 'True', "Skipping functional tests")
class ScanningTestCase(unittest.TestCase):
    def test_user_can_scan_with_one_plugin_using_dictionary_configuration(self):
        test_configuration = {
            'aws': {
                'cloudfront': {
                    'plugins': [
                        {
                            'name': 'tls_protocol',
                        }
                    ]
                }
            }
        }
        oil = Oil(test_configuration)
        data = oil.scan()
        expected = data.get('aws', {}).get('cloudfront', {}).get('tls_protocol')

        self.assertIsNotNone(
            expected,
            (
                'This core functionality of the oil interface '
                'needs to be implemented'
            )
        )

    def test_oil_can_scan_for_https_usage(self):
        config = {
            'aws': {
                'cloudfront': {
                    'plugins': [
                        {
                            'name': 'https'
                        }
                    ]
                }
            }
        }

        oil = Oil(config)
        results = oil.scan()

        aws_results = results.get('aws', {})
        cloudfront_results = aws_results.get('cloudfront', {})
        plugin_results = cloudfront_results.get('https', [])

        self.assertNotEqual(plugin_results, [])

    def test_oil_can_scan_for_https_usage(self):
        config = {
            'aws': {
                'cloudfront': {
                    'plugins': [
                        {
                            'name': 's3_origin_access_identity'
                        }
                    ]
                }
            }
        }

        oil = Oil(config)
        results = oil.scan()

        aws_results = results.get('aws', {})
        cloudfront_results = aws_results.get('cloudfront', {})
        plugin_results = cloudfront_results.get('s3_origin_access_identity', [])

        self.assertNotEqual(plugin_results, [])
