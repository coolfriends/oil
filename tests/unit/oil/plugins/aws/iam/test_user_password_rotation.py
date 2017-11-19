import unittest
import datetime

from oil.plugins.aws.iam import UserPasswordRotationPlugin


class UserPasswordRotationPluginTestCase(unittest.TestCase):

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

        plugin = UserPasswordRotationPlugin({})
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

        plugin = UserPasswordRotationPlugin({})
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
            'password_last_changed': 'N/A',
        }
        user2_fixture = {
            'arn': 'arn2',
            'user': 'user2',
            'password_last_changed': 'N/A',
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

        plugin = UserPasswordRotationPlugin({})
        results = plugin.run(data_fixture)
        results_keys = list(results[0].keys())
        expected = [
            'resource',
            'severity',
            'message',
            'region'
        ]

        self.assertCountEqual(results_keys, expected)

    def test_root_account_is_skipped(self):
        user_fixture = {
            'arn': 'arn1',
            'user': '<root_account>',
        }

        users = [user_fixture]
        data_fixture = {
            'aws': {
                'iam': {
                    'aws-global': {
                        'get_credential_report': users
                    }
                }
            }
        }

        plugin = UserPasswordRotationPlugin({})
        results = plugin.run(data_fixture)
        expected = []

        self.assertEqual(results, expected)

    def test_user_has_no_password(self):
        user_fixture = {
            'arn': 'arn1',
            'user': 'user1',
            'password_last_changed': 'N/A'
        }

        users = [user_fixture]
        data_fixture = {
            'aws': {
                'iam': {
                    'aws-global': {
                        'get_credential_report': users
                    }
                }
            }
        }

        plugin = UserPasswordRotationPlugin({})
        results = plugin.run(data_fixture)
        expected = [
            {
                'resource': 'arn1',
                'severity': 0,
                'region': 'aws-global',
                'message': 'user1 does not have an AWS console password'

            }
        ]

        self.assertEqual(results, expected)

    def test_user_has_severity_2_expired_password(self):
        dt = datetime.datetime.now() - datetime.timedelta(days=-400)
        user_fixture = {
            'arn': 'arn1',
            'user': 'user1',
            'password_last_changed': dt.isoformat()
        }

        users = [user_fixture]
        data_fixture = {
            'aws': {
                'iam': {
                    'aws-global': {
                        'get_credential_report': users
                    }
                }
            }
        }

        plugin = UserPasswordRotationPlugin({})
        results = plugin.run(data_fixture)
        expected = [
            {
                'resource': 'arn1',
                'severity': 2,
                'region': 'aws-global',
                'message': 'user1 has not rotated their password in 400 days'

            }
        ]

        self.assertEqual(results, expected)

    def test_user_has_severity_1_expired_password(self):
        dt = datetime.datetime.now() - datetime.timedelta(days=-200)
        user_fixture = {
            'arn': 'arn1',
            'user': 'user1',
            'password_last_changed': dt.isoformat()
        }

        users = [user_fixture]
        data_fixture = {
            'aws': {
                'iam': {
                    'aws-global': {
                        'get_credential_report': users
                    }
                }
            }
        }

        plugin = UserPasswordRotationPlugin({})
        results = plugin.run(data_fixture)
        expected = [
            {
                'resource': 'arn1',
                'severity': 1,
                'region': 'aws-global',
                'message': 'user1 has not rotated their password in 200 days'

            }
        ]

        self.assertEqual(results, expected)

    def test_user_has_unexpired_password(self):
        dt = datetime.datetime.now() - datetime.timedelta(days=-10)
        user_fixture = {
            'arn': 'arn1',
            'user': 'user1',
            'password_last_changed': dt.isoformat()
        }

        users = [user_fixture]
        data_fixture = {
            'aws': {
                'iam': {
                    'aws-global': {
                        'get_credential_report': users
                    }
                }
            }
        }

        plugin = UserPasswordRotationPlugin({})
        results = plugin.run(data_fixture)
        expected = [
            {
                'resource': 'arn1',
                'severity': 0,
                'region': 'aws-global',
                'message': 'user1 has not rotated their password in 10 days'

            }
        ]

        self.assertEqual(results, expected)

    def test_configure_password_rotation_severity_2_threshold(self):
        dt = datetime.datetime.now() - datetime.timedelta(days=-100)
        user_fixture = {
            'arn': 'arn1',
            'user': 'user1',
            'password_last_changed': dt.isoformat()
        }

        users = [user_fixture]
        data_fixture = {
            'aws': {
                'iam': {
                    'aws-global': {
                        'get_credential_report': users
                    }
                }
            }
        }

        config = {
            'password_rotation_severity_2_threshold': 90
        }
        plugin = UserPasswordRotationPlugin({}, config)
        results = plugin.run(data_fixture)
        expected = [
            {
                'resource': 'arn1',
                'severity': 2,
                'region': 'aws-global',
                'message': 'user1 has not rotated their password in 100 days'

            }
        ]

        self.assertEqual(results, expected)

    def test_configure_password_rotation_severity_1_threshold(self):
        dt = datetime.datetime.now() - datetime.timedelta(days=-100)
        user_fixture = {
            'arn': 'arn1',
            'user': 'user1',
            'password_last_changed': dt.isoformat()
        }

        users = [user_fixture]
        data_fixture = {
            'aws': {
                'iam': {
                    'aws-global': {
                        'get_credential_report': users
                    }
                }
            }
        }

        config = {
            'password_rotation_severity_1_threshold': 90
        }
        plugin = UserPasswordRotationPlugin({}, config)
        results = plugin.run(data_fixture)
        expected = [
            {
                'resource': 'arn1',
                'severity': 1,
                'region': 'aws-global',
                'message': 'user1 has not rotated their password in 100 days'

            }
        ]

        self.assertEqual(results, expected)

    def test_configure_password_rotation_severity_2_message(self):
        dt = datetime.datetime.now() - datetime.timedelta(days=-400)
        user_fixture = {
            'arn': 'arn1',
            'user': 'user1',
            'password_last_changed': dt.isoformat()
        }

        users = [user_fixture]
        data_fixture = {
            'aws': {
                'iam': {
                    'aws-global': {
                        'get_credential_report': users
                    }
                }
            }
        }

        message = 'Password last changed {days} days ago for {username}'
        config = {
            'password_rotation_severity_2_message': message
        }
        plugin = UserPasswordRotationPlugin({}, config)
        results = plugin.run(data_fixture)
        expected = [
            {
                'resource': 'arn1',
                'severity': 2,
                'region': 'aws-global',
                'message': 'Password last changed 400 days ago for user1'
            }
        ]

        self.assertEqual(results, expected)

    def test_configure_password_rotation_severity_1_message(self):
        dt = datetime.datetime.now() - datetime.timedelta(days=-200)
        user_fixture = {
            'arn': 'arn1',
            'user': 'user1',
            'password_last_changed': dt.isoformat()
        }

        users = [user_fixture]
        data_fixture = {
            'aws': {
                'iam': {
                    'aws-global': {
                        'get_credential_report': users
                    }
                }
            }
        }

        message = 'Password last changed {days} days ago for {username}'
        config = {
            'password_rotation_severity_1_message': message
        }
        plugin = UserPasswordRotationPlugin({}, config)
        results = plugin.run(data_fixture)
        expected = [
            {
                'resource': 'arn1',
                'severity': 1,
                'region': 'aws-global',
                'message': 'Password last changed 200 days ago for user1'
            }
        ]

        self.assertEqual(results, expected)

    def test_configure_password_rotation_severity_0_message(self):
        dt = datetime.datetime.now() - datetime.timedelta(days=-10)
        user_fixture = {
            'arn': 'arn1',
            'user': 'user1',
            'password_last_changed': dt.isoformat()
        }

        users = [user_fixture]
        data_fixture = {
            'aws': {
                'iam': {
                    'aws-global': {
                        'get_credential_report': users
                    }
                }
            }
        }

        message = 'Password last changed {days} days ago for {username}'
        config = {
            'password_rotation_severity_0_message': message
        }
        plugin = UserPasswordRotationPlugin(config)
        results = plugin.run(data_fixture)
        expected = [
            {
                'resource': 'arn1',
                'severity': 0,
                'region': 'aws-global',
                'message': 'Password last changed 10 days ago for user1'
            }
        ]

        self.assertEqual(results, expected)

    def test_configure_password_rotation_severity_0_message(self):
        dt = datetime.datetime.now() - datetime.timedelta(days=-10)
        user_fixture = {
            'arn': 'arn1',
            'user': 'user1',
            'password_last_changed': dt.isoformat()
        }

        users = [user_fixture]
        data_fixture = {
            'aws': {
                'iam': {
                    'aws-global': {
                        'get_credential_report': users
                    }
                }
            }
        }

        message = 'Password last changed {days} days ago for {username}'
        config = {
            'password_rotation_severity_0_message': message
        }
        plugin = UserPasswordRotationPlugin({}, config)
        results = plugin.run(data_fixture)
        expected = [
            {
                'resource': 'arn1',
                'severity': 0,
                'region': 'aws-global',
                'message': 'Password last changed 10 days ago for user1'
            }
        ]

        self.assertEqual(results, expected)

    def test_configure_no_password_message(self):
        user_fixture = {
            'arn': 'arn1',
            'user': 'user1',
            'password_last_changed': 'N/A'
        }

        users = [user_fixture]
        data_fixture = {
            'aws': {
                'iam': {
                    'aws-global': {
                        'get_credential_report': users
                    }
                }
            }
        }

        message = 'No password for {username}'
        config = {
            'no_password_message': message
        }
        plugin = UserPasswordRotationPlugin({}, config)
        results = plugin.run(data_fixture)
        expected = [
            {
                'resource': 'arn1',
                'severity': 0,
                'region': 'aws-global',
                'message': 'No password for user1'
            }
        ]

        self.assertEqual(results, expected)
