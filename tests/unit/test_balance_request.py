# -*- coding: utf-8 -*-
import datetime
import unittest
import uuid

from yandex_checkout_payout.domain.request.balance_request import BalanceRequest


class TestBalanceRequest(unittest.TestCase):

    def test_request_cast(self):
        request = BalanceRequest()
        request.agent_id = 123456
        request.client_order_id = '215d8da0-000f-50be-b000-0003308c89be'
        request.request_dt = '2020-03-04T15:39:45.456+03:00'

        self.assertEqual({
            'agent_id': '123456',
            'client_order_id': '215d8da0-000f-50be-b000-0003308c89be',
            'request_dt': datetime.datetime(2020, 3, 4, 15, 39, 45, 456000,
                                            tzinfo=datetime.timezone(datetime.timedelta(seconds=10800))),
            'request_name': 'balanceRequest'
        }, dict(request))

    def test_request_setters(self):
        request = BalanceRequest({
            'agent_id': 123456,
            'client_order_id': '215d8da0-000f-50be-b000-0003308c89be',
            'request_dt': '2020-03-04T15:39:45.456+03:00'
        })

        self.assertIsInstance(request.agent_id, str)
        self.assertIsInstance(request.request_dt, datetime.datetime)
        self.assertEqual(request.request_name, 'balanceRequest')

        with self.assertRaises(TypeError):
            request.request_dt = 'invalid request_dt'

        # with self.assertRaises(TypeError):
        #     request.items = 'invalid items'
        #
        # with self.assertRaises(TypeError):
        #     request.settlements = 'invalid settlements'

