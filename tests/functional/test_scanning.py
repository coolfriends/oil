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
