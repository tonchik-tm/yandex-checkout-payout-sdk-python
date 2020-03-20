# -*- coding: utf-8 -*-
import sys
import unittest
from os.path import abspath
from requests import Response

from yandex_checkout_payout.configuration import Configuration
from yandex_checkout_payout.domain.common.client import ApiClient
from yandex_checkout_payout.domain.common.keychain import KeyChain
from yandex_checkout_payout.domain.request.request_object import RequestObject

if sys.version_info >= (3, 3):
    from unittest.mock import patch
else:
    from mock import patch


class TestClient(unittest.TestCase):
    def setUp(self):
        keychain = KeyChain(abspath('files/250000.cer'), abspath('files/privateKey.pem'), '12345')
        Configuration.configure(250000, keychain)

    def test_request(self):
        client = ApiClient()
        with patch('requests.Session.request') as request_mock:
            res = Response()
            res._content = b'-----BEGIN PKCS7-----\nMIAGCSqGSIb3DQEHAqCAMIACAQExCzAJBgUrDgMCGgUAMIAGCSqGSIb3DQEHAaCA\nJIAEgcA8P3htbCB2ZXJzaW9uPSIxLjAiIGVuY29kaW5nPSJVVEYtOCI/Pg0KPGJh\nbGFuY2VSZXNwb25zZSBjbGllbnRPcmRlcklkPSJkM2JjZWY3YS0xOTk3LTRkN2Mt\nODBjZi1lNjUwZjhhNzE3NjYiIHN0YXR1cz0iMCIgcHJvY2Vzc2VkRFQ9IjIwMjAt\nMDMtMTlUMTk6MzM6NDIuMTkxKzAzOjAwIiBiYWxhbmNlPSItMTc5MDgzODIuMTgi\nIC8+DQoAAAAAAAAxggI3MIICMwIBATCBhDB8MQswCQYDVQQGEwJSVTEPMA0GA1UE\nCBMGUnVzc2lhMRkwFwYDVQQHExBTYWludC1QZXRlcnNidXJnMRgwFgYDVQQKEw9Q\nUyBZYW5kZXguTW9uZXkxEDAOBgNVBAsTB1Vua25vd24xFTATBgNVBAMTDFlhbmRl\neC5Nb25leQIETVolZjAJBgUrDgMCGgUAoIGIMBgGCSqGSIb3DQEJAzELBgkqhkiG\n9w0BBwEwHAYJKoZIhvcNAQkFMQ8XDTIwMDMxOTE2MzM0MlowIwYJKoZIhvcNAQkE\nMRYEFJ8SzUYorMCRecEOXl/Isfy5F8Z0MCkGCSqGSIb3DQEJNDEcMBowCQYFKw4D\nAhoFAKENBgkqhkiG9w0BAQEFADANBgkqhkiG9w0BAQEFAASCAQBQxyZXxOVw5MC/\nfnYPfeqNiqpWp0CJb27nOEO71ZnbiGhzd6TJV3uDtojXp8We7Cm9aFIAwdbU/PjU\nXOvyY262DDf2fbJuMQJI59ObP1SANDiKvl17GQSAkNlKi5gDKZMAjJ4eDwu/mVYa\nNx8L30HlsOVqfhMo4hqkT77UHlo4gnK4tiH3I+MOxzIMhJPPXtrRj0Pu3vwUr4vA\nqayCwu/da/hOcwDAqw0auCck9fpDPEW/TcxJ0Ni+VYE1Zl/Giyz/K2jh6MB1E0rO\nKDic+FRjucCHG+WL8ko9jKpj5OfgAKr1292xgcpcUXSnMh2y43PgkP9L0P/QuIAM\n6RIQtmu0AAAAAAAA\n-----END PKCS7-----\n'
            res.status_code = 200

            request_mock.return_value = res

            response = client.request(client.BALANCE_REQUEST, RequestObject(), {'header': 'header'})
            self.assertIsInstance(response, dict)
