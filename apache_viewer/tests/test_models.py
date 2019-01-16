from django.core.exceptions import ValidationError
from django.test import TestCase
from apache_viewer.models import Logs
from django.utils import timezone


class ApacheLogModelTest(TestCase):
    """test log model"""

    def test_log_with_empty_fields(self):
        """test: should raise"""
        with self.assertRaises(ValidationError):
            Logs().full_clean()

    def test_log_with_valid_data(self):
        """test: exists default schedule"""
        log_ = Logs.objects.create(
            ip="1.1.1.1", tms=timezone.now(), request_code=200, request_size=3000
        )
        f_log = Logs.objects.first()

        self.assertEqual(log_.pk, f_log.pk)

    def test_log_with_invalid_ip(self):
        """test: trying to set invalid ip"""
        log_ = Logs.objects.create(
            ip="fdsfsfs", tms=timezone.now(), request_code=200, request_size=3000
        )
        # should raise
        with self.assertRaises(ValidationError):
            log_.full_clean()
