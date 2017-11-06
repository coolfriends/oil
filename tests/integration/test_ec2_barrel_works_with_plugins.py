import os
import unittest
from unittest.mock import MagicMock
from oil import Oil
from oil.barrels.aws import EC2Barrel
from oil.plugins.aws.ec2 import InstanceNameTagPlugin


class EC2BarrelWorksWithPluginsTestCase(unittest.TestCase):
    def client_mock(self):
        client = MagicMock()
        paginator = MagicMock()
        response_iterator = response_iterator_fixture

        paginator.paginate.return_value = response_iterator
        client.get_paginator.return_value = paginator

        return client

    def test_ec2_data_processed_into_desired_results(self):
        plugin = InstanceNameTagPlugin()
        client = self.client_mock()
        barrel = EC2Barrel(client)
        data = barrel.describe_instances()
        results = plugin.run(data)
        expected = [
            'resource',
            'region',
            'severity',
            'message'
        ]

        self.assertEqual(list(results[0].keys()), expected)
