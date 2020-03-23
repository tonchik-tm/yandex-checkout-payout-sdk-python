# -*- coding: utf-8 -*-
from yandex_checkout_payout.domain.request.request_object import RequestObject


class DepositionRequest(RequestObject):

    __agent_id = None
    __client_order_id = None
    __dst_account = None
    __amount = None
    __currency = None
    __contract = None

    def __init__(self, *args, **kwargs):
        super(DepositionRequest, self).__init__(*args, **kwargs)
        self.request_name = 'deposition'

    @property
    def agent_id(self):
        return self.__agent_id

    @agent_id.setter
    def agent_id(self, value):
        self.__agent_id = int(value)

    @property
    def client_order_id(self):
        return self.__client_order_id

    @client_order_id.setter
    def client_order_id(self, value):
        self.__client_order_id = str(value)

    @property
    def dst_account(self):
        return self.__dst_account

    @dst_account.setter
    def dst_account(self, value):
        self.__dst_account = str(value)

    @property
    def amount(self):
        return self.__amount

    @amount.setter
    def amount(self, value):
        self.__amount = float(value)

    @property
    def currency(self):
        return self.__currency

    @currency.setter
    def currency(self, value):
        self.__currency = int(value)

    @property
    def contract(self):
        return self.__contract

    @contract.setter
    def contract(self, value):
        self.__contract = str(value)

    def validate(self):
        super(DepositionRequest, self).validate()
        if not self.agent_id:
            self.set_validation_error('Deposition agent_id not specified')
        if not self.client_order_id:
            self.set_validation_error('Deposition client_order_id not specified')

    def map(self):
        _map = super(DepositionRequest, self).map()
        _map.update({
            "agentId": self.agent_id,
            "clientOrderId": self.client_order_id,
            "dstAccount": self.dst_account,
            "amount": format(self.amount, ".2f"),
            "currency": self.currency,
            "contract": self.contract,
        })
        return _map

