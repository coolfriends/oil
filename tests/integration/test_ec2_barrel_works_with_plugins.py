import os
import unittest
from unittest.mock import MagicMock
from oil import Oil
from oil.barrels.aws import EC2Barrel
from oil.plugins.aws.ec2 import InstanceNameTagPlugin
from tests.fixtures.aws.ec2 import describe_instances_paginator_with_name_tags


class EC2BarrelWorksWithPluginsTestCase(unittest.TestCase):
    def client_mock(self, fixture):
        client = MagicMock()
        paginator = MagicMock()
        response_iterator = fixture

        paginator.paginate.return_value = response_iterator
        client.get_paginator.return_value = paginator

        return client

    def test_ec2_data_processed_into_desired_results(self):
        plugin = InstanceNameTagPlugin()
        client = self.client_mock(
            describe_instances_paginator_with_name_tags
        )
        barrel = EC2Barrel(client)
        instances = barrel.describe_instances()
        data = {
            'some-region': instances
        }
        results = plugin.run(data)
        results_keys = list(results[0].keys())

        expected = set([
            'resource',
            'region',
            'severity',
            'message'
        ])

        self.assertCountEqual(list(results[0].keys()), expected)
