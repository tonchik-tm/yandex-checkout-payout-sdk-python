# -*- coding: utf-8 -*-
import unittest
import uuid

from os.path import abspath

from var_dump import var_dump

from yandex_checkout_payout.configuration import Configuration
from yandex_checkout_payout.domain.common.currency import Currency
from yandex_checkout_payout.domain.common.keychain import KeyChain
from yandex_checkout_payout.domain.notification.error_deposition_notification import ErrorDepositionNotification
from yandex_checkout_payout.domain.request.make_deposition_request import MakeDepositionRequest
from yandex_checkout_payout.domain.request.synonym_card_request import SynonymCardRequest
from yandex_checkout_payout.domain.request.test_deposition_request import TestDepositionRequest
from yandex_checkout_payout.domain.response.balance_response import BalanceResponse
from yandex_checkout_payout.domain.response.deposition_response import DepositionResponse
from yandex_checkout_payout.domain.response.synonym_card_response import SynonymCardResponse
from yandex_checkout_payout.yandex_checkout_payout import YandexCheckoutPayout


class TestNotification(unittest.TestCase):

    def setUp(self):  # Set the keychain for all tests
        keychain = KeyChain(abspath('../files/250000.cer'), abspath('../files/privateKey.pem'), '12345')
        Configuration.configure(250000, keychain)

    def test_request(self):
        data = b'-----BEGIN PKCS7-----\r\n' \
               b'MIIDGAYJKoZIhvcNAQcCoIIDCTCCAwUCAQExDzANBglghkgBZQMEAgEFADB/Bgkq\r\n' \
               b'hkiG9w0BBwGgcgRwPEVycm9yRGVwb3NpdGlvbk5vdGlmaWNhdGlvblJlc3BvbnNl\r\n' \
               b'IGNsaWVudE9yZGVySWQ9Ik5vbmUiIHByb2Nlc3NlZERUPSIyMDIwLTAzLTEwVDIz\r\n' \
               b'OjA2OjUwLjA2Mjk1MSIgc3RhdHVzPSIwIiAvPjGCAmwwggJoAgEBMFowQzESMBAG\r\n' \
               b'CgmSJomT8ixkARkWAnJ1MRcwFQYKCZImiZPyLGQBGRYHeWFtb25leTEUMBIGA1UE\r\n' \
               b'AxMLTkJDTyBZTSBJbnQCExcAAE7b+LBqLpypzCQAAAAATtswDQYJYIZIAWUDBAIB\r\n' \
               b'BQCggeQwGAYJKoZIhvcNAQkDMQsGCSqGSIb3DQEHATAcBgkqhkiG9w0BCQUxDxcN\r\n' \
               b'MjAwMzEwMjAwNjUwWjAvBgkqhkiG9w0BCQQxIgQgXCyh1zTmx+Z6cOslKYO2DSQR\r\n' \
               b'a1SSm8GOWzVERie6tB4weQYJKoZIhvcNAQkPMWwwajALBglghkgBZQMEASowCwYJ\r\n' \
               b'YIZIAWUDBAEWMAsGCWCGSAFlAwQBAjAKBggqhkiG9w0DBzAOBggqhkiG9w0DAgIC\r\n' \
               b'AIAwDQYIKoZIhvcNAwICAUAwBwYFKw4DAgcwDQYIKoZIhvcNAwICASgwDQYJKoZI\r\n' \
               b'hvcNAQEBBQAEggEAsB1DPguAXGF/qSmL/XkqUZtSgUnRdoGBLcb+HLlp0P32XOm/\r\n' \
               b'OXdRQmG4EbHBjZQT6XOrHB/SiX5SeVLnbJeU/JKLx/ZubgtscklKk8/SxZpLxfWe\r\n' \
               b'jp1T21YAzXjNvBs3j318ap9uksGNvJiP+F/iT/u9cmMsh09gDDI4RzLkr5gWe92A\r\n' \
               b'ujn6Vu8D7FC+OH2n7H/mKXZ8ZrqFrIGbMxvarixgX7RW2jineKZ8cT964pLoYp1g\r\n' \
               b'9tSDUkw6scBQmKu5Sek1kzDcbXIqUU6d8dP8Bux8YpkT3LG/0WW7UMp4YtFNydF3\r\n' \
               b'WSJjfNJF0W+8sPKZvp5hC4ZsBjVSRyaCzL20NA==\r\n' \
               b'-----END PKCS7-----\r\n'
        request = ErrorDepositionNotification.input(data)
        var_dump(request)
        # self.assertIsInstance(response, BalanceResponse)
        # self.assertEqual(response.client_order_id, client_order_id)

    def test_response(self):
        status = 0
        response = ErrorDepositionNotification.output(status)
        var_dump(response)
        # self.assertIsInstance(response, BalanceResponse)
        # self.assertEqual(response.client_order_id, client_order_id)
