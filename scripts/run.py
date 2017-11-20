import sys
import os
import json
import csv
import argparse


try:
    from oil import Oil
except ImportError: # If module not installed with pip
    oil_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, oil_path)
    from oil import Oil

from oil.barrels.aws import CloudFrontBarrel
from oil.plugins.aws.cloudfront import TLSProtocolPlugin


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run a basic oil scan."
    )
    choices = ['json', 'csv']
    parser.add_argument('--output',
                        help='set output as json or csv',
                        choices=choices,
                        default='json')
    return parser.parse_args()

def generate_flattened_dict(scan_data):
    for provider, services in scan_data.items():
        for service, calls in services.items():
            for call, results in calls.items():
                for result in results:
                    row = {
                        'provider': provider,
                        'service': service,
                        'title': call,
                        'region': result['region'],
                        'resource': result['resource'],
                        'severity': result['severity'],
                        'message': result['message']
                    }
                    yield row

def print_as_csv(scan_data):
    fields = (
        'provider',
        'service',
        'title',
        'region',
        'resource',
        'severity',
        'message'
    )

    writer = csv.DictWriter(sys.stdout, fieldnames=fields)
    writer.writeheader()
    for row in generate_flattened_dict(scan_data):
        writer.writerow(row)

def main():
    args = parse_args()

    oil = Oil()
    """ Use sts credentials
    oil.register_barrel(CloudFrontBarrel, config={
            'aws_access_key_id': 'my_access_key',
            'aws_secret_access_key': 'my_secret_access_key',
            'aws_session_token': 'my-session-token'
        }
    )
    """
    oil.register_barrel(CloudFrontBarrel)
    oil.register_plugin(TLSProtocolPlugin)
    data = oil.scan()
    if args.output == 'csv':
        print_as_csv(data)
    elif args.output == 'json':
        print(json.dumps(data, indent=2))
    else:
        print('Unsupported output format.')

if __name__ == "__main__":
    main()
