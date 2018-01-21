import unittest
from unittest.mock import MagicMock
from oil.barrels.aws import SESBarrel


class SESBarrelTestCase(unittest.TestCase):

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
            'us-east-1',
            'us-west-2',
            'eu-west-1',
        ])
        barrel = SESBarrel({}, clients={})
        self.assertEqual(supported_regions, barrel.supported_regions)

    def test_list_identities_by_region(self):
        fixture_1 = [
            {
                'Identities': [
                    'identity_1'
                ]
            },
            {
                'Identities': [
                    'identity_2'
                ]
            }
        ]

        fixture_2 = [
            {
                'Identities': [
                    'identity_3'
                ]
            },
            {
                'Identities': [
                    'identity_4'
                ]
            }
        ]
        clients = {
            'us-east-1': self.client_mock(fixture_1),
            'us-east-2': self.client_mock(fixture_2),
        }
        barrel = SESBarrel({}, clients=clients)

        results = barrel.list_identities()

        expected = {
            'us-east-1': [
                'identity_1',
                'identity_2',
            ],
            'us-east-2': [
                'identity_3',
                'identity_4',
            ],
        }

        self.assertEqual(results, expected)

    def test_list_identities_cached(self):
        fixture_1 = [
            {
                'Identities': [
                    'identity_1',
                    'identity_2',
                ]
            }
        ]
        fixture_2 = [
            {
                'Identities': [
                    'identity_3',
                    'identity_4',
                ]
            }
        ]
        clients = {
            'us-east-1': self.client_mock(fixture_1),
            'us-east-2': self.client_mock(fixture_2),
        }
        barrel = SESBarrel({}, clients=clients)

        results = barrel.list_identities()
        cached = barrel.cache['list_identities']

        self.assertEqual(results, cached)

    def test_list_identities_empty(self):
        fixture_1 = [
            {
                'Identities': []
            }
        ]
        fixture_2 = [
            {
                'Identities': []
            }
        ]
        clients = {
            'us-east-1': self.client_mock(fixture_1),
            'us-east-2': self.client_mock(fixture_2),
        }
        barrel = SESBarrel({}, clients=clients)

        results = barrel.list_identities()

        expected = {
            'us-east-1': [],
            'us-east-2': [],
        }

        self.assertEqual(results, expected)
