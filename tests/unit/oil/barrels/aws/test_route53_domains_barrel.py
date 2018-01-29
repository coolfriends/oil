import unittest
from unittest.mock import MagicMock
from oil.barrels.aws import Route53DomainsBarrel


class Route53DomainsBarrelTestCase(unittest.TestCase):

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
        https://docs.aws.amazon.com/general/latest/gr/rande.html#r53_region
        """
        supported_regions = set([
            'us-east-1',
        ])
        barrel = Route53DomainsBarrel({}, clients={})
        self.assertEqual(supported_regions, barrel.supported_regions)

    def test_list_domains_by_region(self):
        fixture_1 = [
            {
                'Domains': [
                    {
                        'DomainName': 'domain 1'
                    },
                    {
                        'DomainName': 'domain 2'
                    },
                ]
            },
            {
                'Domains': [
                    {
                        'DomainName': 'domain 3'
                    },
                    {
                        'DomainName': 'domain 4'
                    },
                ]
            },
        ]

        fixture_2 = [
            {
                'Domains': [
                    {
                        'DomainName': 'domain 5'
                    },
                    {
                        'DomainName': 'domain 6'
                    },
                ]
            },
            {
                'Domains': [
                    {
                        'DomainName': 'domain 7'
                    },
                    {
                        'DomainName': 'domain 8'
                    },
                ]
            },
        ]
        clients = {
            'us-east-1': self.client_mock(fixture_1),
            'us-east-2': self.client_mock(fixture_2),
        }
        barrel = Route53DomainsBarrel({}, clients=clients)

        results = barrel.list_domains()

        expected = {
            'us-east-1': [
                {
                    'DomainName': 'domain 1'
                },
                {
                    'DomainName': 'domain 2'
                },
                {
                    'DomainName': 'domain 3'
                },
                {
                    'DomainName': 'domain 4'
                },
            ],
            'us-east-2': [
                {
                    'DomainName': 'domain 5'
                },
                {
                    'DomainName': 'domain 6'
                },
                {
                    'DomainName': 'domain 7'
                },
                {
                    'DomainName': 'domain 8'
                },
            ],
        }

        self.assertEqual(results, expected)
