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

    def test_describe_instances_returns_only_instances(self):
        client = self.client_mock(
            boto3_describe_instances_paginator_one_field
        )
        barrel = EC2Barrel(client)

        results = barrel.describe_instances()

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

        self.assertEqual(results, expected)
