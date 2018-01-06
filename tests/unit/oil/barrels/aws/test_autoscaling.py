import unittest
from unittest.mock import MagicMock, patch
from oil.barrels.aws import AutoScalingBarrel


class AutoScalingBarrelTestCase(unittest.TestCase):
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
            'us-west-2',
            'us-west-1',
            'ap-northeast-1',
            'ap-northeast-2',
            'ap-south-1',
            'ap-southheast-1',
            'ap-southheast-2',
            'ca-central-1',
            'cn-north-1',
            'cn-northwest-1',
            'eu-central-1',
            'eu-west-1',
            'eu-west-2',
            'eu-west-3',
            'sa-east-1',
        ])
        barrel = AutoScalingBarrel({}, clients={})
        self.assertEqual(supported_regions, barrel.supported_regions)

    @patch("boto3.client")
    def test_default_clients(self, mock_client):
        mock_client.return_value = MagicMock()
        barrel = AutoScalingBarrel({})

        for region, client in barrel.clients.items():
            self.assertIn(region, barrel.supported_regions)

    def test_tap_functions_with_describe_auto_scaling_groups(self):
        fixture = [
            {
                'AutoScalingGroups': [
                    {
                        'AutoScalingGroupName': 'a_group',
                    }
                ]
            }
        ]
        clients = {
            'us-east-1': self.client_mock(fixture)
        }
        barrel = AutoScalingBarrel({}, clients=clients)
        tap_return = barrel.tap('describe_auto_scaling_groups')
        auto_scaling_return = barrel.describe_auto_scaling_groups()

        self.assertEqual(auto_scaling_return, tap_return)

    def test_tap_throws_error_with_unsupported_call(self):
        barrel = AutoScalingBarrel({})

        with self.assertRaises(RuntimeError):
            barrel.tap('unsupported_call')

    def test_auto_scaling_returns_groups_by_region(self):
        fixture_1 = [
            {
                'AutoScalingGroups': [
                    {
                        'AutoScalingGroupName': 'a_group',
                    }
                ]
            }
        ]
        fixture_2 = [
            {
                'AutoScalingGroups': [
                    {
                        'AutoScalingGroupName': 'a_group_2',
                    }
                ]
            }
        ]
        clients = {
            'us-east-1': self.client_mock(fixture_1),
            'us-east-2': self.client_mock(fixture_2),
        }
        barrel = AutoScalingBarrel({}, clients=clients)

        results = barrel.describe_auto_scaling_groups()

        expected = {
            'us-east-1': [
                {
                    'AutoScalingGroupName': 'a_group'
                },
            ],
            'us-east-2': [
                {
                    'AutoScalingGroupName': 'a_group_2'
                },
            ]
        }

        self.assertEqual(results, expected)

    def test_describe_auto_scaling_groups_empty(self):
        fixture = [  # Multiple pages of empty
            {
                'AutoScalingGroups': [
                ]
            }
        ]
        clients = {
            'us-east-1': self.client_mock(fixture)
        }
        barrel = AutoScalingBarrel({}, clients=clients)

        results = barrel.describe_auto_scaling_groups()

        expected = {
            'us-east-1': []
        }

        self.assertEqual(results, expected)
