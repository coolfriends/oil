import unittest
import datetime

from oil.plugins.aws.iam import UserMFAPlugin


class UserMFAPluginTestCase(unittest.TestCase):

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

        plugin = UserMFAPlugin()
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

        plugin = UserMFAPlugin({})
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
            'mfa_active': 'true'
        }
        user2_fixture = {
            'arn': 'arn2',
            'user': 'user2',
            'mfa_active': 'true'
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

        plugin = UserMFAPlugin()
        results = plugin.run(data_fixture)
        results_keys = list(results[0].keys())
        expected = [
            'resource',
            'severity',
            'message',
            'region'
        ]

        self.assertCountEqual(results_keys, expected)

    def test_skips_root_account(self):
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

        plugin = UserMFAPlugin()
        results = plugin.run(data_fixture)
        expected = []

        self.assertEqual(results, expected)


    def test_mfa_is_active(self):
        user_fixture = {
            'arn': 'arn1',
            'user': 'user1',
            'mfa_active': 'true',
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

        plugin = UserMFAPlugin()
        results = plugin.run(data_fixture)
        expected = [
            {
                'resource': 'arn1',
                'region': 'aws-global',
                'severity': 0,
                'message': 'MFA enabled for user1'
            }
        ]

        self.assertEqual(results, expected)

    def test_mfa_is_not_active(self):
        user_fixture = {
            'arn': 'arn1',
            'user': 'user1',
            'mfa_active': 'false',
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

        plugin = UserMFAPlugin()
        results = plugin.run(data_fixture)
        expected = [
            {
                'resource': 'arn1',
                'region': 'aws-global',
                'severity': 2,
                'message': 'MFA not enabled for user1'
            }
        ]

        self.assertEqual(results, expected)

    def test_mfa_is_not_active(self):
        user_fixture = {
            'arn': 'arn1',
            'user': 'user1',
            'mfa_active': 'false',
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

        plugin = UserMFAPlugin()
        results = plugin.run(data_fixture)
        expected = [
            {
                'resource': 'arn1',
                'region': 'aws-global',
                'severity': 2,
                'message': 'MFA not enabled for user1'
            }
        ]

        self.assertEqual(results, expected)

    def test_configure_enabled_message(self):
        user_fixture = {
            'arn': 'arn1',
            'user': 'user1',
            'mfa_active': 'true',
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
            'enabled_message': 'Enabled: {username}'
        }
        plugin = UserMFAPlugin(config)
        results = plugin.run(data_fixture)
        expected = [
            {
                'resource': 'arn1',
                'region': 'aws-global',
                'severity': 0,
                'message': 'Enabled: user1'
            }
        ]

        self.assertEqual(results, expected)

    def test_configure_not_enabled_message(self):
        user_fixture = {
            'arn': 'arn1',
            'user': 'user1',
            'mfa_active': 'false',
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
            'not_enabled_message': 'Not Enabled: {username}'
        }
        plugin = UserMFAPlugin(config)
        results = plugin.run(data_fixture)
        expected = [
            {
                'resource': 'arn1',
                'region': 'aws-global',
                'severity': 2,
                'message': 'Not Enabled: user1'
            }
        ]

        self.assertEqual(results, expected)

    def test_configure_not_enabled_severity_level(self):
        user_fixture = {
            'arn': 'arn1',
            'user': 'user1',
            'mfa_active': 'false',
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
            'not_enabled_severity_level': 1
        }
        plugin = UserMFAPlugin(config)
        results = plugin.run(data_fixture)
        expected = [
            {
                'resource': 'arn1',
                'region': 'aws-global',
                'severity': 1,
                'message': 'MFA not enabled for user1'
            }
        ]

        self.assertEqual(results, expected)
