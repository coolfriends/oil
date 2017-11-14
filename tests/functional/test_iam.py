# Make sure that Oil implements all necessary EC2 security plugins
import unittest
import os

from oil import Oil


@unittest.skipIf(os.environ.get('OIL_FUNCTIONAL_TESTS', 'False') != 'True', "Skipping functional tests")
class IAMScanningTestCase(unittest.TestCase):
    def test_oil_can_scan_for_extra_access_key(self):
        config = {
            'aws': {
                'iam': {
                    'plugins': [
                        {
                            'name': 'extra_access_key'
                        }
                    ]
                }
            }
        }

        oil = Oil(config)
        results = oil.scan()

        aws_results = results.get('aws', {})
        iam_results = aws_results.get('iam', {})
        plugin_results = iam_results.get('extra_access_key', [])

        self.assertNotEqual(plugin_results, [])

    def test_oil_can_scan_for_access_key_usage(self):
        config = {
            'aws': {
                'iam': {
                    'plugins': [
                        {
                            'name': 'access_key_usage'
                        }
                    ]
                }
            }
        }

        oil = Oil(config)
        results = oil.scan()

        aws_results = results.get('aws', {})
        iam_results = aws_results.get('iam', {})
        plugin_results = iam_results.get('access_key_usage', [])

        self.assertNotEqual(plugin_results, [])

    def test_oil_can_scan_for_access_key_usage_with_custom_config(self):
        plugin_config = {
            'access_key_last_used_severity_two_threshold': 90,
            'access_key_last_used_severity_one_threshold': 60,
        }

        config = {
            'aws': {
                'iam': {
                    'plugins': [
                        {
                            'name': 'access_key_usage',
                            'config': plugin_config,
                        }
                    ]
                }
            }
        }

        oil = Oil(config)
        results = oil.scan()

        aws_results = results.get('aws', {})
        iam_results = aws_results.get('iam', {})
        plugin_results = iam_results.get('access_key_usage', [])

        self.assertNotEqual(plugin_results, [])

    def test_oil_can_scan_for_active_mfa_device_for_user(self):
        config = {
            'aws': {
                'iam': {
                    'plugins': [
                        {
                            'name': 'user_mfa'
                        }
                    ]
                }
            }
        }

        oil = Oil(config)
        results = oil.scan()

        aws_results = results.get('aws', {})
        iam_results = aws_results.get('iam', {})
        plugin_results = iam_results.get('user_mfa', [])

        self.assertNotEqual(plugin_results, [])

    def test_oil_can_scan_for_active_mfa_device_with_config(self):
        config = {
            'aws': {
                'iam': {
                    'plugins': [
                        {
                            'name': 'user_mfa',
                            'config': {
                                'root_user_enabled_message': 'Enabled: {username}',
                                'root_user_not_enabled_message': 'Not Enabled: {username}',
                                'root_user_not_enabled_severity_level': 1,
                                'enabled_message': 'Enabled: {username}',
                                'not_enabled_message': 'Not Enabled: {username}',
                                'not_enabled_severity_level': 1,
                            }
                        }
                    ]
                }
            }
        }

        oil = Oil(config)
        results = oil.scan()

        aws_results = results.get('aws', {})
        iam_results = aws_results.get('iam', {})
        plugin_results = iam_results.get('user_mfa', [])

        self.assertNotEqual(plugin_results, [])

    def test_oil_can_scan_for_password_rotation_date_for_user(self):
        config = {
            'aws': {
                'iam': {
                    'plugins': [
                        {
                            'name': 'user_password_rotation'
                        }
                    ]
                }
            }
        }

        oil = Oil(config)
        results = oil.scan()

        aws_results = results.get('aws', {})
        iam_results = aws_results.get('iam', {})
        plugin_results = iam_results.get('user_password_rotation', [])

        self.assertNotEqual(plugin_results, [])

    def test_oil_can_scan_for_active_mfa_device_with_config(self):
        config = {
            'aws': {
                'iam': {
                    'plugins': [
                        {
                            'name': 'user_password_rotation',
                            'config': {
                                'password_rotation_severity_2_threshold': 180,
                                'password_rotation_severity_1_threshold': 90,
                                'password_rotation_severity_2_message': (
                                    '{days} days since last rotation for {username} '
                                ),
                                'password_rotation_severity_1_message': (
                                    '{days} days since last rotation for {username}'
                                ),
                                'password_rotation_severity_0_message': (
                                    '{username} is not violating password rotation '
                                    'best practices'
                                ),
                                'password_rotation_severity_0_message': (
                                    'No password for this user'
                                ),
                            }
                        }
                    ]
                }
            }
        }

        oil = Oil(config)
        results = oil.scan()

        aws_results = results.get('aws', {})
        iam_results = aws_results.get('iam', {})
        plugin_results = iam_results.get('user_password_rotation', [])

        self.assertNotEqual(plugin_results, [])
