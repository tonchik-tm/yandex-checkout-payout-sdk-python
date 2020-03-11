# -*- coding: utf-8 -*-
from yandex_checkout_payout.domain.models.recipients.recipient import Recipient
from yandex_checkout_payout.domain.models.recipients.recipient_factory import RecipientFactory
from yandex_checkout_payout.domain.request.deposition_request import DepositionRequest


class MakeDepositionRequest(DepositionRequest):

    __payment_params = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request_name = 'makeDeposition'

    @property
    def payment_params(self):
        return self.__payment_params

    @payment_params.setter
    def payment_params(self, value):
        if isinstance(value, Recipient):
            self.__payment_params = value
        elif isinstance(value, dict):
            self.__payment_params = RecipientFactory.factory(value)
        else:
            raise TypeError('Invalid pdr_doc_issue_date value type')

    def map(self):
        _map = super().map()
        if self.payment_params:
            _map.update({
                "paymentParams": self.payment_params.map()
            })
        return {self.request_name + 'Request': _map}