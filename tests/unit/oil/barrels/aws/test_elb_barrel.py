import unittest
from unittest.mock import MagicMock
from oil.barrels.aws import ELBBarrel


class ELBBarrelTestCase(unittest.TestCase):

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
        https://docs.aws.amazon.com/general/latest/gr/rande.html#elb_region
        """
        supported_regions = set([
            'us-east-2',
            'us-east-1',
            'us-west-1',
            'us-west-2',
            'ca-central-1',
            'ap-south-1',
            'ap-northeast-2',
            'ap-northeast-1',
            'ap-southeast-2',
            'ap-southeast-1',
            'cn-northwest-1',
            'eu-central-1',
            'eu-west-1',
            'eu-west-2',
            'eu-west-3',
            'sa-east-1'
        ])
        barrel = ELBBarrel({}, clients={})
        self.assertEqual(supported_regions, barrel.supported_regions)

    def test_describe_load_balancers_by_region(self):
        fixture_1 = [
            {
                'LoadBalancers': [
                    {
                        'LoadBalancerArn': 'arn 1'
                    },
                    {
                        'LoadBalancerArn': 'arn 2'
                    },
                ]
            },
            {
                'LoadBalancers': [
                    {
                        'LoadBalancerArn': 'arn 3'
                    },
                    {
                        'LoadBalancerArn': 'arn 4'
                    },
                ]
            },
        ]

        fixture_2 = [
            {
                'LoadBalancers': [
                    {
                        'LoadBalancerArn': 'arn 5'
                    },
                    {
                        'LoadBalancerArn': 'arn 6'
                    },
                ]
            },
            {
                'LoadBalancers': [
                    {
                        'LoadBalancerArn': 'arn 7'
                    },
                    {
                        'LoadBalancerArn': 'arn 8'
                    },
                ]
            },
        ]
        clients = {
            'us-east-1': self.client_mock(fixture_1),
            'us-east-2': self.client_mock(fixture_2),
        }
        barrel = ELBBarrel({}, clients=clients)

        results = barrel.tap('describe_load_balancers')

        expected = {
            'us-east-1': [
                {
                    'LoadBalancerArn': 'arn 1'
                },
                {
                    'LoadBalancerArn': 'arn 2'
                },
                {
                    'LoadBalancerArn': 'arn 3'
                },
                {
                    'LoadBalancerArn': 'arn 4'
                },
            ],
            'us-east-2': [
                {
                    'LoadBalancerArn': 'arn 5'
                },
                {
                    'LoadBalancerArn': 'arn 6'
                },
                {
                    'LoadBalancerArn': 'arn 7'
                },
                {
                    'LoadBalancerArn': 'arn 8'
                },
            ],
        }

        self.assertEqual(results, expected)
