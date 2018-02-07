import unittest
from unittest.mock import MagicMock
from oil.barrels.aws import SNSBarrel


class SNSBarrelTestCase(unittest.TestCase):

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
        https://docs.aws.amazon.com/general/latest/gr/rande.html#sns_region
        """
        supported_regions = set([
            'us-east-2',
            'us-east-1',
            'us-west-1',
            'us-west-2',
            'ca-central-1',
            'ap-south-1',
            'ap-northeast-2',
            'ap-southeast-2',
            'ap-northeast-1',
            'eu-central-1',
            'eu-west-1',
            'eu-west-3',
        ])
        barrel = SNSBarrel({}, clients={})
        self.assertEqual(supported_regions, barrel.supported_regions)

    def test_list_topics_by_region(self):
        fixture_1 = [
            {
                'Topics': [
                    {
                        'TopicArn': 'arn 1'
                    },
                    {
                        'TopicArn': 'arn 2'
                    },
                ]
            },
            {
                'Topics': [
                    {
                        'TopicArn': 'arn 3'
                    },
                    {
                        'TopicArn': 'arn 4'
                    },
                ]
            },
        ]

        fixture_2 = [
            {
                'Topics': [
                    {
                        'TopicArn': 'arn 5'
                    },
                    {
                        'TopicArn': 'arn 6'
                    },
                ]
            },
            {
                'Topics': [
                    {
                        'TopicArn': 'arn 7'
                    },
                    {
                        'TopicArn': 'arn 8'
                    },
                ]
            },
        ]
        clients = {
            'us-east-1': self.client_mock(fixture_1),
            'us-east-2': self.client_mock(fixture_2),
        }
        barrel = SNSBarrel({}, clients=clients)

        results = barrel.tap('list_topics')

        expected = {
            'us-east-1': [
                {
                    'TopicArn': 'arn 1'
                },
                {
                    'TopicArn': 'arn 2'
                },
                {
                    'TopicArn': 'arn 3'
                },
                {
                    'TopicArn': 'arn 4'
                },
            ],
            'us-east-2': [
                {
                    'TopicArn': 'arn 5'
                },
                {
                    'TopicArn': 'arn 6'
                },
                {
                    'TopicArn': 'arn 7'
                },
                {
                    'TopicArn': 'arn 8'
                },
            ],
        }

        self.assertEqual(results, expected)

    def test_get_topic_attributes_by_region(self):
        list_topics_fixture = {
            'us-east-1': [
                {
                    'TopicArn': 'arn 1'
                }
            ]
        }

        client = MagicMock()
        client.get_topic_attributes.return_value = {
            'Attributes': {
                'TopicArn': 'arn 1',
                'Owner': '123123123'
            }
        }

        clients = {
            'us-east-1': client,
        }
        barrel = SNSBarrel({}, clients=clients)
        barrel.cache['list_topics'] = list_topics_fixture

        results = barrel.get_topic_attributes()

        expected = {
            'us-east-1': {
                'arn 1': {
                    'TopicArn': 'arn 1',
                    'Owner': '123123123'
                },
            }
        }

        self.assertEqual(results, expected)
