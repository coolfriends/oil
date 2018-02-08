import unittest
from unittest.mock import MagicMock
from oil.barrels.aws import S3Barrel


class S3BarrelTestCase(unittest.TestCase):

    def test_has_correct_supported_regions(self):
        """
        Reference:
        https://docs.aws.amazon.com/general/latest/gr/rande.html#s3_region
        """
        supported_regions = set([
            'us-east-2',
            'us-east-1',
            'us-west-1',
            'us-west-2',
            'ca-central-1',
            'ap-south-1',
            'ap-northeast-2',
            'ap-southeast-1',
            'ap-southeast-2',
            'ap-northeast-1',
            'eu-west-1',
            'eu-west-2',
            'eu-west-3',
            'sa-east-1'
        ])
        barrel = S3Barrel({}, clients={})
        self.assertEqual(supported_regions, barrel.supported_regions)

    def test_list_buckets_by_region(self):
        fixture_1 = {
            'Buckets': [
                {
                    'Name': 'bucket 1',
                    'CreationDate': 'a datetime'
                },
                {
                    'Name': 'bucket 2',
                    'CreationDate': 'a datetime'
                },
            ],
            'Owner': {
                'DisplayName': 'Owner display name',
                'ID': 'Owner ID'
            }

        }

        fixture_2 = {
            'Buckets': [
                {
                    'Name': 'bucket 3',
                    'CreationDate': 'a datetime'
                }
            ],
            'Owner': {
                'DisplayName': 'Owner display name',
                'ID': 'Owner ID'
            }

        }
        client_mock_1 = MagicMock()
        client_mock_1.list_buckets.return_value = fixture_1
        client_mock_2 = MagicMock()
        client_mock_2.list_buckets.return_value = fixture_2

        clients = {
            'us-east-1': client_mock_1,
            'us-east-2': client_mock_2
        }
        barrel = S3Barrel({}, clients=clients)

        results = barrel.tap('list_buckets')

        expected = {
            'us-east-1': [
                {
                    'Name': 'bucket 1',
                    'CreationDate': 'a datetime'
                },
                {
                    'Name': 'bucket 2',
                    'CreationDate': 'a datetime'
                },
            ],
            'us-east-2': [
                {
                    'Name': 'bucket 3',
                    'CreationDate': 'a datetime'
                },
            ],
        }

        self.assertEqual(results, expected)

    def test_get_bucket_acl_by_region(self):
        list_buckets_fixture = {
            'us-east-1': [
                {
                    'Name': 'bucket 1',
                    'CreationDate': 'a datetime'
                },
            ]
        }

        client_mock_1 = MagicMock()
        client_mock_1.get_bucket_acl.return_value = {
            'Grants': [
                {
                    'Grantee': {
                        'DisplayName': 'a name'
                    }
                }
            ]
        }

        clients = {
            'us-east-1': client_mock_1,
        }
        barrel = S3Barrel({}, clients=clients)
        barrel.cache['list_buckets'] = list_buckets_fixture

        results = barrel.tap('get_bucket_acl')

        expected = {
            'us-east-1': {
                'bucket 1': [
                    {
                        'Grantee': {
                            'DisplayName': 'a name'
                        }
                    }
                ]
            }
        }

        self.assertEqual(results, expected)

    def test_get_bucket_versioning_by_region(self):
        list_buckets_fixture = {
            'us-east-1': [
                {
                    'Name': 'bucket 1',
                    'CreationDate': 'a datetime'
                },
            ]
        }

        client_mock_1 = MagicMock()
        client_mock_1.get_bucket_versioning.return_value = {
            'Status': 'Enabled',
            'MFADelete': 'Disabled'
        }

        clients = {
            'us-east-1': client_mock_1,
        }
        barrel = S3Barrel({}, clients=clients)
        barrel.cache['list_buckets'] = list_buckets_fixture

        results = barrel.tap('get_bucket_versioning')

        expected = {
            'us-east-1': {
                'bucket 1': {
                    'Status': 'Enabled',
                    'MFADelete': 'Disabled'
                }
            }
        }

        self.assertEqual(results, expected)
