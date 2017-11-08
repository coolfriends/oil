import unittest

from oil.plugins.aws.ec2 import InstanceNameTagPlugin

class InstanceNameTagPluginTestCase(unittest.TestCase):

    def test_can_be_initialized_and_run_with_no_config(self):
        data_fixture = {
            'aws': {
                'ec2': {
                    'us-east-1': {
                        'describe_instances': []
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
        data_fixture = {
            'aws': {
                'ec2': {
                    'us-east-1': {
                        'describe_instances': []
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


    def test_no_instances(self):
        data_fixture = {
            'aws': {
                'ec2': {
                    'us-east-1': {
                        'describe_instances': []
                    }
                }
            }
        }
        plugin = InstanceNameTagPlugin()
        results = plugin.run(data_fixture)
        expected = [{
            'resource': 'None',
            'region': 'us-east-1',
            'severity': 0,
            'message': 'No instances found'
        }]

        self.assertEqual(results, expected)

    def test_instance_has_name_tag(self):
        data_fixture = {
            'aws': {
                'ec2': {
                    'us-east-1': {
                        'describe_instances': [
                            {
                                'InstanceId': 'id1',
                                'Tags': [
                                    {
                                        'Key': 'Name',
                                        'Value': 'name1'
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        }
        plugin = InstanceNameTagPlugin()
        results = plugin.run(data_fixture)
        expected = [{
            'resource': 'id1',
            'region': 'us-east-1',
            'severity': 0,
            'message': 'Instance has a Name tag of name1'
        }]

        self.assertEqual(results, expected)

    def test_instance_has_no_name_tag(self):
        data_fixture = {
            'aws': {
                'ec2': {
                    'us-east-1': {
                        'describe_instances': [
                            {
                                'InstanceId': 'id1',
                                'Tags': [
                                    {
                                        'Key': 'NotName',
                                        'Value': 'name1'
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        }
        plugin = InstanceNameTagPlugin()
        results = plugin.run(data_fixture)
        expected = [{
            'resource': 'id1',
            'region': 'us-east-1',
            'severity': 1,
            'message': 'Instance does not have a Name tag'
        }]

        self.assertEqual(results, expected)
