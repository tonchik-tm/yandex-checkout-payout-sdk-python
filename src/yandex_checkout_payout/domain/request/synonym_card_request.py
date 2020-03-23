# -*- coding: utf-8 -*-

from yandex_checkout_payout.domain.common.base_object import BaseObject
from yandex_checkout_payout.domain.common.data_context import DataContext


class SynonymCardRequest(BaseObject):
    """
    Class for request
    """

    __destination_card_number = None
    __response_format = 'json'
    __error_url = None
    __success_url = None

    @property
    def destination_card_number(self):
        return self.__destination_card_number

    @destination_card_number.setter
    def destination_card_number(self, value):
        self.__destination_card_number = str(value)

    @property
    def response_format(self):
        return self.__response_format

    @response_format.setter
    def response_format(self, value):
        self.__response_format = str(value)

    @property
    def error_url(self):
        return self.__error_url

    @error_url.setter
    def error_url(self, value):
        self.__error_url = str(value)

    @property
    def success_url(self):
        return self.__success_url

    @success_url.setter
    def success_url(self, value):
        self.__success_url = str(value)

    @staticmethod
    def context():
        return DataContext.REQUEST

    def map(self):
        """
        Mapping request data to protocol
        """
        return {
            "skr_destinationCardNumber": self.destination_card_number,
            "skr_responseFormat": self.response_format,
            "skr_errorUrl": self.error_url,
            "skr_successUrl": self.success_url,
        }

    def validate(self):
        """
        Validate request data
        """
        pass
