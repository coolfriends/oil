import unittest

from oil.plugins.aws.rds import PublicDBInstancesPlugin


class ExtraAccessKeyPluginTestCase(unittest.TestCase):

    def test_can_be_initialized_and_run_with_no_config(self):
        data_fixture = {
            'aws': {
                'rds': {
                    'aws-global': {
                        'describe_db_instances': []
                    }
                }
            }
        }

        plugin = PublicDBInstancesPlugin()
        results = plugin.run(data_fixture)
        results_keys = list(results[0].keys())
        expected = [
            'resource',
            'severity',
            'message',
            'region'
        ]

        self.assertCountEqual(results_keys, expected)

    def test_can_be_initialized_and_run_with_empty_config(self):
        data_fixture = {
            'aws': {
                'rds': {
                    'aws-global': {
                        'describe_db_instances': []
                    }
                }
            }
        }

        plugin = PublicDBInstancesPlugin()
        results = plugin.run(data_fixture)
        results_keys = list(results[0].keys())
        expected = [
            'resource',
            'severity',
            'message',
            'region'
        ]

        self.assertCountEqual(results_keys, expected)

    def test_creates_results_with_correct_fields_for_multiple_users(self):
        db_instance1_fixture = {
            'DBInstanceIdentifier': 'Any Identifier',
            'DBInstanceArn': 'Any Arn',
            'PubliclyAccessible': True,
        }
        db_instance2_fixture = {
            'DBInstanceIdentifier': 'An Identifier',
            'DBInstanceArn': 'An Arn',
            'PubliclyAccessible': False,
        }

        db_instances = [db_instance1_fixture, db_instance2_fixture]
        data_fixture = {
            'aws': {
                'rds': {
                    'aws-global': {
                        'describe_db_instances': db_instances
                    }
                }
            }
        }

        plugin = PublicDBInstancesPlugin()
        results = plugin.run(data_fixture)
        results_keys = list(results[0].keys())
        expected = [
            'resource',
            'severity',
            'message',
            'region'
        ]

        self.assertCountEqual(results_keys, expected)

    def test_no_db_instances(self):
        data_fixture = {
            'aws': {
                'rds': {
                    'aws-global': {
                        'describe_db_instances': []
                    }
                }
            }
        }

        plugin = PublicDBInstancesPlugin()
        results = plugin.run(data_fixture)
        expected = [{
            'resource': 'None',
            'region': 'aws-global',
            'severity': 0,
            'message': 'No DB instances found',
        }]

        self.assertEqual(results, expected)

    def test_public_db_instance(self):
        db_instance_fixture = {
            'DBInstanceIdentifier': 'Any Identifier',
            'DBInstanceArn': 'Any Arn',
            'PubliclyAccessible': True,
        }

        data_fixture = {
            'aws': {
                'rds': {
                    'aws-global': {
                        'describe_db_instances': [db_instance_fixture]
                    }
                }
            }
        }

        plugin = PublicDBInstancesPlugin()
        results = plugin.run(data_fixture)
        expected = [{
            'resource': db_instance_fixture['DBInstanceIdentifier'],
            'region': 'aws-global',
            'severity': 2,
            'message': 'The DB instance {db_id} is publicly accessible'.format(
                db_id=db_instance_fixture['DBInstanceIdentifier']
            ),
        }]

        self.assertEqual(results, expected)

    def test_non_public_db_instance(self):
        db_instance_fixture = {
            'DBInstanceIdentifier': 'Any Identifier',
            'DBInstanceArn': 'Any Arn',
            'PubliclyAccessible': False,
        }

        data_fixture = {
            'aws': {
                'rds': {
                    'aws-global': {
                        'describe_db_instances': [db_instance_fixture]
                    }
                }
            }
        }

        plugin = PublicDBInstancesPlugin()
        results = plugin.run(data_fixture)
        expected = [{
            'resource': db_instance_fixture['DBInstanceIdentifier'],
            'region': 'aws-global',
            'severity': 0,
            'message': 'The DB instance {db_id} is not publicly accessible'.format(
                db_id=db_instance_fixture['DBInstanceIdentifier']
            ),
        }]

        self.assertEqual(results, expected)

    def test_non_public_db_instance(self):
        db_instance_fixture = {
            'DBInstanceIdentifier': 'Any Identifier',
            'DBInstanceArn': 'Any Arn',
            'PubliclyAccessible': False,
        }

        data_fixture = {
            'aws': {
                'rds': {
                    'aws-global': {
                        'describe_db_instances': [db_instance_fixture]
                    }
                }
            }
        }

        plugin = PublicDBInstancesPlugin()
        results = plugin.run(data_fixture)
        expected = [{
            'resource': db_instance_fixture['DBInstanceIdentifier'],
            'region': 'aws-global',
            'severity': 0,
            'message': 'The DB instance {db_id} is not publicly accessible'.format(
                db_id=db_instance_fixture['DBInstanceIdentifier']
            ),
        }]

        self.assertEqual(results, expected)

    def test_configure_no_db_instances_severity(self):
        data_fixture = {
            'aws': {
                'rds': {
                    'aws-global': {
                        'describe_db_instances': []
                    }
                }
            }
        }

        config = {
            'no_db_instances_severity': 1
        }
        plugin = PublicDBInstancesPlugin(config)
        results = plugin.run(data_fixture)
        expected = [
            {
                'resource': 'None',
                'region': 'aws-global',
                'severity': 1,
                'message': 'No DB instances found'
            }
        ]

        self.assertEqual(results, expected)

    def test_configure_public_db_instances_severity(self):
        db_instance_fixture = {
            'DBInstanceIdentifier': 'Any Identifier',
            'DBInstanceArn': 'Any Arn',
            'PubliclyAccessible': True,
        }

        data_fixture = {
            'aws': {
                'rds': {
                    'aws-global': {
                        'describe_db_instances': [db_instance_fixture]
                    }
                }
            }
        }

        config = {
            'public_db_instance_severity': 1
        }
        plugin = PublicDBInstancesPlugin(config)
        results = plugin.run(data_fixture)
        expected = [
            {
                'resource': db_instance_fixture['DBInstanceIdentifier'],
                'region': 'aws-global',
                'severity': 1,
                'message': 'The DB instance {db_id} is publicly accessible'.format(
                        db_id=db_instance_fixture['DBInstanceIdentifier'],
                )
            }
        ]

        self.assertEqual(results, expected)

    def test_configure_non_public_db_instances_severity(self):
        db_instance_fixture = {
            'DBInstanceIdentifier': 'Any Identifier',
            'DBInstanceArn': 'Any Arn',
            'PubliclyAccessible': False,
        }

        data_fixture = {
            'aws': {
                'rds': {
                    'aws-global': {
                        'describe_db_instances': [db_instance_fixture]
                    }
                }
            }
        }

        config = {
            'non_public_db_instance_severity': 2
        }
        plugin = PublicDBInstancesPlugin(config)
        results = plugin.run(data_fixture)
        expected = [
            {
                'resource': db_instance_fixture['DBInstanceIdentifier'],
                'region': 'aws-global',
                'severity': 2,
                'message': 'The DB instance {db_id} is not publicly accessible'.format(
                        db_id=db_instance_fixture['DBInstanceIdentifier'],
                )
            }
        ]

        self.assertEqual(results, expected)

    def test_configure_no_db_instances_message(self):
        data_fixture = {
            'aws': {
                'rds': {
                    'aws-global': {
                        'describe_db_instances': []
                    }
                }
            }
        }

        config = {
            'no_db_instances_message': 'Overridden message'
        }
        plugin = PublicDBInstancesPlugin(config)
        results = plugin.run(data_fixture)
        expected = [
            {
                'resource': 'None',
                'region': 'aws-global',
                'severity': 0,
                'message': 'Overridden message',
            }
        ]

        self.assertEqual(results, expected)

    def test_configure_public_db_instances_message(self):
        db_instance_fixture = {
            'DBInstanceIdentifier': 'Any Identifier',
            'DBInstanceArn': 'Any Arn',
            'PubliclyAccessible': True,
        }

        data_fixture = {
            'aws': {
                'rds': {
                    'aws-global': {
                        'describe_db_instances': [db_instance_fixture]
                    }
                }
            }
        }

        config = {
            'public_db_instance_message': 'Overridden message for public DB instance {db_id}'
        }
        plugin = PublicDBInstancesPlugin(config)
        results = plugin.run(data_fixture)
        expected = [
            {
                'resource': db_instance_fixture['DBInstanceIdentifier'],
                'region': 'aws-global',
                'severity': 2,
                'message': 'Overridden message for public DB instance {db_id}'.format(
                        db_id=db_instance_fixture['DBInstanceIdentifier'],
                )
            }
        ]

        self.assertEqual(results, expected)

    def test_configure_non_public_db_instances_message(self):
        db_instance_fixture = {
            'DBInstanceIdentifier': 'Any Identifier',
            'DBInstanceArn': 'Any Arn',
            'PubliclyAccessible': False,
        }

        data_fixture = {
            'aws': {
                'rds': {
                    'aws-global': {
                        'describe_db_instances': [db_instance_fixture]
                    }
                }
            }
        }

        config = {
            'non_public_db_instance_message': 'Overridden message for non-public DB instance {db_id}'
        }
        plugin = PublicDBInstancesPlugin(config)
        results = plugin.run(data_fixture)
        expected = [
            {
                'resource': db_instance_fixture['DBInstanceIdentifier'],
                'region': 'aws-global',
                'severity': 0,
                'message': 'Overridden message for non-public DB instance {db_id}'.format(
                        db_id=db_instance_fixture['DBInstanceIdentifier'],
                )
            }
        ]

        self.assertEqual(results, expected)
