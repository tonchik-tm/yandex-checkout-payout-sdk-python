# -*- coding: utf-8 -*-
from yandex_checkout_payout.domain.common.base_object import BaseObject


class Recipient(BaseObject):

    __pof_offer_accepted = None

    @property
    def pof_offer_accepted(self):
        return self.__pof_offer_accepted

    @pof_offer_accepted.setter
    def pof_offer_accepted(self, value):
        self.__pof_offer_accepted = bool(value)

    def map(self):
        return {
            "pof_offerAccepted": [str(int(self.pof_offer_accepted))]
        }
