import unittest

from oil.plugins.aws.ec2 import InstanceNameTagPlugin

class InstanceNameTagPluginTestCase(unittest.TestCase):

    def test_can_be_initialized_and_run_with_no_config(self):
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
            'aws': {
                'ec2': {
                    'us-east-1': {
                        'describe_instances': [instance_fixture]
                    }
                }
            }
        }

        plugin = InstanceNameTagPlugin({})
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
            'aws': {
                'ec2': {
                    'us-east-1': {
                        'describe_instances': [instance_fixture]
                    }
                }
            }
        }

        plugin = InstanceNameTagPlugin({})
        results = plugin.run(data_fixture)
        results_keys = list(results[0].keys())
        expected = [
            'resource',
            'severity',
            'message',
            'region'
        ]

        self.assertCountEqual(results_keys, expected)




    def test_creates_results_with_correct_fields_for_multiple_instances(self):
        instance1_fixture = {
            'InstanceId': 'theinstance-id1',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'An Instance Name1'
                }
            ]
        }
        instance2_fixture = {
            'InstanceId': 'theinstance-id2',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'An Instance Name2'
                }
            ]
        }

        instances = [instance1_fixture, instance2_fixture]
        data_fixture = {
            'aws': {
                'ec2': {
                    'us-east-1': {
                        'describe_instances': instances
                    }
                }
            }
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

