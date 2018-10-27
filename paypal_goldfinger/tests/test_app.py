
import datetime
import dateutil
import unittest
from paypal_goldfinger.app import PaypalGoldfinger

class TestPaypalGoldfinger(unittest.TestCase):

    def setUp(self):
        self._g = PaypalGoldfinger()

    def test_placeholder(self):
        self.assertTrue(True)

    def test_nonce(self):
        self.assertTrue(self._g.nonce())

    def test_eval_min_datetime(self):
        test1 = datetime.datetime(
            year=2001,
            month=2,
            day=1,
            hour=1,
            minute=2,
            second=3
        )
        got1 = self._g.eval_min_datetime(test1,3)
        self.assertEqual(got1.year,2000)
        self.assertEqual(got1.month,11)
        self.assertEqual(got1.day,1)

    def test_get_utc_now(self):
        got1 = self._g.get_utc_now()
        self.assertIs(got1.tzinfo,None)

    def test_format_timestamp(self):
        test1 = datetime.datetime(
            year=2001,
            month=2,
            day=1,
            hour=1,
            minute=2,
            second=3
        )
        got1 = self._g.format_timestamp(test1)
        self.assertEqual(got1,'2001-02-01T01:02:03')

if __name__ == '__main__':
    unittest.main()
