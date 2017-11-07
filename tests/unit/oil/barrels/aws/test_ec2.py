import unittest
from unittest.mock import MagicMock
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

    def test_tap_functions_with_describe_instances(self):
        clients = {
            'us-east-1': self.client_mock(
                boto3_describe_instances_paginator_one_field
            )
        }
        barrel = EC2Barrel(clients)
        tap_return = barrel.tap('describe_instances')
        describe_instances_return = barrel.describe_instances()

        self.assertEqual(describe_instances_return, tap_return)

    def test_describe_instances_returns_only_instances(self):
        clients = {
            'us-east-1': self.client_mock(
                boto3_describe_instances_paginator_one_field
            )
        }
        barrel = EC2Barrel(clients)

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
        barrel = EC2Barrel(clients)

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
        barrel = EC2Barrel(clients)

        results = barrel.describe_instances()

        expected = {
            'us-east-1': []
        }

        self.assertEqual(results, expected)
