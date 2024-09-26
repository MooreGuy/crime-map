import unittest
import slopd_log_parse
from main import Scraper
from unittest.mock import Mock, MagicMock


class TestParseSLOPDLogs(unittest.TestCase):
    def setUp(self):
        self.scraper = Scraper()
        self.scraper.fetch_log = lambda: raise_(
            Exception("Should not call this function!"
                      " Do not want to load a public service unnecessarily"))

        with open('sample_slopd_log_1.txt', 'r') as sample_file:
            sample_log = sample_file.read()
            self.scraper.raw_log = sample_log
            self.scraper.parse_logs()

    def test_parse_log_address(self):
        sample_file = open('sample_slopd_log.txt', 'r')
        sample_log = sample_file.read()
        parsed = slopd_log_parse.parse_log(sample_log)
        for entry in parsed:
            self.assertIn('address', entry)
        sample_file.close()

    def test_parse_date_and_time(self):
        entry = self.scraper.pulled_log[0]
        self.assertIn("timestamp", entry)

    def test_scraper(self):
        self.assertIsNotNone(self.scraper.pulled_log)
        self.assertGreater(len(self.scraper.pulled_log), 0)

    def test_send_logs(self):
        attrs = {
            'find_one.return_value': None,
            'insert_one.return_value': type('obj', (object,), {'inserted_id': 1})
        }
        self.scraper.logs = Mock(**attrs)
        self.scraper.send_log_to_kafka = MagicMock()

        total, inserted = self.scraper.send_out_logs()

        self.assertEqual(total, inserted)
        self.assertEqual(total, len(self.scraper.pulled_log))
        self.assertGreater(total, 0)

        self.scraper.logs.find_one.assert_called()
        self.scraper.logs.insert_one.assert_called()
        self.scraper.send_log_to_kafka.assert_called()
