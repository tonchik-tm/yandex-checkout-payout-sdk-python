# -*- coding: utf-8 -*-
"""Main module."""
import uuid
from os.path import abspath

import var_dump

from yandex_checkout_payout.domain.common.client import ApiClient
from yandex_checkout_payout.domain.common.generator_csr import GeneratorCsr
from yandex_checkout_payout.domain.common.openssl_helper import OpenSSLHelper
from yandex_checkout_payout.domain.common.xml_helper import XMLHelper
from yandex_checkout_payout.domain.exceptions.api_error import ApiError
from yandex_checkout_payout.domain.request.balance_request import BalanceRequest
from yandex_checkout_payout.domain.request.balance_response import BalanceResponse


class YandexCheckoutPayout:

    def __init__(self):
        self.client = ApiClient()
        self.agent_id = self.client.configuration.agent_id

    # @classmethod
    # def create_deposition(cls):
    #     instance = cls()
    #     path = instance.client.DEPOSITION_REQUEST
    #
    #     response = instance.client.request(path, params)
    #     return DepositionResponse(response)

    @classmethod
    def get_balance(cls, client_order_id=None):
        instance = cls()
        path = instance.client.BALANCE_REQUEST

        if not client_order_id:
            client_order_id = uuid.uuid4()

        request = BalanceRequest({"agent_id": instance.agent_id, "client_order_id": client_order_id})
        response = instance.client.request(path, request)

        if response:
            return BalanceResponse(response['balanceResponse'])
        else:
            raise ApiError('Cannot get data!')

    @staticmethod
    def get_csr(org, output, key_pass):
        gen = GeneratorCsr(key_pass, org, abspath(output))
        gen.generate_all()
