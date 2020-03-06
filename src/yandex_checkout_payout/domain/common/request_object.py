# -*- coding: utf-8 -*-
import datetime

from yandex_checkout_payout.domain.common.base_object import BaseObject
from yandex_checkout_payout.domain.common.data_context import DataContext


class RequestObject(BaseObject):
    """
    Base class for request objects
    """
    __request_dt = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request_dt = datetime.datetime.now()

    @property
    def request_dt(self):
        return self.__request_dt

    @request_dt.setter
    def request_dt(self, value):
        if isinstance(value, str):
            try:
                self.__request_dt = datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')
            except Exception:
                raise TypeError('Invalid request_dt value type')
        elif isinstance(value, datetime.datetime):
            self.__request_dt = value
        else:
            raise TypeError('Invalid request_dt value type')

    @staticmethod
    def context():
        return DataContext.REQUEST

    def map(self):
        """
        Mapping request data to protocol
        """
        return {
            "requestDT": self.request_dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + "Z"
        }

    def validate(self):
        """
        Validate request data
        """
        pass
