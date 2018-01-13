import unittest
from unittest.mock import MagicMock
from oil.barrels.aws import STSBarrel


class STSBarrelTestCase(unittest.TestCase):

    def client_mock(self, fixture):
        client = MagicMock()
        client.get_caller_identity.return_value = fixture
        return client

    def test_has_correct_supported_regions(self):
        """
        Reference:
        https://docs.aws.amazon.com/general/latest/gr/rande.html#sts_region
        """
        supported_regions = set([
            'aws-global',
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
            'eu-central-1',
            'eu-west-1',
            'eu-west-2',
            'sa-east-1',
        ])
        barrel = STSBarrel({}, clients={})
        self.assertEqual(supported_regions, barrel.supported_regions)

    def test_tap_functions_with_get_caller_identity(self):
        fixture = {
            'UserId': 'AWS User ID',
        }
        clients = {
            'us-east-1': self.client_mock(fixture)
        }
        barrel = STSBarrel({}, clients=clients)
        tap_return = barrel.tap('get_caller_identity')
        expected_return = barrel.get_caller_identity()

        self.assertEqual(expected_return, tap_return)

    def test_tap_throws_error_with_unsupported_call(self):
        barrel = STSBarrel({})

        with self.assertRaises(RuntimeError):
            barrel.tap('unsupported_call')

    def test_get_caller_identity_lists_by_region(self):
        fixture_1 = {
            'UserId': 'AWS User ID',
        }
        fixture_2 = {
            'UserId': 'AWS User ID2',
        }
        clients = {
            'us-east-1': self.client_mock(fixture_1),
            'us-east-2': self.client_mock(fixture_2),
        }
        barrel = STSBarrel({}, clients=clients)

        results = barrel.get_caller_identity()

        expected = {
            'us-east-1': {
                'UserId': 'AWS User ID'
            },
            'us-east-2': {
                'UserId': 'AWS User ID2'
            },
        }

        self.assertEqual(results, expected)
