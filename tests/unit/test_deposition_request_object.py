# -*- coding: utf-8 -*-
import datetime
import unittest

from dateutil import tz, parser

from yandex_checkout_payout.domain.request.request_object import RequestObject


class TestTestDepositionRequest(unittest.TestCase):

    def test_request_cast(self):
        request = RequestObject()
        request.request_dt = '2020-03-04T15:39:45.456+03:00'

        self.assertEqual({
            'request_dt': datetime.datetime(2020, 3, 4, 15, 39, 45, 456000, tzinfo=tz.gettz('Europe/Moscow')),
            'request_name': 'baseRequest'
        }, dict(request))

    def test_request_setters(self):
        request = RequestObject()

        self.assertIsInstance(request.request_dt, datetime.datetime)
        self.assertEqual(request.request_name, 'baseRequest')

        with self.assertRaises(TypeError):
            request.request_dt = 'invalid request_dt'

    def test_request_map(self):
        request = RequestObject()
        self.assertEqual(request.map(), {
            "requestDT": request.request_dt.strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
        })
