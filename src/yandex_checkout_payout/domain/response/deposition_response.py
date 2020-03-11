# -*- coding: utf-8 -*-
from yandex_checkout_payout.domain.response.response_object import ResponseObject


class DepositionResponse(ResponseObject):

    __client_order_id = None
    __error = None
    __tech_message = None
    __identification = None

    @property
    def client_order_id(self):
        return self.__client_order_id

    @client_order_id.setter
    def client_order_id(self, value):
        self.__client_order_id = str(value)

    @property
    def error(self):
        return self.__error

    @error.setter
    def error(self, value):
        self.__error = int(value)

    @property
    def tech_message(self):
        return self.__tech_message

    @tech_message.setter
    def tech_message(self, value):
        self.__tech_message = str(value)

    @property
    def identification(self):
        return self.__identification

    @identification.setter
    def identification(self, value):
        self.__identification = str(value)

    def validate(self):
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
            "error": "error",
            "techMessage": "tech_message",
            "identification": "identification",
        })
        return _map