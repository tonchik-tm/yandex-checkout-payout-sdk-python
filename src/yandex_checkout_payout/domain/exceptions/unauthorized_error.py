# -*- coding: utf-8 -*-
from yandex_checkout_payout.domain.exceptions.api_error import ApiError


class UnauthorizedError(ApiError):
    HTTP_CODE = 401
