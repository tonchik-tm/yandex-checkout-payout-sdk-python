# -*- coding: utf-8 -*-
import unittest
import uuid

from os.path import abspath

from var_dump import var_dump

from yandex_checkout_payout.configuration import Configuration
from yandex_checkout_payout.domain.common.keychain import KeyChain
from yandex_checkout_payout.domain.notification.error_deposition_notification import ErrorDepositionNotification


class TestNotification(unittest.TestCase):

    def setUp(self):  # Set the keychain for all tests
        keychain = KeyChain(abspath('../files/250000.cer'), abspath('../files/privateKey.pem'), '12345')
        Configuration.configure(250000, keychain)

    def test_request(self):
        data = b'-----BEGIN PKCS7-----\r\n' \
               b'MIAGCSqGSIb3DQEHAqCAMIACAQExCzAJBgUrDgMCGgUAMIAGCSqGSIb3DQEHAaCA\r\n' \
               b'JIAEgac8ZXJyb3JEZXBvc2l0aW9uTm90aWZpY2F0aW9uUmVxdWVzdCBjbGllbnRP\r\n' \
               b'cmRlcklkPSIzMTY2NzExNyIgcmVxdWVzdERUPSIyMDIwLTAzLTEwVDIxOjQ4OjE3\r\n' \
               b'LjYwOFoiIGRzdEFjY291bnQ9IjI1NzAwMTMwNTM1MTg2IiBhbW91bnQ9IjUwMDAi\r\n' \
               b'IGN1cnJlbmN5PSI2NDMiIGVycm9yPSIzMSIvPgAAAAAAADGCAjcwggIzAgEBMIGE\r\n' \
               b'MHwxCzAJBgNVBAYTAlJVMQ8wDQYDVQQIEwZSdXNzaWExGTAXBgNVBAcTEFNhaW50\r\n' \
               b'LVBldGVyc2J1cmcxGDAWBgNVBAoTD1BTIFlhbmRleC5Nb25leTEQMA4GA1UECxMH\r\n' \
               b'VW5rbm93bjEVMBMGA1UEAxMMWWFuZGV4Lk1vbmV5AgRNWiVmMAkGBSsOAwIaBQCg\r\n' \
               b'gYgwGAYJKoZIhvcNAQkDMQsGCSqGSIb3DQEHATAcBgkqhkiG9w0BCQUxDxcNMjAw\r\n' \
               b'MzEwMjE0ODE3WjAjBgkqhkiG9w0BCQQxFgQUyRvLH4M6tP0gMKCdNMZsryyAJhQw\r\n' \
               b'KQYJKoZIhvcNAQk0MRwwGjAJBgUrDgMCGgUAoQ0GCSqGSIb3DQEBAQUAMA0GCSqG\r\n' \
               b'SIb3DQEBAQUABIIBAATmOL69LMjeW7NRcrk20XqqJ11rgHYaIx1DMFdJzUtpQlnX\r\n' \
               b'1r5fpvqXr4au0TR757OwMapQForPDULnuj9qT/LCRg+qAxcQbA+Bu6dXccpIvurx\r\n' \
               b'InFcSf9MlJsIB6twAMiXXASj/Smt0mtiAffIcxgYb5VZnFmf2JtyUbhLzg+jwegB\r\n' \
               b'm1Uy+a7ijiTpezce4aVxYvOkM5F9jm532oVxJ/WCou2SbszFqh7brlZJhLpBOG1r\r\n' \
               b'Z8ZbPrZY+Fl9H6t6GiMLWNuveOvBIfC5UvDSV2olsrVTl9qRtgXBQSF2O9wPSX1k\r\n' \
               b'9P2oWQ3dB/pDK4JKWIAVfaMTUdrIF4V2Wgdbd5YAAAAAAAA=\r\n' \
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
