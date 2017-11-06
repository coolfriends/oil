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

instances_only_one_field = [
    {
        'InstanceId': 'instance1'
    },
    {
        'InstanceId': 'instance2'
    },
    {
        'InstanceId': 'instance3'
    },
    {
        'InstanceId': 'instance4'
    },
    {
        'InstanceId': 'instance5'
    },
    {
        'InstanceId': 'instance6'
    },
    {
        'InstanceId': 'instance7'
    },
    {
        'InstanceId': 'instance8'
    },
]

describe_instances_paginator_with_name_tags = [
    {
        'Reservations': [
            {
                'Instances': [
                    {
                        'InstanceId': 'instance1',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'Instance 1',
                            }
                        ]
                    },
                    {
                        'InstanceId': 'instance2',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'Instance 2',
                            }
                        ]
                    }
                ]
            },
            {
                'Instances': [
                    {
                        'InstanceId': 'instance3',

                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'Instance 3',
                            }
                        ]
                    },
                    {
                        'InstanceId': 'instance4',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'Instance 4',
                            }
                        ]
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
                        'InstanceId': 'instance5',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'Instance 5',
                            }
                        ]

                    },
                    {
                        'InstanceId': 'instance6',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'Instance 6',
                            }
                        ]
                    }
                ]
            },
            {
                'Instances': [
                    {
                        'InstanceId': 'instance7',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'Instance 7',
                            }
                        ]
                    },
                    {
                        'InstanceId': 'instance8',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'Instance 8',
                            }
                        ]
                    }
                ]
            }
        ]
    },
]
