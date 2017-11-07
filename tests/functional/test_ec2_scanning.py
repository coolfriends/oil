# Make sure that Oil implements all necessary EC2 security plugins
import unittest

from oil import Oil


class EC2ScanningTestCase(unittest.TestCase):
    def test_oil_can_scan_for_name_tag_compliance(self):
        config = {
            'aws': {
                'ec2': {
                    'plugins': [
                        {
                            'name': 'instance_name_tag'
                        }
                    ]
                }
            }
        }

        oil = Oil(config)
        results = oil.scan()

        aws_results = results.get('aws', {})
        ec2_results = aws_results.get('ec2', {})
        plugin_results = ec2_results.get('instance_name_tag', [])

        self.assertNotEqual(plugin_results, [])

