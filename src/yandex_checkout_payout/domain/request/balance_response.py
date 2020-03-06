# -*- coding: utf-8 -*-
import datetime

from yandex_checkout_payout.domain.common.response_object import ResponseObject


class BalanceResponse(ResponseObject):

    __agent_id = None

    __client_order_id = None

    __balance = None

    @property
    def agent_id(self):
        return self.__agent_id

    @agent_id.setter
    def agent_id(self, value):
        self.__agent_id = str(value)

    @property
    def client_order_id(self):
        return self.__client_order_id

    @client_order_id.setter
    def client_order_id(self, value):
        self.__client_order_id = str(value)

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, value):
        self.__balance = float(value)

    def validate(self):
        if self.agent_id is None:
            self.__set_validation_error('Balance agent_id not specified')

        if self.client_order_id is None:
            self.__set_validation_error('Balance client_order_id not specified')

    def __set_validation_error(self, message):
        raise ValueError(message)

    def map_in(self):
        _map = super().map_in()
        _map.update({
            "agentId": "agent_id",
            "clientOrderId": "client_order_id",
            "balance": "balance",
        })
        return _map
