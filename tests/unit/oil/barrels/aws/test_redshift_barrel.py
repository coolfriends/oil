import unittest
from unittest.mock import MagicMock
from oil.barrels.aws import RedShiftBarrel


class RedShiftBarrelTestCase(unittest.TestCase):

    def client_mock(self, fixture):
        client = MagicMock()
        paginator = MagicMock()
        response_iterator = fixture

        paginator.paginate.return_value = response_iterator
        client.get_paginator.return_value = paginator

        return client

    def test_has_correct_supported_regions(self):
        """
        Reference:
        https://docs.aws.amazon.com/general/latest/gr/rande.html#sts_region
        """
        supported_regions = set([
            'us-east-2',
            'us-east-1',
            'us-west-1',
            'us-west-2',
            'ap-northeast-1',
            'ap-northeast-2',
            'ap-south-1',
            'ap-southheast-1',
            'ap-southheast-2',
            'ca-central-1',
            'eu-central-1',
            'eu-west-1',
            'eu-west-2',
            'eu-west-3',
            'sa-east-1',
        ])
        barrel = RedShiftBarrel({}, clients={})
        self.assertEqual(supported_regions, barrel.supported_regions)

    def test_tap_functions_with_describe_clusters(self):
        fixture_1 = [
            {
                'Clusters': [
                    {
                        'ClusterIdentifier': 'Cluster 1',
                    }
                ]
            }
        ]
        clients = {
            'us-east-1': self.client_mock(fixture_1),
        }
        barrel = RedShiftBarrel({}, clients=clients)
        tap_return = barrel.tap('describe_clusters')
        expected = barrel.describe_clusters()

        self.assertEqual(expected, tap_return)

    def test_can_describe_clusters_by_region(self):
        fixture_1 = [
            {
                'Clusters': [
                    {
                        'ClusterIdentifier': 'Cluster 1',
                    },
                    {
                        'ClusterIdentifier': 'Cluster 2',
                    }
                ]
            }
        ]

        fixture_2 = [
            {
                'Clusters': [
                    {
                        'ClusterIdentifier': 'Cluster 3',
                    },
                    {
                        'ClusterIdentifier': 'Cluster 4',
                    }
                ]
            }
        ]
        clients = {
            'us-east-1': self.client_mock(fixture_1),
            'us-east-2': self.client_mock(fixture_2),
        }
        barrel = RedShiftBarrel({}, clients=clients)

        results = barrel.describe_clusters()

        expected = {
            'us-east-1': [
                {
                    'ClusterIdentifier': 'Cluster 1',
                },
                {
                    'ClusterIdentifier': 'Cluster 2',
                }
            ],
            'us-east-2': [
                {
                    'ClusterIdentifier': 'Cluster 3',
                },
                {
                    'ClusterIdentifier': 'Cluster 4',
                }
            ],
        }

        self.assertEqual(results, expected)

    def test_can_describe_clusters_empty(self):
        fixture_1 = [
            {
                'Clusters': []
            }
        ]
        fixture_2 = [
            {
                'Clusters': []
            }
        ]
        clients = {
            'us-east-1': self.client_mock(fixture_1),
            'us-east-2': self.client_mock(fixture_2),
        }
        barrel = RedShiftBarrel({}, clients=clients)

        results = barrel.describe_clusters()

        expected = {
            'us-east-1': [],
            'us-east-2': [],
        }

        self.assertEqual(results, expected)
