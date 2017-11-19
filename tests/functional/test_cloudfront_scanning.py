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

from oil.plugins.aws.cloudfront import HTTPSPlugin
from oil.plugins.aws.cloudfront import S3OriginAccessIdentityPlugin

from oil.barrels.aws import CloudFrontBarrel


@unittest.skipIf(os.environ.get('OIL_FUNCTIONAL_TESTS', 'False') != 'True', "Skipping functional tests")
class ScanningTestCase(unittest.TestCase):

    def test_oil_can_scan_for_https_usage(self):
        oil = Oil()
        oil.register_barrel(CloudFrontBarrel)
        oil.register_plugin(HTTPSPlugin)
        results = oil.scan()

        aws_results = results.get('aws', {})
        cloudfront_results = aws_results.get('cloudfront', {})
        plugin_results = cloudfront_results.get('https', [])

        self.assertNotEqual(plugin_results, [])

    def test_oil_can_scan_for_s3_origin_access_identity(self):
        oil = Oil()
        oil.register_barrel(CloudFrontBarrel)
        oil.register_plugin(S3OriginAccessIdentityPlugin)
        results = oil.scan()

        aws_results = results.get('aws', {})
        cloudfront_results = aws_results.get('cloudfront', {})
        plugin_results = cloudfront_results.get('s3_origin_access_identity', [])

        self.assertNotEqual(plugin_results, [])
