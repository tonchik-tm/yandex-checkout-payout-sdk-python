# -*- coding: utf-8 -*-
"""Main module."""
import uuid
from os.path import abspath

from yandex_checkout_payout.domain.common.client import ApiClient
from yandex_checkout_payout.domain.common.generator_csr import GeneratorCsr
from yandex_checkout_payout.domain.exceptions.api_error import ApiError
from yandex_checkout_payout.domain.request.balance_request import BalanceRequest
from yandex_checkout_payout.domain.request.deposition_request import DepositionRequest
from yandex_checkout_payout.domain.request.deposition_request_builder import DepositionRequestBuilder
from yandex_checkout_payout.domain.request.synonym_card_request import SynonymCardRequest
from yandex_checkout_payout.domain.response.balance_response import BalanceResponse
from yandex_checkout_payout.domain.response.deposition_response_builder import DepositionResponseBuilder
from yandex_checkout_payout.domain.response.synonym_card_response import SynonymCardResponse


class YandexCheckoutPayout(object):
    """

    """
    def __init__(self):
        self.client = ApiClient()
        self.agent_id = self.client.configuration.agent_id

    @classmethod
    def get_balance(cls, client_order_id=None):
        instance = cls()
        path = instance.client.BALANCE_REQUEST

        if not client_order_id:
            client_order_id = uuid.uuid4()

        request = BalanceRequest({"agent_id": instance.agent_id, "client_order_id": client_order_id})
        response = instance.client.request(path, request)

        if response and 'balanceResponse' in response:
            return BalanceResponse(response['balanceResponse'])
        else:
            raise ApiError('Cannot get data!')

    @classmethod
    def get_synonym_card(cls, params):
        instance = cls()
        path = instance.client.SYNONYM_CARD_REQUEST

        if isinstance(params, dict):
            request = SynonymCardRequest(params)
        elif isinstance(params, SynonymCardRequest):
            request = params
        else:
            raise ApiError('Unsupported data format!')

        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        response = instance.client.request(path, request, headers=headers, is_ssl=False)

        if response and 'storeCard' in response:
            return SynonymCardResponse(response['storeCard'])
        else:
            raise ApiError('Cannot get data!')

    @classmethod
    def create_deposition(cls, params):
        instance = cls()
        path = instance.client.DEPOSITION_REQUEST

        if isinstance(params, dict):
            request = DepositionRequestBuilder.build(params)
        elif isinstance(params, DepositionRequest):
            request = params
        else:
            raise ApiError('Unsupported data format!')

        request.validate()

        response = instance.client.request(path.format(request.request_name), request)
        return DepositionResponseBuilder.build(response)

    @staticmethod
    def get_csr(org, output, key_pass):
        gen = GeneratorCsr(key_pass, org, abspath(output))
        gen.generate_all()
