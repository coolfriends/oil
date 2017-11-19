import unittest
import datetime

from oil.plugins.aws.iam import TotalUsersPlugin


class TotalUsersPluginTestCase(unittest.TestCase):

    def test_can_be_initialized_and_run_with_no_config(self):
        data_fixture = {
            'aws': {
                'iam': {
                    'aws-global': {
                        'get_credential_report': [
                        ]
                    }
                }
            }
        }

        plugin = TotalUsersPlugin({})
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
                'iam': {
                    'aws-global': {
                        'get_credential_report': [
                        ]
                    }
                }
            }
        }

        plugin = TotalUsersPlugin({})
        results = plugin.run(data_fixture)
        results_keys = list(results[0].keys())
        expected = [
            'resource',
            'severity',
            'message',
            'region'
        ]

        self.assertCountEqual(results_keys, expected)

    def test_creates_results_with_correct_fields_for_multiple_users(self):
        user1_fixture = {
            'arn': 'arn1',
            'user': 'user1',
        }
        user2_fixture = {
            'arn': 'arn2',
            'user': 'user2'
        }

        users = [user1_fixture, user2_fixture]
        data_fixture = {
            'aws': {
                'iam': {
                    'aws-global': {
                        'get_credential_report': users
                    }
                }
            }
        }

        plugin = TotalUsersPlugin({})
        results = plugin.run(data_fixture)
        results_keys = list(results[0].keys())
        expected = [
            'resource',
            'severity',
            'message',
            'region'
        ]

        self.assertCountEqual(results_keys, expected)

    # NOTE: It does not seem possible that an AWS account could have no users
    # because the root account should always exist, but just incase...
    def test_no_users(self):
        data_fixture = {
            'aws': {
                'iam': {
                    'aws-global': {
                        'get_credential_report': []
                    }
                }
            }
        }

        plugin = TotalUsersPlugin({})
        results = plugin.run(data_fixture)
        expected = [
            {
                'resource': 'None',
                'region': 'aws-global',
                'severity': 0,
                'message': 'There are no users for this account'
            }
        ]

        self.assertEqual(results, expected)


    def test_users_severity_2(self):
        users_fixture = []
        for number in range(0, 2000):
            users_fixture.append({
                'user': 'user{}'.format(number),
                'arn': 'arn{}'.format(number),
            })
        data_fixture = {
            'aws': {
                'iam': {
                    'aws-global': {
                        'get_credential_report': users_fixture
                    }
                }
            }
        }

        plugin = TotalUsersPlugin({})
        results = plugin.run(data_fixture)
        expected = [
            {
                'resource': 'None',
                'region': 'aws-global',
                'severity': 2,
                'message': 'There are 2000 users for this account'
            }
        ]

        self.assertEqual(results, expected)

    def test_users_severity_1(self):
        users_fixture = []
        for number in range(0, 600):
            users_fixture.append({
                'user': 'user{}'.format(number),
                'arn': 'arn{}'.format(number),
            })
        data_fixture = {
            'aws': {
                'iam': {
                    'aws-global': {
                        'get_credential_report': users_fixture
                    }
                }
            }
        }

        plugin = TotalUsersPlugin({})
        results = plugin.run(data_fixture)
        expected = [
            {
                'resource': 'None',
                'region': 'aws-global',
                'severity': 1,
                'message': 'There are 600 users for this account'
            }
        ]

        self.assertEqual(results, expected)

    def test_users_severity_0(self):
        users_fixture = [
            {
                'user': 'user1',
                'arn': 'arn1',
            }
        ]
        data_fixture = {
            'aws': {
                'iam': {
                    'aws-global': {
                        'get_credential_report': users_fixture
                    }
                }
            }
        }

        plugin = TotalUsersPlugin({})
        results = plugin.run(data_fixture)
        expected = [
            {
                'resource': 'None',
                'region': 'aws-global',
                'severity': 0,
                'message': 'There are 1 users for this account'
            }
        ]

        self.assertEqual(results, expected)

    def test_configure_total_users_severity_2_threshold(self):
        users_fixture = [
            {
                'user': 'user1',
                'arn': 'arn1',
            },
            {
                'user': 'user1',
                'arn': 'arn1',
            },
            {
                'user': 'user1',
                'arn': 'arn1',
            }
        ]
        data_fixture = {
            'aws': {
                'iam': {
                    'aws-global': {
                        'get_credential_report': users_fixture
                    }
                }
            }
        }

        config = {
            'total_users_severity_2_threshold': 2
        }
        plugin = TotalUsersPlugin({}, config)
        results = plugin.run(data_fixture)
        expected = [
            {
                'resource': 'None',
                'region': 'aws-global',
                'severity': 2,
                'message': 'There are 3 users for this account'
            }
        ]

        self.assertEqual(results, expected)

    def test_configure_total_users_severity_1_threshold(self):
        users_fixture = [
            {
                'user': 'user1',
                'arn': 'arn1',
            },
            {
                'user': 'user1',
                'arn': 'arn1',
            },
            {
                'user': 'user1',
                'arn': 'arn1',
            }
        ]
        data_fixture = {
            'aws': {
                'iam': {
                    'aws-global': {
                        'get_credential_report': users_fixture
                    }
                }
            }
        }

        config = {
            'total_users_severity_1_threshold': 2
        }
        plugin = TotalUsersPlugin({}, config)
        results = plugin.run(data_fixture)
        expected = [
            {
                'resource': 'None',
                'region': 'aws-global',
                'severity': 1,
                'message': 'There are 3 users for this account'
            }
        ]

        self.assertEqual(results, expected)

    def test_configure_total_users_severity_2_message(self):
        users_fixture = [
            {
                'user': 'user1',
                'arn': 'arn1',
            },
            {
                'user': 'user1',
                'arn': 'arn1',
            },
            {
                'user': 'user1',
                'arn': 'arn1',
            }
        ]
        data_fixture = {
            'aws': {
                'iam': {
                    'aws-global': {
                        'get_credential_report': users_fixture
                    }
                }
            }
        }

        config = {
            'total_users_severity_2_threshold': 2,
            'total_users_severity_2_message': '{total_users} is too many users'
        }
        plugin = TotalUsersPlugin({}, config)
        results = plugin.run(data_fixture)
        expected = [
            {
                'resource': 'None',
                'region': 'aws-global',
                'severity': 2,
                'message': '3 is too many users'
            }
        ]

        self.assertEqual(results, expected)

    def test_configure_total_users_severity_1_message(self):
        users_fixture = [
            {
                'user': 'user1',
                'arn': 'arn1',
            },
            {
                'user': 'user1',
                'arn': 'arn1',
            },
            {
                'user': 'user1',
                'arn': 'arn1',
            }
        ]
        data_fixture = {
            'aws': {
                'iam': {
                    'aws-global': {
                        'get_credential_report': users_fixture
                    }
                }
            }
        }

        config = {
            'total_users_severity_1_threshold': 2,
            'total_users_severity_1_message': '{total_users} is too many users'
        }
        plugin = TotalUsersPlugin({}, config)
        results = plugin.run(data_fixture)
        expected = [
            {
                'resource': 'None',
                'region': 'aws-global',
                'severity': 1,
                'message': '3 is too many users'
            }
        ]

        self.assertEqual(results, expected)

    def test_configure_total_users_severity_0_message(self):
        users_fixture = [
            {
                'user': 'user1',
                'arn': 'arn1',
            },
            {
                'user': 'user1',
                'arn': 'arn1',
            },
            {
                'user': 'user1',
                'arn': 'arn1',
            }
        ]
        data_fixture = {
            'aws': {
                'iam': {
                    'aws-global': {
                        'get_credential_report': users_fixture
                    }
                }
            }
        }

        config = {
            'total_users_severity_0_message': (
                '{total_users} is an acceptable amount of users'
            )
        }
        plugin = TotalUsersPlugin({}, config)
        results = plugin.run(data_fixture)
        expected = [
            {
                'resource': 'None',
                'region': 'aws-global',
                'severity': 0,
                'message': '3 is an acceptable amount of users'
            }
        ]

        self.assertEqual(results, expected)

    def test_configure_no_users_message(self):
        data_fixture = {
            'aws': {
                'iam': {
                    'aws-global': {
                        'get_credential_report': []
                    }
                }
            }
        }

        config = {
            'no_users_message': (
                'No users found'
            )
        }
        plugin = TotalUsersPlugin({}, config)
        results = plugin.run(data_fixture)
        expected = [
            {
                'resource': 'None',
                'region': 'aws-global',
                'severity': 0,
                'message': 'No users found'
            }
        ]

        self.assertEqual(results, expected)
