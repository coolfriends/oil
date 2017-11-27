import unittest

from oil.plugins.aws.ec2 import InstanceHighThreatPortPlugin


class InstanceHighThreatPortPluginTestCase(unittest.TestCase):

    def test_can_be_initialized_and_run_with_no_config(self):
        data_fixture = {
            'aws': {
                'ec2': {
                    'us-east-1': {
                        'high_threat_security_groups': [],
                        'describe_instances': [],
                    }
                }
            }
        }

        plugin = InstanceHighThreatPortPlugin({})
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
                        'high_threat_security_groups': [],
                        'describe_instances': [],
                    }
                }
            }
        }

        plugin = InstanceHighThreatPortPlugin({})
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
                        'high_threat_security_groups': [],
                        'describe_instances': [],
                    }
                }
            }
        }

        plugin = InstanceHighThreatPortPlugin({})
        results = plugin.run(data_fixture)
        expected = [
            {
                'resource': 'None',
                'region': 'us-east-1',
                'severity': 0,
                'message': 'No instances found'
            }
        ]

        self.assertEqual(results, expected)

    def test_high_threat_port_on_instance(self):
        data_fixture = {
            'aws': {
                'ec2': {
                    'us-east-1': {
                        'high_threat_security_groups': [
                            {
                                'id': 'group_id',
                                'ports': [
                                    80,
                                ]
                            }
                        ],
                        'describe_instances': [
                            {
                                'InstanceId': 'instance_id',
                                'SecurityGroups': [
                                    {
                                        'GroupId': 'group_id'
                                    }
                                ],
                            }
                        ],
                    }
                }
            }
        }

        plugin = InstanceHighThreatPortPlugin({})
        results = plugin.run(data_fixture)
        expected = [
            {
                'resource': 'instance_id',
                'region': 'us-east-1',
                'severity': 2,
                'message': 'Port 80 open on group group_id',
            }
        ]

        self.assertEqual(results, expected)

    def test_no_high_threat_ports_on_instance(self):
        data_fixture = {
            'aws': {
                'ec2': {
                    'us-east-1': {
                        'high_threat_security_groups': [
                            {
                                'id': 'group_id',
                                'ports': [
                                    80,
                                ]
                            }
                        ],
                        'describe_instances': [
                            {
                                'InstanceId': 'instance_id',
                                'SecurityGroups': [
                                    {
                                        'GroupId': 'some_other_id'
                                    }
                                ],
                            }
                        ],
                    }
                }
            }
        }

        plugin = InstanceHighThreatPortPlugin({})
        results = plugin.run(data_fixture)
        expected = [
            {
                'resource': 'instance_id',
                'region': 'us-east-1',
                'severity': 0,
                'message': 'Instance has no high threat ports open',
            }
        ]

        self.assertEqual(results, expected)

    def test_configure_no_instances_message(self):
        data_fixture = {
            'aws': {
                'ec2': {
                    'us-east-1': {
                        'high_threat_security_groups': [
                            {
                                'id': 'group_id',
                                'ports': [
                                    80,
                                ]
                            }
                        ],
                        'describe_instances': [],
                    }
                }
            }
        }

        config = {
            'no_instances_message': 'Overloaded message',
        }
        plugin = InstanceHighThreatPortPlugin({}, config=config)
        results = plugin.run(data_fixture)
        expected = [
            {
                'resource': 'None',
                'region': 'us-east-1',
                'severity': 0,
                'message': 'Overloaded message',
            }
        ]

        self.assertEqual(results, expected)

    def test_configure_no_instances_display(self):
        data_fixture = {
            'aws': {
                'ec2': {
                    'us-east-1': {
                        'high_threat_security_groups': [
                            {
                                'id': 'group_id',
                                'ports': [
                                    80,
                                ]
                            }
                        ],
                        'describe_instances': [],
                    }
                }
            }
        }

        config = {
            'no_instances_display': False,
        }
        plugin = InstanceHighThreatPortPlugin({}, config=config)
        results = plugin.run(data_fixture)
        expected = []

        self.assertEqual(results, expected)

    def test_configure_high_threat_severity(self):
        data_fixture = {
            'aws': {
                'ec2': {
                    'us-east-1': {
                        'high_threat_security_groups': [
                            {
                                'id': 'group_id',
                                'ports': [
                                    80,
                                ],
                            },
                        ],
                        'describe_instances': [
                            {
                                'InstanceId': 'my_id',
                                'SecurityGroups': [
                                    {
                                        'GroupId': 'group_id',
                                    },
                                ],
                            }
                        ],
                    }
                }
            }
        }

        config = {
            'high_threat_severity': 1,
        }
        plugin = InstanceHighThreatPortPlugin({}, config=config)
        results = plugin.run(data_fixture)
        expected = [
            {
                'resource': 'my_id',
                'region': 'us-east-1',
                'severity': 1,
                'message': 'Port 80 open on group group_id',
            }
        ]

        self.assertEqual(results, expected)

    def test_configure_high_threat_message(self):
        data_fixture = {
            'aws': {
                'ec2': {
                    'us-east-1': {
                        'high_threat_security_groups': [
                            {
                                'id': 'group_id',
                                'ports': [
                                    80,
                                ],
                            },
                        ],
                        'describe_instances': [
                            {
                                'InstanceId': 'my_id',
                                'SecurityGroups': [
                                    {
                                        'GroupId': 'group_id',
                                    },
                                ],
                            }
                        ],
                    }
                }
            }
        }

        config = {
            'high_threat_message': 'Overloaded message {group_id}, {port}',
        }
        plugin = InstanceHighThreatPortPlugin({}, config=config)
        results = plugin.run(data_fixture)
        expected = [
            {
                'resource': 'my_id',
                'region': 'us-east-1',
                'severity': 2,
                'message': 'Overloaded message group_id, 80',
            }
        ]

        self.assertEqual(results, expected)

    def test_configure_no_high_threat_display(self):
        data_fixture = {
            'aws': {
                'ec2': {
                    'us-east-1': {
                        'high_threat_security_groups': [
                            {
                                'id': 'group_id',
                                'ports': [
                                    80,
                                ],
                            },
                        ],
                        'describe_instances': [
                            {
                                'InstanceId': 'my_id',
                                'SecurityGroups': [
                                ],
                            }
                        ],
                    }
                }
            }
        }

        config = {
            'no_high_threat_display': False,
        }
        plugin = InstanceHighThreatPortPlugin({}, config=config)
        results = plugin.run(data_fixture)
        expected = []

        self.assertEqual(results, expected)

    def test_configure_no_high_threat_message(self):
        data_fixture = {
            'aws': {
                'ec2': {
                    'us-east-1': {
                        'high_threat_security_groups': [
                            {
                                'id': 'other_group_id',
                                'ports': [
                                    80,
                                ],
                            },
                        ],
                        'describe_instances': [
                            {
                                'InstanceId': 'my_id',
                                'SecurityGroups': [
                                    {
                                        'GroupId': 'group_id',
                                    },
                                ],
                            }
                        ],
                    }
                }
            }
        }

        config = {
            'no_high_threat_message': 'Overloaded message',
        }
        plugin = InstanceHighThreatPortPlugin({}, config=config)
        results = plugin.run(data_fixture)
        expected = [
            {
                'resource': 'my_id',
                'region': 'us-east-1',
                'severity': 0,
                'message': 'Overloaded message',
            }
        ]

        self.assertEqual(results, expected)
