response_iterator_fixture = [
    {
        "DistributionList": {
            "Items": [
                {
                    "ARN": "some arn",
                    "ViewerCertificate": {
                        "MinimumProtocolVersion": 'example value'
                    }
                },
                {
                    "ARN": "another arn",
                    "ViewerCertificate": {
                        "MinimumProtocolVersion": 'test value'
                    }
                }
            ]
        }
    },
    {
        "DistributionList": {
            "Items": [
                {
                    "ARN": "test arn",
                    "ViewerCertificate": {
                        "MinimumProtocolVersion": 'some value'
                    }
                },
                {
                    "ARN": "example arn",
                    "ViewerCertificate": {
                        "MinimumProtocolVersion": 'another value'
                    }
                }
            ]
        }
    }
]
