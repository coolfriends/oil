import unittest
from unittest.mock import MagicMock
from oil.barrels.aws import CloudWatchLogsBarrel


class CloudWatchLogsBarrelCase(unittest.TestCase):

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
        https://docs.aws.amazon.com/general/latest/gr/rande.html#cwl_region
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
            'cn-north-1'
            'cn-northwest-1',
            'eu-central-1',
            'eu-west-1',
            'eu-west-2',
            'eu-west-3',
            'sa-east-1',
        ])
        barrel = CloudWatchLogsBarrel({}, clients={})
        self.assertEqual(supported_regions, barrel.supported_regions)

    def test_tap_functions_with_describe_metric_filters(self):
        fixture = [
            {
                'metricFilters': [
                    {
                        'filterName': 'a_trail',
                    }
                ]
            }
        ]
        clients = {
            'us-east-1': self.client_mock(fixture)
        }
        barrel = CloudWatchLogsBarrel({}, clients=clients)
        tap_return = barrel.tap('describe_metric_filters')
        describe_metric_filters_return = barrel.describe_metric_filters()

        self.assertEqual(describe_metric_filters_return, tap_return)

    def test_tap_throws_error_with_unsupported_call(self):
        barrel = CloudWatchLogsBarrel({})

        with self.assertRaises(RuntimeError):
            barrel.tap('unsupported_call')

    def test_describe_metric_filters_returns_filters_by_region(self):
        fixture_1 = [
            {
                'metricFilters': [
                    {
                        'filterName': 'a_filter',
                    }
                ]
            },
            {
                'metricFilters': [
                    {
                        'filterName': 'another_filter',
                    }
                ]
            }
        ]
        fixture_2 = [
            {
                'metricFilters': [
                    {
                        'filterName': 'another_other_filter',
                    }
                ]
            },
            {
                'metricFilters': [
                    {
                        'filterName': 'another_other_other_filter',
                    }
                ]
            }
        ]
        clients = {
            'us-east-1': self.client_mock(fixture_1),
            'us-east-2': self.client_mock(fixture_2),
        }
        barrel = CloudWatchLogsBarrel({}, clients=clients)

        results = barrel.describe_metric_filters()

        expected = {
            'us-east-1': [
                {
                    'filterName': 'a_filter'
                },
                {
                    'filterName': 'another_filter'
                },
            ],
            'us-east-2': [
                {
                    'filterName': 'another_other_filter'
                },
                {
                    'filterName': 'another_other_other_filter'
                },
            ]
        }

        self.assertEqual(results, expected)

    def test_describe_metric_filters_empty(self):
        fixture = [
            {
                'metricFilters': []
            }
        ]
        clients = {
            'us-east-1': self.client_mock(fixture)
        }

        barrel = CloudWatchLogsBarrel({}, clients=clients)

        results = barrel.describe_metric_filters()

        expected = {
            'us-east-1': []
        }

        self.assertEqual(results, expected)
