# -*- coding: utf-8 -*-
import unittest

from os.path import abspath

import var_dump

from yandex_checkout_payout.configuration import Configuration
from yandex_checkout_payout.domain.common.keychain import KeyChain
from yandex_checkout_payout.domain.request.synonym_card_request import SynonymCardRequest
from yandex_checkout_payout.domain.response.synonym_card_response import SynonymCardResponse
from yandex_checkout_payout.yandex_checkout_payout import YandexCheckoutPayout


class TestSynonymCardRequest(unittest.TestCase):

    def setUp(self):  # Set the keychain for all tests
        keychain = KeyChain(abspath('../files/250000.cer'), abspath('../files/privateKey.pem'), '12345')
        Configuration.configure(250000, keychain)

    def test_synonym_card_request(self):
        params = self.create_params()
        request = SynonymCardRequest(params)
        # var_dump.var_dump(request)
        response = YandexCheckoutPayout.get_synonym_card(request)
        # var_dump.var_dump(response)

        self.assertIsInstance(response, SynonymCardResponse)
        self.assertEqual(response.panmask, "555555******4444")

    @staticmethod
    def create_params():
        return {
            "destination_card_number": "5555555555554444",
            "response_format": "json",
        }

