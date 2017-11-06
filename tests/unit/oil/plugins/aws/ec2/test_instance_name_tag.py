import unittest

from oil.plugins.aws.ec2 import InstanceNameTagPlugin

class InstanceNameTagPluginTestCase(unittest.TestCase):
    def test_creates_results_with_correct_fields_for_one_instance(self):
        instance_fixture = {
            'InstanceId': 'theinstance-id',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'An Instance Name'
                }
            ]
        }

        data_fixture = {
            'us-east-1': [
                instance_fixture
            ]
        }

        plugin = InstanceNameTagPlugin()
        results = plugin.run(data_fixture)
        results_keys = list(results[0].keys())
        expected = [
            'resource',
            'severity',
            'message',
            'region'
        ]

        self.assertCountEqual(results_keys, expected)




