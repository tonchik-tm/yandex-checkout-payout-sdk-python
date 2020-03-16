# -*- coding: utf-8 -*-
from yandex_checkout_payout.domain.request.deposition_request import DepositionRequest


class TestDepositionRequest(DepositionRequest):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request_name = 'testDeposition'

    def map(self):
        _map = super().map()
        return {self.request_name + 'Request': _map}
