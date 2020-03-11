# -*- coding: utf-8 -*-
import datetime

from yandex_checkout_payout.domain.common.base_object import BaseObject
from yandex_checkout_payout.domain.common.data_context import DataContext


class ErrorDepositionNotificationResponse(BaseObject):

    __processed_dt = None
    __client_order_id = None
    __status = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.processed_dt = datetime.datetime.now()

    @staticmethod
    def context():
        return DataContext.RESPONSE

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

    def validate(self):
        if self.client_order_id is None:
            self.__set_validation_error('ErrorDepositionNotificationResponse client_order_id not specified')
        if self.status is None:
            self.__set_validation_error('ErrorDepositionNotificationResponse status not specified')

    def __set_validation_error(self, message):
        raise ValueError(message)

    def map(self):
        return {
            "ErrorDepositionNotificationResponse": {
                "clientOrderId": self.client_order_id,
                "processedDT": self.processed_dt.strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
                "status": self.status,
            }
        }