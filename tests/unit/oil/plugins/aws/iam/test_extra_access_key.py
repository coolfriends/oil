import unittest

from oil.plugins.aws.iam import ExtraAccessKeyPlugin


class ExtraAccessKeyPluginTestCase(unittest.TestCase):

    def test_can_be_initialized_and_run_with_no_config(self):
        data_fixture = {
            'aws': {
                'iam': {
                    'aws-global': {
                        'get_credential_report': [
                        ]
                    }
                }
            }
        }

        plugin = ExtraAccessKeyPlugin()
        results = plugin.run(data_fixture)
        results_keys = list(results[0].keys())
        expected = [
            'resource',
            'severity',
            'message',
            'region'
        ]

        self.assertCountEqual(results_keys, expected)
