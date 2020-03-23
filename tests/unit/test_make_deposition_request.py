# -*- coding: utf-8 -*-
import datetime
import unittest
import uuid

from dateutil import tz

from yandex_checkout_payout.domain.common.currency import Currency
from yandex_checkout_payout.domain.models.recipients.recipient import Recipient
from yandex_checkout_payout.domain.request.make_deposition_request import MakeDepositionRequest


class TestMakeDepositionRequest(unittest.TestCase):

    def test_request_cast(self):
        request = MakeDepositionRequest()
        request.agent_id = 250000
        request.client_order_id = '215d8da0-000f-50be-b000-0003308c89be'
        request.request_dt = '2020-03-04T15:39:45.456+03:00'

        rec = Recipient()
        rec.pof_offer_accepted = True
        request.payment_params = rec

        self.assertEqual({
            'agent_id': 250000,
            'client_order_id': '215d8da0-000f-50be-b000-0003308c89be',
            'request_dt': datetime.datetime(2020, 3, 4, 15, 39, 45, 456000, tzinfo=tz.gettz('Europe/Moscow')),
            'request_name': 'makeDeposition',
            'payment_params': {'pof_offer_accepted': True},
        }, dict(request))

    def test_request_setters(self):
        request = MakeDepositionRequest(self.create_make_params())

        self.assertIsInstance(request.agent_id, int)
        self.assertIsInstance(request.request_dt, datetime.datetime)
        self.assertEqual(request.request_name, 'makeDeposition')
        self.assertIsInstance(request.payment_params, Recipient)
        self.assertIsInstance(request.payment_params.pof_offer_accepted, bool)

        with self.assertRaises(TypeError):
            request.request_dt = 'invalid request_dt'

        with self.assertRaises(TypeError):
            request.payment_params = 'invalid payment_params'

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

    @staticmethod
    def create_make_params():
        client_order_id = str(uuid.uuid4())
        return {
            "agent_id": 250000,
            "client_order_id": client_order_id,
            "dst_account": "41001614575714",
            "amount": 10.00,
            "currency": Currency.RUB,
            "contract": "Зачисление на кошелек",
            "payment_params": {
                "skr_destination_card_synonym": "h4h8FWCnhpiGKrg5eRKQ6hQS.SC.000.202003",
                "pof_offer_accepted": True,
                "sms_phone_number": "79818932328",
                "pdr_first_name": "Эдуард",
                "pdr_last_name": "Запеканкин",
                "pdr_doc_number": "1013123456",
                "pdr_doc_issue_date": "2013-10-10",
                "pdr_country": Currency.RUB,
                "pdr_birth_date": "1973-10-31"
            }
        }
