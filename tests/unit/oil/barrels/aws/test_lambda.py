import unittest
from unittest.mock import MagicMock
from oil.barrels.aws import LambdaBarrel


class LambdaBarrelTestCase(unittest.TestCase):

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
            'cn-north-1',
            'eu-central-1',
            'eu-west-1',
            'eu-west-2',
            'sa-east-1',
        ])
        barrel = LambdaBarrel({}, clients={})
        self.assertEqual(supported_regions, barrel.supported_regions)

    def test_tap_functions_with_list_functions(self):
        client = MagicMock()
        clients = {
            'us-east-1': client
        }
        barrel = LambdaBarrel({}, clients=clients)
        tap_return = barrel.tap('list_functions')
        expected = barrel.list_functions()

        self.assertEqual(expected, tap_return)

    def test_can_list_functions_by_region(self):
        fixture_1 = {
            'FunctionName': 'Function 1',
        }
        fixture_2 = {
            'FunctionName': 'Function 2',
        }
        clients = {
            'us-east-1': self.client_mock(fixture_1),
            'us-east-2': self.client_mock(fixture_2),
        }
        barrel = LambdaBarrel({}, clients=clients)

        results = barrel.list_functions()

        expected = {
            'us-east-1': {
                'UserId': 'AWS User ID'
            },
            'us-east-2': {
                'UserId': 'AWS User ID2'
            },
        }

        self.assertEqual(results, expected)

    def test_can_list_functions_empty(self):
        fixture_1 = {
            'FunctionName': 'Function 1',
        }
        fixture_2 = {
            'FunctionName': 'Function 2',
        }
        clients = {
            'us-east-1': self.client_mock(fixture_1),
            'us-east-2': self.client_mock(fixture_2),
        }
        barrel = LambdaBarrel({}, clients=clients)

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
