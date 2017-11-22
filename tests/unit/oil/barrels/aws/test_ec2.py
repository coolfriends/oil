import unittest
from unittest.mock import MagicMock, patch
from oil.barrels.aws import EC2Barrel
from tests.fixtures.aws.ec2 import boto3_describe_instances_paginator_one_field


class EC2BarrelTestCase(unittest.TestCase):
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
            'sa-east-1'
        ])
        barrel = EC2Barrel({})
        self.assertEqual(supported_regions, barrel.supported_regions)

    @patch("boto3.client")
    def test_default_clients(self, mock_client):
        mock_client.return_value = MagicMock()
        barrel = EC2Barrel({})

        for region, client in barrel.clients.items():
            self.assertIn(region, barrel.supported_regions)

    def test_tap_functions_with_describe_instances(self):
        clients = {
            'us-east-1': self.client_mock(
                boto3_describe_instances_paginator_one_field
            )
        }
        barrel = EC2Barrel({}, clients=clients)
        tap_return = barrel.tap('describe_instances')
        describe_instances_return = barrel.describe_instances()

        self.assertEqual(describe_instances_return, tap_return)

    def test_tap_functions_with_describe_security_groups(self):
        clients = {
            'us-east-1': self.client_mock(
                boto3_describe_instances_paginator_one_field
            )
        }
        barrel = EC2Barrel({}, clients=clients)
        tap_return = barrel.tap('describe_security_groups')
        describe_security_groups_return = barrel.describe_security_groups()

        self.assertEqual(describe_security_groups_return, tap_return)

    def test_tap_throws_error_with_unsupported_call(self):
        barrel = EC2Barrel({})

        with self.assertRaises(RuntimeError):
            tap_return = barrel.tap('unsupported_call')

    def test_describe_instances_returns_only_instances(self):
        clients = {
            'us-east-1': self.client_mock(
                boto3_describe_instances_paginator_one_field
            )
        }
        barrel = EC2Barrel({}, clients=clients)

        results = barrel.describe_instances()
        results_from_region = results['us-east-1']

        expected = [
            {
                'InstanceId': 'instance1'
            },
            {
                'InstanceId': 'instance2'
            },
            {
                'InstanceId': 'instance3'
            },
            {
                'InstanceId': 'instance4'
            },
            {
                'InstanceId': 'instance5'
            },
            {
                'InstanceId': 'instance6'
            },
            {
                'InstanceId': 'instance7'
            },
            {
                'InstanceId': 'instance8'
            },
        ]

        self.assertEqual(results_from_region, expected)

    def test_describe_instances_empty_with_no_instances(self):
        fixture = [ # Multiple pages of empty
            {
                'Reservations': [
                    {
                        'Instances': []
                    }
                ]
            }
        ]
        clients = {
            'us-east-1': self.client_mock(fixture)
        }
        barrel = EC2Barrel({}, clients=clients)

        results = barrel.describe_instances()

        expected = {
            'us-east-1': []
        }

        self.assertEqual(results, expected)

    def test_describe_instances_returns_empty_list_with_no_instances_key(self):
        fixture = [ # Multiple pages of empty
            {
                'Reservations': [
                    {
                    }
                ]
            }
        ]
        clients = {
            'us-east-1': self.client_mock(fixture)
        }
        barrel = EC2Barrel({}, clients=clients)

        results = barrel.describe_instances()

        expected = {
            'us-east-1': []
        }

        self.assertEqual(results, expected)

    def test_describe_security_groups_returns_only_security_groups(self):
        fixture = [
            {
                'SecurityGroups': [
                    {
                        'GroupName': 'group1'
                    },
                    {
                        'GroupName': 'group2'
                    }
                ]
            },
            {
                'SecurityGroups': [
                    {
                        'GroupName': 'group3'
                    },
                    {
                        'GroupName': 'group4'
                    },
                ]
            }
        ]
        clients = {
            'us-east-1': self.client_mock(fixture)
        }
        barrel = EC2Barrel({}, clients=clients)

        results = barrel.describe_security_groups()
        expected = {
            'us-east-1': [
                {
                    'GroupName': 'group1'
                },
                {
                    'GroupName': 'group2'
                },
                {
                    'GroupName': 'group3'
                },
                {
                    'GroupName': 'group4'
                }
            ]
        }

        self.assertEqual(results, expected)

    def test_describe_security_groups_empty(self):
        fixture = [
            {
                'SecurityGroups': [
                ]
            }
        ]
        clients = {
            'us-east-1': self.client_mock(fixture)
        }
        barrel = EC2Barrel({}, clients=clients)

        results = barrel.describe_security_groups()

        expected = {
            'us-east-1': []
        }

        self.assertEqual(results, expected)

    def test_describe_security_groups_returns_empty_list_with_missing_key(self):
        fixture = [
            {
                # Security groups key should be here
            }
        ]
        clients = {
            'us-east-1': self.client_mock(fixture)
        }
        barrel = EC2Barrel({}, clients=clients)

        results = barrel.describe_security_groups()

        expected = {
            'us-east-1': []
        }

        self.assertEqual(results, expected)
