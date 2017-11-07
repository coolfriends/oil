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
        clients = {
            'us-east-1': self.client_mock(
                describe_instances_paginator_with_name_tags
            )
        }
        barrel = EC2Barrel(clients)
        instances_by_region = barrel.describe_instances()

        # TODO: This object would normally be created by oil
        api_data = {
            'aws': {
                'ec2': {
                    'us-east-1': {
                        'describe_instances': instances_by_region['us-east-1']
                    }
                }
            }
        }

        results = plugin.run(api_data)
        results_keys = list(results[0].keys())

        expected = set([
            'resource',
            'region',
            'severity',
            'message'
        ])

        self.assertCountEqual(list(results[0].keys()), expected)
