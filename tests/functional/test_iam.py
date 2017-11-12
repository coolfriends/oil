# Make sure that Oil implements all necessary EC2 security plugins
import unittest
import os

from oil import Oil


@unittest.skipIf(os.environ.get('OIL_FUNCTIONAL_TESTS', 'False') != 'True', "Skipping functional tests")
class IAMScanningTestCase(unittest.TestCase):
    def test_oil_can_scan_for_extra_access_key(self):
        config = {
            'aws': {
                'iam': {
                    'plugins': [
                        {
                            'name': 'extra_access_key'
                        }
                    ]
                }
            }
        }

        oil = Oil(config)
        results = oil.scan()

        aws_results = results.get('aws', {})
        iam_results = aws_results.get('iam', {})
        plugin_results = iam_results.get('extra_access_key', [])

        self.assertNotEqual(plugin_results, [])
