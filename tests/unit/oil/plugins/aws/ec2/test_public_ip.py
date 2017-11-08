import unittest

from oil.plugins.aws.ec2 import PublicIpPlugin

class PublicIpPluginTestCase(unittest.TestCase):

    def test_can_be_initialized_and_run_with_no_config(self):
        data_fixture = {
            'aws': {
                'ec2': {
                    'us-east-1': {
                        'describe_instances': [
                            {
                                'InstanceId': 'theid'
                            }
                        ]
                    }
                }
            }
        }

        plugin = PublicIpPlugin()
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
                        'describe_instances': [
                            {
                                'InstanceId': 'anid'
                            }
                        ]
                    }
                }
            }
        }

        plugin = PublicIpPlugin({})
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
            'InstanceId': 'id1'
        }
        instance2_fixture = {
            'InstanceId': 'id1'
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

        plugin = PublicIpPlugin()
        results = plugin.run(data_fixture)
        results_keys = list(results[0].keys())
        expected = [
            'resource',
            'severity',
            'message',
            'region'
        ]

        self.assertCountEqual(results_keys, expected)

    def test_only_one_sensible_result_if_no_instances(self):
        api_data_fixture = {
            'aws': {
                'ec2': {
                    'us-east-1': {
                        'describe_instances': []
                    }
                }
            }
        }

        plugin = PublicIpPlugin()
        results = plugin.run(api_data_fixture)
        expected = [{
            'resource': 'None',
            'region': 'us-east-1',
            'severity': 0,
            'message': 'No instances found'
            }]

        self.assertCountEqual(results, expected)

    # Write test case for all cases
    def test_with_base_public_ip(self):
        api_data_fixture = {
            'aws': {
                'ec2': {
                    'us-east-1': {
                        'describe_instances': [
                            {
                                'InstanceId': 'theid',
                                'PublicIpAddress': '111.111.111.111'
                            }
                        ]
                    }
                }
            }
        }

        plugin = PublicIpPlugin()
        results = plugin.run(api_data_fixture)
        expected = [{
            'resource': 'theid',
            'region': 'us-east-1',
            'severity': 1,
            'message': 'Instance has public ip: 111.111.111.111'
        }]

        self.assertEqual(results, expected)

    def test_with_nested_public_ip(self):
        api_data_fixture = {
            'aws': {
                'ec2': {
                    'us-east-1': {
                        'describe_instances': [
                            {
                                'InstanceId': 'theid',
                                'NetworkInterfaces': [
                                    {
                                        'Association': {
                                            'PublicIp': '111.111.111.111'
                                        }
                                    },
                                    {
                                        'Association': {
                                            'PublicIp': '111.111.111.000'
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        }

        plugin = PublicIpPlugin()
        results = plugin.run(api_data_fixture)
        message_format = 'Instance has public ip: {}'
        expected = [
            {
                'resource': 'theid',
                'region': 'us-east-1',
                'severity': 1,
                'message': message_format.format('111.111.111.111')
            },
            {
                'resource': 'theid',
                'region': 'us-east-1',
                'severity': 1,
                'message': message_format.format('111.111.111.000')
            }
        ]

        self.assertEqual(results, expected)

    def test_with_nested_public_ip_does_not_add_public_ip_twice(self):
        api_data_fixture = {
            'aws': {
                'ec2': {
                    'us-east-1': {
                        'describe_instances': [
                            {
                                'InstanceId': 'theid',
                                'PublicIpAddress': '111.111.111.111',
                                'NetworkInterfaces': [
                                    {
                                        'Association': {
                                            'PublicIp': '111.111.111.111'
                                        }
                                    },
                                ]
                            }
                        ]
                    }
                }
            }
        }

        plugin = PublicIpPlugin()
        results = plugin.run(api_data_fixture)
        message_format = 'Instance has public ip: {}'
        expected = [
            {
                'resource': 'theid',
                'region': 'us-east-1',
                'severity': 1,
                'message': message_format.format('111.111.111.111')
            }
        ]
        self.assertEqual(expected, results)
