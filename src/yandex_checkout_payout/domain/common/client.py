# -*- coding: utf-8 -*-
from yandex_checkout_payout.domain.exceptions.open_ssl_error import OpenSSLError

try:
    from StringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

import requests
import urllib3
from requests.adapters import HTTPAdapter
from urllib3 import Retry
from urllib3.util.ssl_ import create_urllib3_context

from yandex_checkout_payout.configuration import Configuration
from yandex_checkout_payout.domain.common.openssl_helper import OpenSSLHelper
from yandex_checkout_payout.domain.common.xml_helper import XMLHelper
from yandex_checkout_payout.domain.request.request_object import RequestObject
from yandex_checkout_payout.domain.request.synonym_card_request import SynonymCardRequest
from yandex_checkout_payout.domain.exceptions.api_error import ApiError
from yandex_checkout_payout.domain.exceptions.bad_request_error import BadRequestError
from yandex_checkout_payout.domain.exceptions.forbidden_error import ForbiddenError
from yandex_checkout_payout.domain.exceptions.not_found_error import NotFoundError
from yandex_checkout_payout.domain.exceptions.response_processing_error import ResponseProcessingError
from yandex_checkout_payout.domain.exceptions.too_many_request_error import TooManyRequestsError
from yandex_checkout_payout.domain.exceptions.unauthorized_error import UnauthorizedError
from yandex_checkout_payout.domain.request.request_object import RequestObject
from yandex_checkout_payout.domain.request.synonym_card_request import SynonymCardRequest


class ApiClient:
    DEPOSITION_REQUEST = 'webservice/deposition/api/{}'
    BALANCE_REQUEST = 'webservice/deposition/api/balance'
    SYNONYM_CARD_REQUEST = 'gates/card/storeCard'

    endpoint = Configuration.api_endpoint()

    def __init__(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        # requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        self.configuration = Configuration.instantiate()
        self.agent_id = self.configuration.agent_id
        self.keychain = self.configuration.keychain
        self.timeout = self.configuration.timeout
        self.max_attempts = self.configuration.max_attempts

    def request(self, path="", body=None, headers=None, method="POST", query_params=None, is_ssl=True):
        body = self.prepare_body(body, is_ssl)
        self.endpoint = Configuration.api_endpoint(is_ssl)
        request_headers = self.prepare_request_headers(headers)
        raw_response = self.execute(body, method, path, query_params, request_headers, is_ssl)

        if raw_response.status_code != 200:
            self.__handle_error(raw_response)

        if is_ssl:
            return self.prepare_response(raw_response.content)
        else:
            return raw_response.json()

    def prepare_response(self, response):
        try:
            xml = OpenSSLHelper.decrypt_pkcs7(response.decode("utf-8"), self.configuration.yandex_cert)
            xml = xml.replace(b'\r', b'')
            return XMLHelper.xml_to_object(xml.decode("utf-8"))
        except OpenSSLError:
            return None

    def execute(self, body, method, path, query_params, request_headers, is_ssl=True):
        session = self.get_session(is_ssl)
        raw_response = session.request(
            method,
            self.endpoint + path,
            params=query_params,
            headers=request_headers,
            data=body,
            verify=False
        )
        session.close()
        return raw_response

    def get_session(self, is_ssl=True):
        session = requests.Session()
        retries = Retry(total=self.max_attempts,
                        backoff_factor=self.timeout / 1000,
                        method_whitelist=['POST'],
                        status_forcelist=[202])
        if is_ssl:
            session.mount('https://', SSLAdapter(keychain=self.keychain, max_retries=retries))
        else:
            session.mount('https://', HTTPAdapter(max_retries=retries))
        return session

    def prepare_request_headers(self, headers):
        request_headers = {'Content-type': 'application/pkcs7-mime'}
        if isinstance(headers, dict):
            request_headers.update(headers)
        return request_headers

    def __handle_error(self, raw_response):
        http_code = raw_response.status_code
        if http_code == BadRequestError.HTTP_CODE:
            raise BadRequestError(raw_response)
        elif http_code == ForbiddenError.HTTP_CODE:
            raise ForbiddenError(raw_response)
        elif http_code == NotFoundError.HTTP_CODE:
            raise NotFoundError(raw_response)
        elif http_code == TooManyRequestsError.HTTP_CODE:
            raise TooManyRequestsError(raw_response)
        elif http_code == UnauthorizedError.HTTP_CODE:
            raise UnauthorizedError(raw_response)
        elif http_code == ResponseProcessingError.HTTP_CODE:
            raise ResponseProcessingError(raw_response)
        else:
            raise ApiError(raw_response.text)

    def prepare_body(self, body, is_ssl):
        if isinstance(body, RequestObject):
            body.validate()
            if is_ssl:
                body = OpenSSLHelper.encrypt_pkcs7(XMLHelper.object_to_xml(body.map()), self.keychain)
            else:
                body = dict(body)
        elif isinstance(body, SynonymCardRequest):
            body = urlencode(body.map())
        return body


class SSLAdapter(HTTPAdapter):
    def __init__(self, keychain, *args, **kwargs):
        self._keychain = keychain
        return super(SSLAdapter, self).__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        self._add_ssl_context(kwargs)
        return super(SSLAdapter, self).init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        self._add_ssl_context(kwargs)
        return super(SSLAdapter, self).proxy_manager_for(*args, **kwargs)

    def _add_ssl_context(self, kwargs):
        context = create_urllib3_context()
        context.load_cert_chain(certfile=self._keychain.public_cert,
                                keyfile=self._keychain.private_key,
                                password=str(self._keychain.key_password))
        kwargs['ssl_context'] = context
