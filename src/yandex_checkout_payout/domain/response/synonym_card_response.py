# -*- coding: utf-8 -*-
from yandex_checkout_payout.domain.common.base_object import BaseObject


class SynonymCardResponse(BaseObject):

    __id = None
    __panmask = None
    __synonym = None
    __reason = None
    __bank_name = None
    __country_code = None
    __payment_system = None
    __product_name = None
    __product_code = None

    @property
    def panmask(self):
        return self.__panmask

    @panmask.setter
    def panmask(self, value):
        self.__panmask = str(value)

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = int(value)

    @property
    def synonym(self):
        return self.__synonym

    @synonym.setter
    def synonym(self, value):
        self.__synonym = str(value)

    @property
    def reason(self):
        return self.__reason

    @reason.setter
    def reason(self, value):
        self.__reason = str(value)

    @property
    def bank_name(self):
        return self.__bank_name

    @bank_name.setter
    def bank_name(self, value):
        self.__bank_name = str(value)

    @property
    def country_code(self):
        return self.__country_code

    @country_code.setter
    def country_code(self, value):
        self.__country_code = str(value)

    @property
    def payment_system(self):
        return self.__payment_system

    @payment_system.setter
    def payment_system(self, value):
        self.__payment_system = str(value)

    @property
    def product_name(self):
        return self.__product_name

    @product_name.setter
    def product_name(self, value):
        self.__product_name = str(value)

    @property
    def product_code(self):
        return self.__product_code

    @product_code.setter
    def product_code(self, value):
        self.__product_code = str(value)

    def validate(self):
        if self.panmask is None:
            self.__set_validation_error('SynonymCard panmask not specified')

        if self.synonym is None:
            self.__set_validation_error('SynonymCard synonym not specified')

        if self.reason is None:
            self.__set_validation_error('SynonymCard reason not specified')

    def __set_validation_error(self, message):
        raise ValueError(message)

    def map_in(self):
        return {
            "skr_destinationCardPanmask": "panmask",
            "skr_destinationCardSynonim": "synonym",
            "reason": "reason",
            "skr_int_id": "id",
            "skr_destinationCardBankName": "bank_name",
            "skr_destinationCardCountryCode": "country_code",
            "skr_destinationCardPaymentSystem": "payment_system",
            "skr_destinationCardProductName": "product_name",
            "skr_destinationCardProductCode": "product_code",
        }
