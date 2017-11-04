import os
import unittest
from unittest.mock import MagicMock
from oil import Oil
from oil.barrels.aws import CloudFrontBarrel
from oil.plugins.aws.cloudfront import TLSProtocolPlugin
from tests.fixtures.aws.cloudfront import response_iterator_fixture


class CloudfrontFetchAndProcessProtocols(unittest.TestCase):
    def client_mock(self):
        client = MagicMock()
        paginator = MagicMock()
        response_iterator = response_iterator_fixture

        paginator.paginate.return_value = response_iterator
        client.get_paginator.return_value = paginator

        return client

    def test_cloudfront_data_processed_into_desired_results(self):
        plugin = TLSProtocolPlugin()
        client = self.client_mock()
        barrel = CloudFrontBarrel(client)
        data = barrel.list_distributions()
        results = plugin.run(data)
        expected = [
            'resource',
            'region',
            'severity',
            'message'
            ]

        self.assertEqual(list(results[0].keys()), expected)
