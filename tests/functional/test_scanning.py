"""
These tests require functioning AWS access keys. That means the following
environment variables must be set. Necessary permissions for running these
tests should be documented. Functional tests also should NOT run unless
specified.

AWS_SECRET_ACCESS_KEY
AWS_ACCESS_KEY_ID
"""
import os
import unittest
from oil import Oil
from oil.plugins.cloudfront import insecure_protocols
from oil.plugins.cloudfront import default_plugins

class ScanningTestCase(unittest.TestCase):
    def test_user_can_run_a_scan_using_env_variables_by_default(self):
        plugins = [insecure_protocols]
        oil = Oil(plugins)
        data = oil.scan()
        self.assertIsNotNone(data)

    def test_user_can_scan_with_a_single_plugin(self):
        plugins = [insecure_protocols]
        oil = Oil(plugins)
        data = oil.scan()
        self.assertIsNotNone(data)

    def test_user_can_scan_with_a_single_service(self):
        plugins = default_plugins
        oil = Oil(default_plugins)
        data = oil.scan()
        self.assertIsNotNone(data)

    @unittest.skip('Not ready to test against ')
    def test_user_can_scan_with_provided_aws_credentials(self):
        aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
        aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY'];
        oil = Oil()
        plugins = default_plugins
        oil = Oil(default_plugins,
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)
        data = oil.scan()
        self.assertIsNotNone(data)
