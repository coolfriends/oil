import unittest
import os

from oil import Oil
from oil.barrels.aws import IAMBarrel
from oil.plugins.aws.iam import ExtraAccessKeyPlugin
from oil.plugins.aws.iam import AccessKeyUsagePlugin
from oil.plugins.aws.iam import UserMFAPlugin
from oil.plugins.aws.iam import UserPasswordRotationPlugin
from oil.plugins.aws.iam import TotalUsersPlugin


@unittest.skipIf(os.environ.get('OIL_FUNCTIONAL_TESTS', 'False') != 'True', "Skipping functional tests")
class IAMTestCase(unittest.TestCase):
    def test_oil_can_scan_for_extra_access_key(self):
        oil = Oil()
        oil.register_barrel(IAMBarrel)
        oil.register_plugin(ExtraAccessKeyPlugin)
        results = oil.scan()

        aws_results = results.get('aws', {})
        iam_results = aws_results.get('iam', {})
        plugin_results = iam_results.get('extra_access_key', [])

        self.assertNotEqual(plugin_results, [])

    def test_oil_can_scan_for_access_key_usage(self):
        oil = Oil()
        oil.register_barrel(IAMBarrel)
        oil.register_plugin(AccessKeyUsagePlugin)
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

        oil = Oil()
        oil.register_barrel(IAMBarrel)
        oil.register_plugin(AccessKeyUsagePlugin, plugin_config)
        results = oil.scan()

        aws_results = results.get('aws', {})
        iam_results = aws_results.get('iam', {})
        plugin_results = iam_results.get('access_key_usage', [])

        self.assertNotEqual(plugin_results, [])

    def test_oil_can_scan_for_active_mfa_device_for_user(self):
        oil = Oil()
        oil.register_barrel(IAMBarrel)
        oil.register_plugin(UserMFAPlugin)
        results = oil.scan()

        aws_results = results.get('aws', {})
        iam_results = aws_results.get('iam', {})
        plugin_results = iam_results.get('user_mfa', [])

        self.assertNotEqual(plugin_results, [])

    def test_oil_can_scan_for_active_mfa_device_with_config(self):
        plugin_config = {
            'root_user_enabled_message': 'Enabled: {username}',
            'root_user_not_enabled_message': 'Not Enabled: {username}',
            'root_user_not_enabled_severity_level': 1,
            'enabled_message': 'Enabled: {username}',
            'not_enabled_message': 'Not Enabled: {username}',
            'not_enabled_severity_level': 1,
        }

        oil = Oil()
        oil.register_barrel(IAMBarrel)
        oil.register_plugin(UserMFAPlugin, plugin_config)
        results = oil.scan()

        aws_results = results.get('aws', {})
        iam_results = aws_results.get('iam', {})
        plugin_results = iam_results.get('user_mfa', [])

        self.assertNotEqual(plugin_results, [])

    def test_oil_can_scan_for_password_rotation_date_for_user(self):
        oil = Oil()
        oil.register_barrel(IAMBarrel)
        oil.register_plugin(UserPasswordRotationPlugin)
        results = oil.scan()

        aws_results = results.get('aws', {})
        iam_results = aws_results.get('iam', {})
        plugin_results = iam_results.get('user_password_rotation', [])

        self.assertNotEqual(plugin_results, [])

    def test_oil_can_scan_for_password_rotation_with_config(self):
        plugin_config = {
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
        oil = Oil()
        oil.register_barrel(IAMBarrel)
        oil.register_plugin(UserPasswordRotationPlugin, plugin_config)
        results = oil.scan()

        aws_results = results.get('aws', {})
        iam_results = aws_results.get('iam', {})
        plugin_results = iam_results.get('user_password_rotation', [])

        self.assertNotEqual(plugin_results, [])

    def test_oil_can_scan_for_total_users(self):
        config = {
            'aws': {
                'iam': {
                    'plugins': [
                        {
                            'name': 'total_users',
                        }
                    ]
                }
            }
        }

        oil = Oil(config)
        oil.register_barrel(IAMBarrel)
        oil.register_plugin(TotalUsersPlugin)
        results = oil.scan()

        aws_results = results.get('aws', {})
        iam_results = aws_results.get('iam', {})
        plugin_results = iam_results.get('total_users', [])

        self.assertNotEqual(plugin_results, [])

    def test_oil_can_scan_for_total_users_with_config(self):
        plugin_config = {
            'total_users_severity_2_threshold': 50,
            'total_users_severity_1_threshold': 20,
            'total_users_severity_2_message': (
                'Total users: {total_users}'
            ),
            'total_users_severity_1_message': (
                'Total users: {total_users}'
            ),
            'total_users_severity_0_message': (
                'Total users: {total_users}'
            ),
            'no_users_message': (
                'No users in this AWS account'
            ),
        }

        oil = Oil()
        oil.register_barrel(IAMBarrel)
        oil.register_plugin(TotalUsersPlugin, plugin_config)
        results = oil.scan()

        aws_results = results.get('aws', {})
        iam_results = aws_results.get('iam', {})
        plugin_results = iam_results.get('total_users', [])

        self.assertNotEqual(plugin_results, [])
