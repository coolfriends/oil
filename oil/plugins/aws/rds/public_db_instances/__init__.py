from oil.plugins import Plugin


class PublicDBInstancesPlugin(Plugin):

    name = 'public_db_instances'
    provider = 'aws'
    service = 'rds'

    requirements = {
        'db_instances': ['aws', 'rds', 'describe_db_instances']
    }

    default_config = {
        'public_db_instance_severity': {
            'name': 'Public DB Instance Severity',
            'description': 'Adjust severity level for public DB instances',
            'value_description': '0 1 2',
            'default': 2,
        },
        'non_public_db_instance_severity': {
            'name': 'Non-Public DB Instance Severity',
            'description': 'Adjust severity level for non-public DB instances',
            'value_description': '0 1 2',
            'default': 0,
        },
        'no_db_instances_severity': {
            'name': 'No DB Instance Severity',
            'description': 'Adjust severity level for no DB instances',
            'value_description': '0 1 2',
            'default': 0,
        },
        'public_db_instance_message': {
            'name': 'Public DB Instance Severity',
            'description': 'Adjust message for public DB instances',
            'value_description': '{db_id}',
            'default': 'The DB instance {db_id} is publicly accessible',
        },
        'non_public_db_instance_message': {
            'name': 'Non-Public DB Instance Message',
            'description': 'Adjust message level for non-public DB instances',
            'value_description': '{db_id}',
            'default': 'The DB instance {db_id} is not publicly accessible',
        },
        'no_db_instances_message': {
            'name': 'No DB Instance Message',
            'description': 'Adjust message level for no DB instances',
            'value_description': 'string',
            'default': 'No DB instances found',
        },
    }

    def run(self, api_data):
        # Reset the results list for this plugin
        self.results = []

        requirements = self.collect_requirements(api_data)
        db_instances_by_region = requirements['db_instances']
        for region, db_instances in db_instances_by_region.items():
            if not db_instances:
                self.results.append({
                    'resource': 'None',
                    'region': region,
                    'severity': self.config['no_db_instances_severity'],
                    'message': self.config['no_db_instances_message'],
                })

            for db_instance in db_instances:
                db_instance_identifier = db_instance['DBInstanceIdentifier']
                db_instance_arn = db_instance['DBInstanceArn']

                publicly_accessible = db_instance['PubliclyAccessible']
                if publicly_accessible:
                    severity = self.config['public_db_instance_severity']
                    message = self.config['public_db_instance_message'].format(
                        db_id=db_instance_identifier,
                    )

                else:
                    severity = self.config['non_public_db_instance_severity']
                    message = self.config['non_public_db_instance_message'].format(
                        db_id=db_instance_identifier,
                    )

                self.results.append({
                    'resource': db_instance_identifier,
                    'region': region,
                    'severity': severity,
                    'message': message,
                })

        return self.results
