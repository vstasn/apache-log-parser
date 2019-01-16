from django.test import TestCase
from apache_viewer.utils import parse_apache_string, format_date
from datetime import datetime


class UtilsTest(TestCase):
    def setUp(self):
        self.log_string = '93.185.192.80 - - [18/Feb/2016:13:33:49 +0100] "GET /administrator/ HTTP/1.1" 200 4263 "-" "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36" "-"'

    def test_utils_apache_parse_string(self):
        """test: convert from apache log to dict"""
        result = parse_apache_string(self.log_string)

        self.assertEqual(result["ip"], "93.185.192.80")
        self.assertEqual(result["request_method"], "GET")

    def test_utils_format_datetime(self):
        """test: function format_date should return correct datetime"""

        result = parse_apache_string(self.log_string)
        mock_date = datetime()
        self.assertIn("time", result)

        self.assertEqual(type(format_date(result["time"])), type(mock_date))
