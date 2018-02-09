import unittest
from unittest.mock import MagicMock
from oil.barrels.aws import KMSBarrel


class KMSBarrelTestCase(unittest.TestCase):

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
        https://docs.aws.amazon.com/general/latest/gr/rande.html#kms_region
        """
        supported_regions = set([
            'us-east-2',
            'us-east-1',
            'us-west-1',
            'us-west-2',
            'ap-northeast-1',
            'ap-northeast-2',
            'ap-south-1',
            'ap-southeast-1',
            'ap-southeast-2',
            'ca-central-1',
            'eu-central-1',
            'eu-west-1',
            'eu-west-2',
            'eu-west-3',
            'sa-east-1'
        ])
        barrel = KMSBarrel({}, clients={})
        self.assertEqual(supported_regions, barrel.supported_regions)

    def test_list_keys_by_region(self):
        fixture_1 = [
            {
                'Keys': [
                    {
                        'KeyId': 'key 1',
                        'KeyArn': 'arn 1',
                    },
                    {
                        'KeyId': 'key 2',
                        'KeyArn': 'arn 2',
                    },
                ],
            }
        ]

        fixture_2 = [
            {
                'Keys': [
                    {
                        'KeyId': 'key 3',
                        'KeyArn': 'arn 3',
                    },
                    {
                        'KeyId': 'key 4',
                        'KeyArn': 'arn 4',
                    },
                ],
            }
        ]
        clients = {
            'us-east-1': self.client_mock(fixture_1),
            'us-east-2': self.client_mock(fixture_2)
        }
        barrel = KMSBarrel({}, clients=clients)

        results = barrel.tap('list_keys')

        expected = {
            'us-east-1': [
                {
                    'KeyId': 'key 1',
                    'KeyArn': 'arn 1'
                },
                {
                    'KeyId': 'key 2',
                    'KeyArn': 'arn 2'
                },
            ],
            'us-east-2': [
                {
                    'KeyId': 'key 3',
                    'KeyArn': 'arn 3'
                },
                {
                    'KeyId': 'key 4',
                    'KeyArn': 'arn 4'
                },
            ],
        }

        self.assertEqual(results, expected)

    def test_describe_key_by_region(self):
        list_keys_fixture = {
            'us-east-1': [
                {
                    'KeyId': 'key 1',
                    'KeyArn': 'arn 1'
                },
            ]
        }

        client_mock_1 = MagicMock()
        client_mock_1.describe_key.return_value = {
            'KeyMetadata': {
                'KeyId': 'key 1',
                'Arn': 'arn 1'
            }
        }

        clients = {
            'us-east-1': client_mock_1,
        }
        barrel = KMSBarrel({}, clients=clients)
        barrel.cache['list_keys'] = list_keys_fixture

        results = barrel.tap('describe_key')

        expected = {
            'us-east-1': {
                'key 1': {
                    'KeyId': 'key 1',
                    'Arn': 'arn 1'
                }
            }
        }

        self.assertEqual(results, expected)

    def test_get_key_rotation_status_by_region(self):
        list_keys_fixture = {
            'us-east-1': [
                {
                    'KeyId': 'key 1',
                    'KeyArn': 'arn 1'
                },
            ]
        }

        client_mock_1 = MagicMock()
        client_mock_1.get_key_rotation_status.return_value = {
            'KeyRotationEnabled': True
        }

        clients = {
            'us-east-1': client_mock_1,
        }
        barrel = KMSBarrel({}, clients=clients)
        barrel.cache['list_keys'] = list_keys_fixture

        results = barrel.tap('get_key_rotation_status')

        expected = {
            'us-east-1': {
                'key 1': {
                    'KeyRotationEnabled': True
                }
            }
        }

        self.assertEqual(results, expected)
