import unittest

from oil.barrels.barrel import Barrel


class BarrelTestCase(unittest.TestCase):

    def test_regions_can_be_configured(self):
        my_regions = [
            'my-region-1',
            'my-region-2'
        ]
        mock_oil = {}
        mock_clients = {}
        barrel = Barrel(mock_oil, regions=my_regions, clients=mock_clients)
        self.assertEqual(barrel.regions, my_regions)
