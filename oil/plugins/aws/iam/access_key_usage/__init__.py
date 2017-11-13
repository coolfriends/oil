from oil.plugins import Plugin
from oil import utils


class AccessKeyUsagePlugin(Plugin):

    name = 'access_key_usage'
    provider = 'aws'
    service = 'iam'

    requirements = {
        'users': ['aws', 'iam', 'get_credential_report']
    }

    default_config = {
        'access_key_last_used_severity_two_threshold': {
            'name': 'Access Key Last Used Severity Two Threshold',
            'description': 'Threshold for a severity two finding',
            'value_description': 'Number of days since key last used',
            'default': 180,
        },
        'access_key_last_used_severity_one_threshold': {
            'name': 'Access Key Last Used Severity One Threshold',
            'description': 'Threshold for a severity one finding',
            'value_description': 'Number of days since key last used',
            'default': 90,
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
            # This is handled in a separate plugin
            if user['user'] == '<root_account>':
                continue

            active_key_1 = user.get('access_key_1_active', 'false')
            active_key_2 = user.get('access_key_2_active', 'false')
            if active_key_1 == 'true':
                self.results.append(self._check_last_used(user, '1'))
            if active_key_2 == 'true':
                self.results.append(self._check_last_used(user, '2'))
            if active_key_1 == 'false' and active_key_2 == 'false':
                severity = 0
                message = 'No active keys for {}'.format(
                    user['user'],
                )
                self.results.append({
                    'resource': user['arn'],
                    'region': 'aws-global',
                    'severity': severity,
                    'message': message
                })

        return self.results

    def _check_last_used(self, user, key_1_or_2):
        resource = user['arn']
        username = user['user']
        region = 'aws-global'

        sev_2_threshold = self.config.get(
            'access_key_last_used_severity_two_threshold'
        )
        sev_1_threshold = self.config.get(
            'access_key_last_used_severity_one_threshold'
        )

        last_used_key = 'access_key_{}_last_used_date'.format(key_1_or_2)
        last_used = user.get(last_used_key, 'N/A')

        if last_used == 'N/A':
            return {
                'resource': resource,
                'region': 'aws-global',
                'severity': 0,
                'message': 'Access key {} has never been used for {}'.format(
                    key_1_or_2,
                    username
                )
            }

        # Check sev 2
        days_ago = -(utils.days_ago(last_used))
        if days_ago > sev_2_threshold:
            return {
                'resource': resource,
                'region': 'aws-global',
                'severity': 2,
                'message': 'Access key {} last used {} days ago for {}'.format(
                    key_1_or_2,
                    days_ago,
                    username,
                )
            }

        if days_ago > sev_1_threshold:
            return {
                'resource': resource,
                'region': 'aws-global',
                'severity': 1,
                'message': 'Access key {} last used {} days ago for {}'.format(
                    key_1_or_2,
                    days_ago,
                    username,
                )
            }

        return {
            'resource': resource,
            'region': 'aws-global',
            'severity': 0,
            'message': 'Access key {} last used {} days ago for {}'.format(
                key_1_or_2,
                days_ago,
                username
            )
        }
