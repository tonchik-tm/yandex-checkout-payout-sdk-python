# -*- coding: utf-8 -*-
import datetime

from yandex_checkout_payout.domain.common.base_object import BaseObject
from yandex_checkout_payout.domain.common.data_context import DataContext


class ErrorDepositionNotificationRequest(BaseObject):

    __processed_dt = None
    __client_order_id = None
    __dst_account = None
    __amount = None
    __currency = None
    __status = None
    __error = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def context():
        return DataContext.REQUEST

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = int(value)

    @property
    def processed_dt(self):
        return self.__processed_dt

    @processed_dt.setter
    def processed_dt(self, value):
        if isinstance(value, str):
            try:
                self.__processed_dt = datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f%z')
            except Exception:
                raise TypeError('Invalid request_dt value type')
        elif isinstance(value, datetime.datetime):
            self.__processed_dt = value
        else:
            raise TypeError('Invalid request_dt value type')

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
        self.__amount = str(value)

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
