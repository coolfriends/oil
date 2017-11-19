import unittest
import os

from oil import Oil
from oil.plugins.aws.rds import PublicDBInstancesPlugin
from oil.barrels.aws import RDSBarrel


@unittest.skipIf(os.environ.get('OIL_FUNCTIONAL_TESTS', 'False') != 'True', "Skipping functional tests")
class RDSTestCase(unittest.TestCase):
    def test_oil_can_scan_for_rds_public_db_instances(self):
        oil = Oil()
        oil.register_barrel(RDSBarrel)
        oil.register_plugin(PublicDBInstancesPlugin)
        results = oil.scan()

        aws_results = results.get('aws', {})
        rds_results = aws_results.get('rds', {})
        plugin_results = rds_results.get('public_db_instances', [])

        self.assertNotEqual(plugin_results, [])
