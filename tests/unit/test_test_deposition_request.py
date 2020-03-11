# -*- coding: utf-8 -*-
import datetime
import unittest
import uuid
from os.path import abspath

import var_dump

from yandex_checkout_payout.configuration import Configuration
from yandex_checkout_payout.domain.common.currency import Currency
from yandex_checkout_payout.domain.common.error_converter import ErrorConverter
from yandex_checkout_payout.domain.common.keychain import KeyChain
from yandex_checkout_payout.domain.request.make_deposition_request import MakeDepositionRequest
from yandex_checkout_payout.domain.request.test_deposition_request import TestDepositionRequest
from yandex_checkout_payout.domain.response.deposition_response import DepositionResponse
from yandex_checkout_payout.yandex_checkout_payout import YandexCheckoutPayout


class TestTestDepositionRequest(unittest.TestCase):

    def setUp(self):  # Set the keychain for all tests
        keychain = KeyChain(abspath('../files/250000.cer'), abspath('../files/privateKey.pem'), '12345')
        Configuration.configure(250000, keychain)

    def test_request_cast(self):
        request = TestDepositionRequest()
        request.agent_id = 250000
        request.client_order_id = '215d8da0-000f-50be-b000-0003308c89be'
        request.request_dt = '2020-03-04T15:39:45.456+03:00'

        self.assertEqual({
            'agent_id': '250000',
            'client_order_id': '215d8da0-000f-50be-b000-0003308c89be',
            'request_dt': datetime.datetime(2020, 3, 4, 15, 39, 45, 456000,
                                            tzinfo=datetime.timezone(datetime.timedelta(seconds=10800))),
            'request_name': 'testDeposition'
        }, dict(request))

    def test_request_setters(self):
        request = TestDepositionRequest({
            'agent_id': 250000,
            'client_order_id': '215d8da0-000f-50be-b000-0003308c89be',
            'request_dt': '2020-03-04T15:39:45.456+03:00'
        })

        self.assertIsInstance(request.agent_id, str)
        self.assertIsInstance(request.request_dt, datetime.datetime)
        self.assertEqual(request.request_name, 'testDeposition')

        with self.assertRaises(TypeError):
            request.request_dt = 'invalid request_dt'

        # with self.assertRaises(TypeError):
        #     request.items = 'invalid items'
        #
        # with self.assertRaises(TypeError):
        #     request.settlements = 'invalid settlements'

    def test_request_validate(self):
        pass

    def test_deposition_dict(self):
        params = self.create_test_params()
        request = {'testDeposition': params}
        # var_dump.var_dump(request)
        response = YandexCheckoutPayout.create_deposition(request)
        # var_dump.var_dump(response)
        if response.status != 0:
            var_dump.var_dump(ErrorConverter.get_error_message(response.error))
        self.assertIsInstance(response, DepositionResponse)
        self.assertEqual(response.client_order_id, params['client_order_id'])

    def test_deposition_request(self):
        params = self.create_test_params()
        request = TestDepositionRequest(params)
        # var_dump.var_dump(request)
        response = YandexCheckoutPayout.create_deposition(request)
        # var_dump.var_dump(response)
        if response.status != 0:
            var_dump.var_dump(ErrorConverter.get_error_message(response.error))
        self.assertIsInstance(response, DepositionResponse)
        self.assertEqual(response.client_order_id, request.client_order_id)

    def test_make_deposition_request(self):
        params = self.create_make_params()
        request = MakeDepositionRequest(params)
        # var_dump.var_dump(request)
        response = YandexCheckoutPayout.create_deposition(request)
        # var_dump.var_dump(response)
        if response.status != 0:
            var_dump.var_dump(ErrorConverter.get_error_message(response.error))
        self.assertIsInstance(response, DepositionResponse)
        self.assertEqual(response.client_order_id, request.client_order_id)

    @staticmethod
    def create_test_params():
        client_order_id = str(uuid.uuid4())
        return {
            "agent_id": 250000,
            "client_order_id": client_order_id,
            "dst_account": "41001614575714",
            "amount": 10.00,
            "currency": Currency.RUB,
            "contract": "Зачисление на кошелек",
        }

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
