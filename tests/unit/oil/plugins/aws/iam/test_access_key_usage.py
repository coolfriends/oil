import unittest
import datetime

from oil.plugins.aws.iam import AccessKeyUsagePlugin


class AccessKeyUsagePluginTestCase(unittest.TestCase):

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

        plugin = AccessKeyUsagePlugin({})
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

        plugin = AccessKeyUsagePlugin({})
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

        plugin = AccessKeyUsagePlugin({})
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

        plugin = AccessKeyUsagePlugin({})
        results = plugin.run(data_fixture)
        expected = []

        self.assertEqual(results, expected)

    def test_no_access_keys(self):
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

        plugin = AccessKeyUsagePlugin({})
        results = plugin.run(data_fixture)
        expected = [
            {
                'region': 'aws-global',
                'resource': 'arn1',
                'severity': 0,
                'message': 'No active keys for user1'
            }
        ]

        self.assertEqual(results, expected)

    def test_access_key_1_never_used(self):
        user_fixture = {
            'arn': 'arn1',
            'user': 'user1',
            'access_key_1_active': 'true',
            'access_key_1_last_used': 'N/A',
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

        plugin = AccessKeyUsagePlugin({})
        results = plugin.run(data_fixture)
        expected = [
            {
                'region': 'aws-global',
                'resource': 'arn1',
                'severity': 0,
                'message': 'Access key 1 has never been used for user1'
            }
        ]

        self.assertEqual(results, expected)

    def test_access_key_2_never_used(self):
        user_fixture = {
            'arn': 'arn1',
            'user': 'user1',
            'access_key_1_active': 'false',
            'access_key_2_active': 'true',
            'access_key_2_last_used': 'N/A',
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

        plugin = AccessKeyUsagePlugin({})
        results = plugin.run(data_fixture)
        expected = [
            {
                'region': 'aws-global',
                'resource': 'arn1',
                'severity': 0,
                'message': 'Access key 2 has never been used for user1'
            }
        ]

        self.assertEqual(results, expected)


    def test_active_key_1_active_severity_2(self):
        dt = datetime.datetime.now() - datetime.timedelta(days=-200)
        user_fixture = {
            'arn': 'arn1',
            'user': 'user1',
            'access_key_1_active': 'true',
            'access_key_1_last_used_date': dt.isoformat(),
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

        plugin = AccessKeyUsagePlugin({})
        results = plugin.run(data_fixture)
        expected = [
            {
                'region': 'aws-global',
                'resource': 'arn1',
                'severity': 2,
                'message': 'Access key 1 last used 200 days ago for user1'
            }
        ]

        self.assertEqual(results, expected)


    def test_active_key_2_active_severity_2(self):
        dt = datetime.datetime.now() - datetime.timedelta(-200)
        user_fixture = {
            'arn': 'arn1',
            'user': 'user1',
            'access_key_1_active': 'false',
            'access_key_2_active': 'true',
            'access_key_2_last_used_date': dt.isoformat(),
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

        plugin = AccessKeyUsagePlugin({})
        results = plugin.run(data_fixture)
        expected = [
            {
                'region': 'aws-global',
                'resource': 'arn1',
                'severity': 2,
                'message': 'Access key 2 last used 200 days ago for user1'
            }
        ]

        self.assertEqual(results, expected)

    def test_active_key_1_active_severity_1(self):
        dt = datetime.datetime.utcnow() - datetime.timedelta(days=-100)
        user_fixture = {
            'arn': 'arn1',
            'user': 'user1',
            'access_key_1_active': 'true',
            'access_key_1_last_used_date': dt.isoformat(),
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

        plugin = AccessKeyUsagePlugin({})
        results = plugin.run(data_fixture)
        expected = [
            {
                'region': 'aws-global',
                'resource': 'arn1',
                'severity': 1,
                'message': 'Access key 1 last used 100 days ago for user1'
            }
        ]

        self.assertEqual(results, expected)

    def test_active_key_2_active_severity_1(self):
        dt = datetime.datetime.utcnow() - datetime.timedelta(days=-100)
        user_fixture = {
            'arn': 'arn1',
            'user': 'user1',
            'access_key_1_active': 'false',
            'access_key_2_active': 'true',
            'access_key_2_last_used_date': dt.isoformat(),
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

        plugin = AccessKeyUsagePlugin({})
        results = plugin.run(data_fixture)
        expected = [
            {
                'region': 'aws-global',
                'resource': 'arn1',
                'severity': 1,
                'message': 'Access key 2 last used 100 days ago for user1'
            }
        ]

        self.assertEqual(results, expected)

    def test_active_key_1_active_severity_0(self):
        dt = datetime.datetime.utcnow() - datetime.timedelta(days=-20)
        user_fixture = {
            'arn': 'arn1',
            'user': 'user1',
            'access_key_1_active': 'true',
            'access_key_1_last_used_date': dt.isoformat(),
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

        plugin = AccessKeyUsagePlugin({})
        results = plugin.run(data_fixture)
        expected = [
            {
                'region': 'aws-global',
                'resource': 'arn1',
                'severity': 0,
                'message': 'Access key 1 last used 20 days ago for user1'
            }
        ]

        self.assertEqual(results, expected)

    def test_active_key_2_active_severity_0(self):
        dt = datetime.datetime.utcnow() - datetime.timedelta(days=-20)
        user_fixture = {
            'arn': 'arn1',
            'user': 'user1',
            'access_key_1_active': 'false',
            'access_key_2_active': 'true',
            'access_key_2_last_used_date': dt.isoformat(),
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

        plugin = AccessKeyUsagePlugin({})
        results = plugin.run(data_fixture)
        expected = [
            {
                'region': 'aws-global',
                'resource': 'arn1',
                'severity': 0,
                'message': 'Access key 2 last used 20 days ago for user1'
            }
        ]

        self.assertEqual(results, expected)

    def test_custom_severity_2_threshold(self):
        dt = datetime.datetime.utcnow() - datetime.timedelta(days=-61)
        user_fixture = {
            'arn': 'arn1',
            'user': 'user1',
            'access_key_1_active': 'true',
            'access_key_1_last_used_date': dt.isoformat(),
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
            'access_key_last_used_severity_two_threshold': 60
        }
        plugin = AccessKeyUsagePlugin({}, config)
        results = plugin.run(data_fixture)
        expected = [
            {
                'region': 'aws-global',
                'resource': 'arn1',
                'severity': 2,
                'message': 'Access key 1 last used 61 days ago for user1'
            }
        ]

        self.assertEqual(results, expected)

    def test_custom_severity_1_threshold(self):
        dt = datetime.datetime.utcnow() - datetime.timedelta(-31)
        user_fixture = {
            'arn': 'arn1',
            'user': 'user1',
            'access_key_1_active': 'true',
            'access_key_1_last_used_date': dt.isoformat(),
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
            'access_key_last_used_severity_one_threshold': 30
        }
        plugin = AccessKeyUsagePlugin({}, config)
        results = plugin.run(data_fixture)
        expected = [
            {
                'region': 'aws-global',
                'resource': 'arn1',
                'severity': 1,
                'message': 'Access key 1 last used 31 days ago for user1'
            }
        ]

        self.assertEqual(results, expected)
