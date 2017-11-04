import unittest
from unittest.mock import MagicMock
from oil.barrels.aws import CloudFrontBarrel
from tests.fixtures.aws.cloudfront import response_iterator_fixture


class CloudFrontBarrelTestCase(unittest.TestCase):
    def client_mock(self):
        client = MagicMock()
        paginator = MagicMock()
        response_iterator = response_iterator_fixture

        paginator.paginate.return_value = response_iterator
        client.get_paginator.return_value = paginator

        return client

    def test_list_distributions_returns_only_distributions(self):
        client = self.client_mock()
        barrel = CloudFrontBarrel(client)

        results = barrel.list_distributions()

        expected = [
            {
                "ARN": "some arn",
                "ViewerCertificate": {
                    "MinimumProtocolVersion": 'example value'
                }
            },
            {
                "ARN": "another arn",
                "ViewerCertificate": {
                    "MinimumProtocolVersion": 'test value'
                }
            },
            {
                "ARN": "test arn",
                "ViewerCertificate": {
                    "MinimumProtocolVersion": 'some value'
                }
            },
            {
                "ARN": "example arn",
                "ViewerCertificate": {
                    "MinimumProtocolVersion": 'another value'
                }
            }
        ]

        self.assertEqual(results, expected)
