import unittest
from unittest.mock import MagicMock
from oil.barrels.aws import SQSBarrel


class SQSBarrelTestCase(unittest.TestCase):

    def test_has_correct_supported_regions(self):
        """
        Reference:
        https://docs.aws.amazon.com/general/latest/gr/rande.html#sqs_region
        """
        supported_regions = set([
            'us-east-2',
            'us-east-1',
            'us-west-1',
            'us-west-2',
            'ap-south-1',
            'ap-northeast-2',
            'ap-southeast-1',
            'ap-southeast-2',
            'ap-northeast-1',
            'ca-central-1',
            'eu-west-1',
            'eu-west-2',
            'eu-west-3',
            'sa-east-1'
        ])
        barrel = SQSBarrel({}, clients={})
        self.assertEqual(supported_regions, barrel.supported_regions)

    def test_list_queues_by_region(self):
        fixture_1 = {
            'QueueUrls': [
                'url 1',
                'url 2',
                'url 3',
            ]
        }

        fixture_2 = {
            'QueueUrls': [
                'url 4',
                'url 5',
                'url 6',
            ]
        }
        client_mock_1 = MagicMock()
        client_mock_1.list_queues.return_value = fixture_1
        client_mock_2 = MagicMock()
        client_mock_2.list_queues.return_value = fixture_2

        clients = {
            'us-east-1': client_mock_1,
            'us-east-2': client_mock_2
        }
        barrel = SQSBarrel({}, clients=clients)

        results = barrel.tap('list_queues')

        expected = {
            'us-east-1': [
                'url 1',
                'url 2',
                'url 3',
            ],
            'us-east-2': [
                'url 4',
                'url 5',
                'url 6',
            ],
        }

        self.assertEqual(results, expected)

    def test_get_queue_attributes_by_region(self):
        list_queues_fixture = {
            'us-east-1': [
                'url 1',
            ]
        }

        client = MagicMock()
        client.get_queue_attributes.return_value = {
            'Attributes': {
                'Attribute1': 'A value'
            }
        }

        clients = {
            'us-east-1': client,
        }
        barrel = SQSBarrel({}, clients=clients)
        barrel.cache['list_queues'] = list_queues_fixture

        results = barrel.tap('get_queue_attributes')

        expected = {
            'us-east-1': {
                'url 1': {
                    'Attribute1': 'A value',
                },
            }
        }

        self.assertEqual(results, expected)
