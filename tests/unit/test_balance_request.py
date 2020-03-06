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
        request.request_dt = '2020-03-04T15:39:45.456Z'

        self.assertEqual({
            'agent_id': '123456',
            'client_order_id': '215d8da0-000f-50be-b000-0003308c89be',
            'request_dt': datetime.datetime(2020, 3, 4, 15, 39, 45, 456000)
        }, dict(request))

    def test_request_setters(self):
        request = BalanceRequest({
            'agent_id': 123456,
            'client_order_id': '215d8da0-000f-50be-b000-0003308c89be',
            'request_dt': '2020-03-04T15:39:45.456Z'
        })

        self.assertIsInstance(request.agent_id, str)
        self.assertIsInstance(request.request_dt, datetime.datetime)

        with self.assertRaises(TypeError):
            request.request_dt = 'invalid request_dt'

        # with self.assertRaises(TypeError):
        #     request.items = 'invalid items'
        #
        # with self.assertRaises(TypeError):
        #     request.settlements = 'invalid settlements'

    def test_request_validate(self):
        request = ReceiptRequest()

        with self.assertRaises(ValueError):
            request.validate()

        request.type = ReceiptType.PAYMENT

        with self.assertRaises(ValueError):
            request.validate()

        request.send = True

        with self.assertRaises(ValueError):
            request.validate()

        request.customer = ReceiptCustomer({'phone': '79990000000', 'email': 'test@email.com'})

        with self.assertRaises(ValueError):
            request.validate()

        request.items = [
            ReceiptItem({
                "description": "Product 1",
                "quantity": 2.0,
                "amount": {
                    "value": 250.0,
                    "currency": Currency.RUB
                },
                "vat_code": 2
            }),
            ReceiptItem({
                "description": "Product 2",
                "quantity": 1.0,
                "amount": {
                    "value": 100.0,
                    "currency": Currency.RUB
                },
                "vat_code": 2
            })
        ]

        with self.assertRaises(ValueError):
            request.validate()

        request.settlements = [
            Settlement({
                'type': SettlementType.CASHLESS,
                'amount': {
                    'value': 250.0,
                    'currency': Currency.RUB
                }
            })
        ]

        with self.assertRaises(ValueError):
            request.validate()

        request.tax_system_code = 1

        with self.assertRaises(ValueError):
            request.validate()

        request.refund_id = '215d8da0-000f-50be-b000-0003308c89be'

        with self.assertRaises(ValueError):
            request.validate()

        request.payment_id = '215d8da0-000f-50be-b000-0003308c89be'

        self.assertIsNone(request.validate())
