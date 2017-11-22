import unittest
from unittest.mock import MagicMock, patch
from oil.barrels.aws import CloudFrontBarrel
from tests.fixtures.aws.cloudfront import response_iterator_fixture


class CloudFrontBarrelTestCase(unittest.TestCase):
    def client_mock(self, fixture):
        client = MagicMock()
        paginator = MagicMock()
        response_iterator = fixture

        paginator.paginate.return_value = response_iterator
        client.get_paginator.return_value = paginator

        return client

    def test_has_correct_supported_regions(self):
        supported_regions = set([
            'aws-global'
        ])
        barrel = CloudFrontBarrel({}, clients={})
        self.assertEqual(supported_regions, barrel.supported_regions)

    @patch("boto3.client")
    def test_default_clients(self, mock_client):
        mock_client.return_value = MagicMock()
        barrel = CloudFrontBarrel({})

        for region, client in barrel.clients.items():
            self.assertIn(region, barrel.supported_regions)

    def test_tap_functions_with_list_distributions(self):
        fixture = [
            {
                'DistributionList': {
                    'Items': []
                }
            }
        ]
        clients = {
            'aws-global': self.client_mock(fixture)
        }
        barrel = CloudFrontBarrel({}, clients=clients)
        tap_return = barrel.tap('list_distributions')
        list_distributions_return = barrel.list_distributions()

        self.assertEqual(list_distributions_return, tap_return)

    def test_tap_throws_error_with_unsupported_call(self):
        barrel = CloudFrontBarrel({})

        with self.assertRaises(RuntimeError):
            barrel.tap('unsupported_call')

    def test_list_distributions_returns_only_distributions(self):
        clients = {
            'aws-global': self.client_mock(response_iterator_fixture)
        }
        barrel = CloudFrontBarrel({}, clients=clients)

        results = barrel.list_distributions()

        expected = {
            'aws-global': [
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
        }

        self.assertEqual(results, expected)

    def test_list_distributions_empty_with_no_distributions(self):
        fixture = [ # Multiple pages of empty
            {
                'DistributionList': {
                    'Items': []
                }
            }
        ]
        clients = {
            'aws-global': self.client_mock(fixture)
        }
        barrel = CloudFrontBarrel({}, clients=clients)

        results = barrel.list_distributions()

        expected = {
            'aws-global': []
        }

        self.assertEqual(results, expected)

    def test_list_distributions_returns_empty_list_with_no_items_key(self):
        fixture = [ # Multiple pages of empty
            {
                'DistributionList': {
                }
            }
        ]
        clients = {
            'aws-global': self.client_mock(fixture)
        }
        barrel = CloudFrontBarrel({}, clients=clients)

        results = barrel.list_distributions()

        expected = {
            'aws-global': []
        }

        self.assertEqual(results, expected)
