"""
In this file, the client kwarg is overridden because it is referring to a boto3 client.
We do not want to make actual API calls with this unit test.
"""
import unittest
from unittest.mock import MagicMock

from oil.refineries import CloudFrontRefinery
from tests.fixtures import list_distributions_fixtures as fixtures

class CloudFrontRefineryTestCase(unittest.TestCase):

    @staticmethod
    def client_mock():
        client = MagicMock()
        paginator_mock = MagicMock()
        paginator_mock.paginate.return_value = [
            fixtures.list_distributions
        ]
        client.get_paginator.return_value = paginator_mock
        return client

    def setUp(self):
        self.cloudfront_client = self.client_mock()

    def test_list_distributions_returns_distribution_objects(self):
        refinery = CloudFrontRefinery(clients={
            'cloudfront': self.cloudfront_client
        })
        results = refinery.list_distributions()
        expected = fixtures.list_distributions['DistributionList']['Items']
        self.assertEqual(results, expected)
