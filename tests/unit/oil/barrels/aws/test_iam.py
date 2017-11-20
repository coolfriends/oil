import unittest
from unittest.mock import MagicMock, patch
from oil.barrels.aws import IAMBarrel


class IAMBarrelTestCase(unittest.TestCase):
    credential_report_content = (
        'user,arn,user_creation_time,password_enabled,password_last_used,passwo'
        'rd_last_changed,password_next_rotation,mfa_active,access_key_1_active,'
        'access_key_1_last_rotated,access_key_1_last_used_date,access_key_1_las'
        't_used_region,access_key_1_last_used_service,access_key_2_active,acces'
        's_key_2_last_rotated,access_key_2_last_used_date,access_key_2_last_use'
        'd_region,access_key_2_last_used_service,cert_1_active,cert_1_last_rota'
        'ted,cert_2_active,cert_2_last_rotated\n<root_account>,arn:aws:iam::fak'
        'earn:root,2017-06-10T02:35:07+00:00,not_supported,2017-10-22T08:11:09+'
        '00:00,not_supported,not_supported,true,false,N/A,N/A,N/A,N/A,false,N/A'
        ',N/A,N/A,N/A,false,N/A,false,N/A\nexample.user,arn:aws:iam::fakearn:us'
        'er/example.user,2017-06-10T02:43:37+00:00,true,2017-06-10T02:45:16+00:'
        '00,2017-06-10T02:45:50+00:00,N/A,false,true,2017-06-10T02:47:48+00:00,'
        'N/A,N/A,N/A,false,N/A,N/A,N/A,N/A,false,N/A,false,N/A\nfakeuser,arn:aw'
        's:iam::fakearn:user/fakeuser,2017-07-01T02:18:08+00:00,true,2017-07-01'
        'T02:21:06+00:00,2017-10-22T08:12:28+00:00,N/A,true,true,2017-10-22T08:'
        '12:39+00:00,2017-11-08T18:39:00+00:00,ap-southeast-1,ec2,false,N/A,N/A'
        ',N/A,N/A,false,N/A,false,N/A\nfinal.user,arn:aws:iam::fakearn:user/fin'
        'al.user,2017-06-10T02:42:36+00:00,true,2017-06-10T16:19:22+00:00,2017-'
        '06-10T16:19:07+00:00,N/A,false,true,2017-06-10T02:42:36+00:00,N/A,N/A,'
        'N/A,false,N/A,N/A,N/A,N/A,false,N/A,false,N/A'
    ).encode()

    def client_mock(self, fixture):
        client = MagicMock()
        paginator = MagicMock()
        response_iterator = fixture

        paginator.paginate.return_value = response_iterator
        client.get_paginator.return_value = paginator

        return client

    def test_has_correct_default_regions(self):
        default_regions = set([
            'aws-global'
        ])
        barrel = IAMBarrel({})
        self.assertEqual(default_regions, barrel._default_regions)

    @patch("boto3.client")
    def test_default_clients(self, mock_client):
        mock_client.return_value = MagicMock()
        barrel = IAMBarrel({})

        for region, client in barrel.clients.items():
            self.assertIn(region, barrel._default_regions)

    def test_tap_functions_with_get_credential_report(self):
        client = MagicMock()
        client.generate_credential_report.return_value = {
            'State': 'COMPLETE'
        }
        client.get_credential_report.return_value = {
            'Content': self.credential_report_content
        }
        clients = {
            'aws-global': client
        }
        barrel = IAMBarrel({}, clients=clients)
        tap_return = barrel.tap('get_credential_report')
        get_credential_report_return = barrel.get_credential_report()

        self.assertEqual(get_credential_report_return, tap_return)

    def test_tap_throws_error_with_unsupported_call(self):
        barrel = IAMBarrel({})

        with self.assertRaises(RuntimeError):
            barrel.tap('unsupported_call')
