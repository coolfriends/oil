import unittest
from unittest.mock import MagicMock, patch
from oil.barrels.aws import RDSBarrel


class RDSBarrelTestCase(unittest.TestCase):
    def client_mock(self, fixture):
        client = MagicMock()
        paginator = MagicMock()
        response_iterator = fixture

        paginator.paginate.return_value = response_iterator
        client.get_paginator.return_value = paginator

        return client

    def test_has_correct_supported_regions(self):
        supported_regions = set([
            'us-east-2',
            'us-east-1',
            'us-west-1',
            'us-west-2',
            'ap-south-1',
            'ap-northeast-1',
            'ap-northeast-2',
            'ap-southeast-1',
            'ap-southeast-2',
            'ca-central-1',
            'eu-central-1',
            'eu-west-1',
            'eu-west-2',
            'sa-east-1',
        ])
        barrel = RDSBarrel({})
        self.assertEqual(supported_regions, barrel.supported_regions)

    @patch("boto3.client")
    def test_supported_clients(self, mock_client):
        mock_client.return_value = MagicMock()
        barrel = RDSBarrel({})

        for region, client in barrel.clients.items():
            self.assertIn(region, barrel.supported_regions)

    def test_tap_functions_with_describe_db_instances(self):
        clients = {
            'us-east-1': self.client_mock(
                [
                    {
                        'DBInstances': []
                    }
                ]
            )
        }
        barrel = RDSBarrel({}, clients=clients)
        tap_return = barrel.tap('describe_db_instances')
        describe_db_instances_return = barrel.describe_db_instances()

        self.assertEqual(describe_db_instances_return, tap_return)

    def test_tap_throws_error_with_unsupported_call(self):
        barrel = RDSBarrel({}, clients=[])

        with self.assertRaises(RuntimeError):
            barrel.tap('unsupported_call')

    def test_describe_db_instances_returns_only_db_instances(self):
        clients = {
            'us-east-1': self.client_mock(
                [
                    {
                        'DBInstances': [
                            {
                                'DBInstanceIdentifier': 'id1'
                            }
                        ]
                    },
                    {
                        'DBInstances': [
                            {
                                'DBInstanceIdentifier': 'id2'
                            }
                        ]
                    },
                ]
            )
        }
        barrel = RDSBarrel({}, clients=clients)

        results = barrel.describe_db_instances()
        results_from_region = results['us-east-1']

        expected = [
            {
                'DBInstanceIdentifier': 'id1'
            },
            {
                'DBInstanceIdentifier': 'id2'
            },
        ]

        self.assertEqual(results_from_region, expected)

    def test_describe_db_instances_empty_with_no_db_instances(self):
        fixture = [ # Multiple pages of empty
            {
                'DBInstances': []
            }
        ]

        clients = {
            'us-east-1': self.client_mock(fixture)
        }
        barrel = RDSBarrel({}, clients=clients)

        results = barrel.describe_db_instances()

        expected = {
            'us-east-1': []
        }

        self.assertEqual(results, expected)

    def test_describe_instances_returns_empty_list_with_no_db_instances_key(self):
        fixture = [
            {
            }
        ]
        clients = {
            'us-east-1': self.client_mock(fixture)
        }
        barrel = RDSBarrel({}, clients=clients)

        results = barrel.describe_db_instances()

        expected = {
            'us-east-1': []
        }

        self.assertEqual(results, expected)
