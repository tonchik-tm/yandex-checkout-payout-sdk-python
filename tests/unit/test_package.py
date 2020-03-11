# -*- coding: utf-8 -*-
import unittest
import uuid

from os.path import abspath

from yandex_checkout_payout.configuration import Configuration
from yandex_checkout_payout.domain.common.currency import Currency
from yandex_checkout_payout.domain.common.keychain import KeyChain
from yandex_checkout_payout.domain.request.make_deposition_request import MakeDepositionRequest
from yandex_checkout_payout.domain.request.synonym_card_request import SynonymCardRequest
from yandex_checkout_payout.domain.request.test_deposition_request import TestDepositionRequest
from yandex_checkout_payout.domain.response.balance_response import BalanceResponse
from yandex_checkout_payout.domain.response.deposition_response import DepositionResponse
from yandex_checkout_payout.domain.response.synonym_card_response import SynonymCardResponse
from yandex_checkout_payout.yandex_checkout_payout import YandexCheckoutPayout


class TestPackage(unittest.TestCase):

    def setUp(self):  # Set the keychain for all tests
        keychain = KeyChain(abspath('../files/250000.cer'), abspath('../files/privateKey.pem'), '12345')
        Configuration.configure(250000, keychain)

    def test_get_balance(self):
        client_order_id = str(uuid.uuid4())

        response = YandexCheckoutPayout.get_balance(client_order_id)

        self.assertIsInstance(response, BalanceResponse)
        self.assertEqual(response.client_order_id, client_order_id)

    def test_synonym_card_request(self):
        params = {
            "destination_card_number": "5555555555554444",
            "response_format": "json",
        }
        request = SynonymCardRequest(params)
        response = YandexCheckoutPayout.get_synonym_card(request)

        self.assertIsInstance(response, SynonymCardResponse)
        self.assertEqual(response.panmask, "555555******4444")

    def test_test_deposition_request(self):
        params = self.create_test_params()
        request = TestDepositionRequest(params)
        response = YandexCheckoutPayout.create_deposition(request)

        self.assertIsInstance(response, DepositionResponse)
        self.assertEqual(response.client_order_id, request.client_order_id)

    def test_make_deposition_request(self):
        params = self.create_make_params()
        request = MakeDepositionRequest(params)
        response = YandexCheckoutPayout.create_deposition(request)

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
        params = {
            "destination_card_number": "5555555555554444",
            "response_format": "json",
        }
        request = SynonymCardRequest(params)
        response = YandexCheckoutPayout.get_synonym_card(request)

        client_order_id = str(uuid.uuid4())

        return {
            "agent_id": 250000,
            "client_order_id": client_order_id,
            "dst_account": "41001614575714",
            "amount": 10.00,
            "currency": Currency.RUB,
            "contract": "Зачисление на карту",
            "payment_params": {
                "skr_destination_card_synonym": response.panmask,
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
