import unittest
from unittest.mock import MagicMock, patch
from oil.barrels.aws import CloudTrailBarrel


class CloudTrailBarrelTestCase(unittest.TestCase):

    def client_mock(self, fixture):
        client = MagicMock()
        client.describe_trails.return_value = fixture
        return client

    def test_has_correct_supported_regions(self):
        supported_regions = set([
            'us-east-2',
            'us-east-1',
            'us-west-2',
            'us-west-1',
            'ap-northeast-1',
            'ap-northeast-2',
            'ap-south-1',
            'ap-southheast-1',
            'ap-southheast-2',
            'ca-central-1',
            'cn-northwest-1',
            'eu-central-1',
            'eu-west-1',
            'eu-west-2',
            'eu-west-3',
            'sa-east-1',
        ])
        barrel = CloudTrailBarrel({}, clients={})
        self.assertEqual(supported_regions, barrel.supported_regions)

    @patch("boto3.client")
    def test_default_clients(self, mock_client):
        mock_client.return_value = MagicMock()
        barrel = CloudTrailBarrel({})

        for region, client in barrel.clients.items():
            self.assertIn(region, barrel.supported_regions)

    def test_tap_functions_with_describe_trails(self):
        fixture = {
            'trailList': [
                {
                    'Name': 'a_trail',
                }
            ]
        }
        clients = {
            'us-east-1': self.client_mock(fixture)
        }
        barrel = CloudTrailBarrel({}, clients=clients)
        tap_return = barrel.tap('describe_trails')
        describe_trails_return = barrel.describe_trails()

        self.assertEqual(describe_trails_return, tap_return)

    def test_tap_throws_error_with_unsupported_call(self):
        barrel = CloudTrailBarrel({})

        with self.assertRaises(RuntimeError):
            barrel.tap('unsupported_call')

    def test_describe_trails_returns_trails_by_region(self):
        fixture_1 = {
            'trailList': [
                {
                    'Name': 'a_trail',
                }
            ]
        }
        fixture_2 = {
            'trailList': [
                {
                    'Name': 'another_trail',
                }
            ]
        }
        clients = {
            'us-east-1': self.client_mock(fixture_1),
            'us-east-2': self.client_mock(fixture_2),
        }
        barrel = CloudTrailBarrel({}, clients=clients)

        results = barrel.describe_trails()

        expected = {
            'us-east-1': [
                {
                    'Name': 'a_trail'
                },
            ],
            'us-east-2': [
                {
                    'Name': 'another_trail'
                },
            ]
        }

        self.assertEqual(results, expected)

    def test_describe_trails_empty(self):
        fixture = {
            'trailList': [
            ]
        }
        clients = {
            'us-east-1': self.client_mock(fixture)
        }

        barrel = CloudTrailBarrel({}, clients=clients)

        results = barrel.describe_trails()

        expected = {
            'us-east-1': []
        }

        self.assertEqual(results, expected)
