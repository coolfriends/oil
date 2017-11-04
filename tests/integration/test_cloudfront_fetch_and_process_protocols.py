import os
import unittest
from oil import Oil
from oil.barrels.aws import CloudFrontBarrel
from oil.plugins.aws.cloudfront import TLSProtocolPlugin


class CloudfrontFetchAndProcessProtocols(unittest.TestCase):
    def test_cloudfront_data_processed_into_desired_results(self):
        plugin = TLSProtocolPlugin()
        data = CloudFrontBarrel().list_distributions()
        results = plugin.run(data)
        expected = [
            'resource',
            'region',
            'severity',
            'message'
            ]


        self.assertEqual(list(results[0].keys()), expected)
