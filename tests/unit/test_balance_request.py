# -*- coding: utf-8 -*-
import datetime
import unittest
from dateutil import tz, parser

from yandex_checkout_payout.domain.models.recipients.recipient import Recipient
from yandex_checkout_payout.domain.request.balance_request import BalanceRequest
from yandex_checkout_payout.domain.request.make_deposition_request import MakeDepositionRequest


class TestBalanceRequest(unittest.TestCase):

    def test_request_cast(self):
        request = BalanceRequest()
        request.agent_id = 123456
        request.client_order_id = '215d8da0-000f-50be-b000-0003308c89be'
        request.request_dt = '2020-03-04T15:39:45.456+03:00'

        self.assertEqual({
            'agent_id': 123456,
            'client_order_id': '215d8da0-000f-50be-b000-0003308c89be',
            'request_dt': datetime.datetime(2020, 3, 4, 15, 39, 45, 456000, tzinfo=tz.gettz('Europe/Moscow')),
            'request_name': 'balanceRequest'
        }, dict(request))

    def test_request_setters(self):
        request = BalanceRequest({
            'agent_id': 123456,
            'client_order_id': '215d8da0-000f-50be-b000-0003308c89be',
            'request_dt': '2020-03-04T15:39:45.456+03:00'
        })

        self.assertIsInstance(request.agent_id, int)
        self.assertIsInstance(request.client_order_id, str)
        self.assertIsInstance(request.request_dt, datetime.datetime)
        self.assertEqual(request.request_name, 'balanceRequest')

        with self.assertRaises(TypeError):
            request.request_dt = 'invalid request_dt'

    def test_request_validate(self):
        request = MakeDepositionRequest()

        with self.assertRaises(ValueError):
            request.validate()

        request.agent_id = 250000
        with self.assertRaises(ValueError):
            request.validate()

        request.agent_id = 0
        request.client_order_id = '215d8da0-000f-50be-b000-0003308c89be'
        with self.assertRaises(ValueError):
            request.validate()

        request.agent_id = 250000
        request.client_order_id = ''
        with self.assertRaises(ValueError):
            request.validate()

        request.client_order_id = '215d8da0-000f-50be-b000-0003308c89be'

        with self.assertRaises(ValueError):
            request.payment_params = {'invalid': 1}

        with self.assertRaises(ValueError):
            request.validate()

        request = MakeDepositionRequest()
        request.payment_params = Recipient({'pof_offer_accepted': True})
        with self.assertRaises(ValueError):
            request.validate()

        request = MakeDepositionRequest()
        request.payment_params = Recipient({'pof_offer_accepted': True})
        request.client_order_id = '215d8da0-000f-50be-b000-0003308c89be'
        with self.assertRaises(ValueError):
            request.validate()

        request = MakeDepositionRequest()
        request.payment_params = Recipient({'pof_offer_accepted': True})
        request.agent_id = 250000
        with self.assertRaises(ValueError):
            request.validate()
