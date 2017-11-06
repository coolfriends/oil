# http://boto3.readthedocs.io/en/latest/reference/services/ec2.html#EC2.Client.describe_instances
# This makes sure there are multiple reservations per simulated page, and
# multiple instances in each reservation, and multiple pages.
boto3_describe_instances_paginator_one_field = [
    {
        'Reservations': [
            {
                'Instances': [
                    {
                        'InstanceId': 'instance1'
                    },
                    {
                        'InstanceId': 'instance2'
                    }
                ]
            },
            {
                'Instances': [
                    {
                        'InstanceId': 'instance3'
                    },
                    {
                        'InstanceId': 'instance4'
                    }
                ]
            }
        ]
    },
    {
        'Reservations': [
            {
                'Instances': [
                    {
                        'InstanceId': 'instance5'
                    },
                    {
                        'InstanceId': 'instance6'
                    }
                ]
            },
            {
                'Instances': [
                    {
                        'InstanceId': 'instance7'
                    },
                    {
                        'InstanceId': 'instance8'
                    }
                ]
            }
        ]
    },
]
