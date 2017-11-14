from oil.plugins import Plugin
from oil import utils


class UserPasswordRotationPlugin(Plugin):

    name = 'user_password_rotation'
    provider = 'aws'
    service = 'iam'

    requirements = {
        'users': ['aws', 'iam', 'get_credential_report']
    }

    default_config = {
        'password_rotation_severity_2_threshold': {
            'name': 'Threshold for Password Rotation Severity 2',
            'description': 'Threshold for password age in days for severity 2',
            'value_description': 'number of days',
            'default': 365,
        },
        'password_rotation_severity_1_threshold': {
            'name': 'Threshold for Password Rotation Severity 1',
            'description': 'Threshold for password age in days for severity 1',
            'value_description': 'number of days',
            'default': 180,
        },
        'password_rotation_severity_2_message': {
            'name': 'Password Rotation Message for Severity 2 Finding',
            'description': 'The message displayed for a severity 2 finding',
            'value_description': '{username} {days}',
            'default': '{username} has not rotated their password in {days} days',
        },
        'password_rotation_severity_1_message': {
            'name': 'Password Rotation Message for Severity 1 Finding',
            'description': 'The message displayed for a severity 1 finding',
            'value_description': '{username} {days}',
            'default': '{username} has not rotated their password in {days} days',
        },
        'password_rotation_severity_0_message': {
            'name': 'Password Rotation Message for Severity 0 Finding',
            'description': 'The message displayed for a severity 0 finding',
            'value_description': '{username} {days}',
            'default': '{username} has not rotated their password in {days} days',
        },
        'no_password_message': {
            'name': 'No Password Message',
            'description': 'Message displayed when the user has no password',
            'value_description': '{username}',
            'default': '{username} does not have an AWS console password',
        },
    }

    def run(self, api_data):
        # Reset the results list for this plugin
        self.results = []

        requirements = self.collect_requirements(api_data)
        users = requirements['users']['aws-global']

        if not users:
            self.results.append({
                'resource': 'None',
                'region': 'aws-global',
                'severity': 0,
                'message': 'No users found'
            })

        for user in users:
            # Skip root account
            if user['user'] == '<root_account>':
                continue

            username = user['user']
            resource_arn = user['arn']
            password_last_changed = user.get(
                'password_last_changed',
                'N/A'
            )

            if password_last_changed == 'N/A':
                severity = 0
                message = self.config['no_password_message'].format(
                    username=username,
                )
            else:
                severity_key = 'password_rotation_severity_{}_threshold'
                message_key = 'password_rotation_severity_{}_message'

                days_elapsed = -(utils.days_ago(password_last_changed))
                if days_elapsed > self.config[severity_key.format('2')]:
                    severity = 2
                    message = self.config[message_key.format('2')].format(
                        username=username,
                        days=days_elapsed,
                    )
                elif days_elapsed > self.config[severity_key.format('1')]:
                    severity = 1
                    message = self.config[message_key.format('1')].format(
                        username=username,
                        days=days_elapsed,
                    )
                else:
                    severity = 0
                    message = self.config[message_key.format('0')].format(
                        username=username,
                        days=days_elapsed,
                    )

            self.results.append({
                'resource': resource_arn,
                'region': 'aws-global',
                'severity': severity,
                'message': message
            })

        return self.results
