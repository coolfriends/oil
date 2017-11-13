import unittest

from oil.plugins.aws.iam import ExtraAccessKeyPlugin


class ExtraAccessKeyPluginTestCase(unittest.TestCase):

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

        plugin = ExtraAccessKeyPlugin()
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

        plugin = ExtraAccessKeyPlugin({})
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

        plugin = ExtraAccessKeyPlugin()
        results = plugin.run(data_fixture)
        results_keys = list(results[0].keys())
        expected = [
            'resource',
            'severity',
            'message',
            'region'
        ]

        self.assertCountEqual(results_keys, expected)

    def test_skips_root_keys(self):
        user_fixture = {
            'arn': 'arn1',
            'user': '<root_account>',
            'access_key_1_active': 'true',
            'access_key_2_active': 'true',
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

        plugin = ExtraAccessKeyPlugin()
        results = plugin.run(data_fixture)
        expected = []

        self.assertEqual(results, expected)

    def test_two_active_keys(self):
        user_fixture = {
            'arn': 'arn1',
            'user': 'user1',
            'access_key_1_active': 'true',
            'access_key_2_active': 'true',
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

        plugin = ExtraAccessKeyPlugin()
        results = plugin.run(data_fixture)
        expected = [
            {
                'region': 'aws-global',
                'resource': 'arn1',
                'severity': 2,
                'message': 'Multiple active keys found for user user1'
            }
        ]

        self.assertEqual(results, expected)

    def test_only_access_key_1_active(self):
        user_fixture = {
            'arn': 'arn1',
            'user': 'user1',
            'access_key_1_active': 'true',
            'access_key_2_active': 'false',
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

        plugin = ExtraAccessKeyPlugin()
        results = plugin.run(data_fixture)
        expected = [
            {
                'region': 'aws-global',
                'resource': 'arn1',
                'severity': 0,
                'message': 'Key 1 active for user user1'
            }
        ]

        self.assertEqual(results, expected)

    def test_only_access_key_2_active(self):
        user_fixture = {
            'arn': 'arn1',
            'user': 'user1',
            'access_key_1_active': 'false',
            'access_key_2_active': 'true',
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

        plugin = ExtraAccessKeyPlugin()
        results = plugin.run(data_fixture)
        expected = [
            {
                'region': 'aws-global',
                'resource': 'arn1',
                'severity': 0,
                'message': 'Key 2 active for user user1'
            }
        ]

        self.assertEqual(results, expected)

    def test_no_active_keys(self):
        user_fixture = {
            'arn': 'arn1',
            'user': 'user1',
            'access_key_1_active': 'false',
            'access_key_2_active': 'false',
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

        plugin = ExtraAccessKeyPlugin()
        results = plugin.run(data_fixture)
        expected = [
            {
                'region': 'aws-global',
                'resource': 'arn1',
                'severity': 0,
                'message': 'No active keys for user user1'
            }
        ]

        self.assertEqual(results, expected)
