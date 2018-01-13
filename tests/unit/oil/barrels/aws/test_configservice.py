import unittest
from unittest.mock import MagicMock
from oil.barrels.aws import ConfigServiceBarrel


class ConfigServiceBarrelCase(unittest.TestCase):

    def client_mock(self, fixture):
        client = MagicMock()
        client.describe_configuration_recorders.return_value = fixture
        client.describe_configuration_recorder_status.return_value = fixture
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
        barrel = ConfigServiceBarrel({}, clients={})
        self.assertEqual(supported_regions, barrel.supported_regions)

    def test_tap_functions_with_describe_configuration_recorders(self):
        fixture = {
            'ConfigurationRecorders': [
                {
                    'name': 'A Recorder',
                }
            ]
        }
        clients = {
            'us-east-1': self.client_mock(fixture)
        }
        barrel = ConfigServiceBarrel({}, clients=clients)
        tap_return = barrel.tap('describe_configuration_recorders')
        expected_return = barrel.describe_configuration_recorders()

        self.assertEqual(expected_return, tap_return)

    def test_tap_functions_with_describe_configuration_recorder_status(self):
        fixture = {
            'ConfigurationRecordersStatus': [
                {
                    'name': 'A Recorder',
                }
            ]
        }
        clients = {
            'us-east-1': self.client_mock(fixture)
        }
        barrel = ConfigServiceBarrel({}, clients=clients)
        tap_return = barrel.tap('describe_configuration_recorder_status')
        expected_return = barrel.describe_configuration_recorder_status()

        self.assertEqual(expected_return, tap_return)

    def test_tap_throws_error_with_unsupported_call(self):
        barrel = ConfigServiceBarrel({})

        with self.assertRaises(RuntimeError):
            barrel.tap('unsupported_call')

    def test_describe_configuration_recorders_lists_by_region(self):
        fixture_1 = [
            {
                'ConfigurationRecorders': [
                    {
                        'name': 'A Recorder',
                    }
                ]
            },
            {
                'ConfigurationRecorders': [
                    {
                        'name': 'A Recorder 2',
                    }
                ]
            }
        ]
        fixture_2 = [
            {
                'ConfigurationRecorders': [
                    {
                        'name': 'A Recorder 3',
                    }
                ]
            },
            {
                'ConfigurationRecorders': [
                    {
                        'name': 'A Recorder 4',
                    }
                ]
            }
        ]
        clients = {
            'us-east-1': self.client_mock(fixture_1),
            'us-east-2': self.client_mock(fixture_2),
        }
        barrel = ConfigServiceBarrel({}, clients=clients)

        results = barrel.describe_metric_filters()

        expected = {
            'us-east-1': [
                {
                    'name': 'A Recorder'
                },
                {
                    'name': 'A Recorder 2'
                },
            ],
            'us-east-2': [
                {
                    'name': 'A Recorder 3'
                },
                {
                    'name': 'A Recorder 4'
                },
            ]
        }

        self.assertEqual(results, expected)

    def test_describe_configuration_recorders_empty(self):
        fixture = [
            {
                'ConfigurationRecorders': []
            }
        ]
        clients = {
            'us-east-1': self.client_mock(fixture)
        }

        barrel = ConfigServiceBarrel({}, clients=clients)

        results = barrel.describe_configuration_recorders()

        expected = {
            'us-east-1': []
        }

        self.assertEqual(results, expected)

    def test_describe_configuration_recorder_status_lists_by_region(self):
        fixture_1 = [
            {
                'ConfigurationRecordersStatus': [
                    {
                        'name': 'A Recorder',
                    }
                ]
            },
            {
                'ConfigurationRecordersStatus': [
                    {
                        'name': 'A Recorder 2',
                    }
                ]
            }
        ]
        fixture_2 = [
            {
                'ConfigurationRecordersStatus': [
                    {
                        'name': 'A Recorder 3',
                    }
                ]
            },
            {
                'ConfigurationRecordersStatus': [
                    {
                        'name': 'A Recorder 4',
                    }
                ]
            }
        ]
        clients = {
            'us-east-1': self.client_mock(fixture_1),
            'us-east-2': self.client_mock(fixture_2),
        }
        barrel = ConfigServiceBarrel({}, clients=clients)

        results = barrel.describe_configuration_recorder_status()

        expected = {
            'us-east-1': [
                {
                    'name': 'A Recorder'
                },
                {
                    'name': 'A Recorder 2'
                },
            ],
            'us-east-2': [
                {
                    'name': 'A Recorder 3'
                },
                {
                    'name': 'A Recorder 4'
                },
            ]
        }

        self.assertEqual(results, expected)

    def test_describe_configuration_recorder_status_empty(self):
        fixture = [
            {
                'ConfigurationRecordersStatus': []
            }
        ]
        clients = {
            'us-east-1': self.client_mock(fixture)
        }

        barrel = ConfigServiceBarrel({}, clients=clients)

        results = barrel.describe_configuration_recorder_status()

        expected = {
            'us-east-1': []
        }

        self.assertEqual(results, expected)
