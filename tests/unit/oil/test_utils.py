import unittest
import arrow


from oil.utils import days_ago

class UtilsTestCase(unittest.TestCase):
    def test_can_find_difference_one_day_ago(self):
        days = days_ago(arrow.utcnow().shift(days=-1).isoformat())
        self.assertEqual(days, 1)

    def test_can_find_difference_60_days_ago(self):
        days = days_ago(arrow.utcnow().shift(days=-60).isoformat())
        self.assertEqual(days, 60)

    def test_can_find_difference_60_days_in_the_future(self):
        days = days_ago(arrow.utcnow().shift(days=60).isoformat())
        self.assertEqual(days, -60)


