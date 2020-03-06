# -*- coding: utf-8 -*-
import json

import urllib3

try:
    from StringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

import pycurl
import requests
import var_dump
from requests.adapters import HTTPAdapter
from requests.auth import _basic_auth_str
from urllib3 import Retry
from urllib3.util.ssl_ import create_urllib3_context

from yandex_checkout_payout.configuration import Configuration
from yandex_checkout_payout.domain.common.openssl_helper import OpenSSLHelper
from yandex_checkout_payout.domain.common.request_object import RequestObject
from yandex_checkout_payout.domain.common.xml_helper import XMLHelper
from yandex_checkout_payout.domain.exceptions.api_error import ApiError
from yandex_checkout_payout.domain.exceptions.bad_request_error import BadRequestError
from yandex_checkout_payout.domain.exceptions.forbidden_error import ForbiddenError
from yandex_checkout_payout.domain.exceptions.not_found_error import NotFoundError
from yandex_checkout_payout.domain.exceptions.response_processing_error import ResponseProcessingError
from yandex_checkout_payout.domain.exceptions.too_many_request_error import TooManyRequestsError
from yandex_checkout_payout.domain.exceptions.unauthorized_error import UnauthorizedError


class ApiClient:
    DEPOSITION_REQUEST = 'webservice/deposition/api/%s'
    BALANCE_REQUEST = 'webservice/deposition/api/balance'

    endpoint = Configuration.api_endpoint()

    def __init__(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        # requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        self.configuration = Configuration.instantiate()
        self.agent_id = self.configuration.agent_id
        self.keychain = self.configuration.keychain
        self.timeout = self.configuration.timeout
        self.max_attempts = self.configuration.max_attempts

        # self.user_agent = UserAgent()
        # if self.configuration.agent_framework:
        #     self.user_agent.framework = self.configuration.agent_framework
        # if self.configuration.agent_cms:
        #     self.user_agent.cms = self.configuration.agent_cms
        # if self.configuration.agent_module:
        #     self.user_agent.module = self.configuration.agent_module

    def request(self, path="", body=None, headers=None, method="POST", query_params=None):
        if isinstance(body, RequestObject):
            body.validate()
            body = OpenSSLHelper.encrypt_pkcs7(XMLHelper.object_to_xml(body.map()), self.keychain)

        request_headers = self.prepare_request_headers(headers)
        raw_response = self.execute(body, method, path, query_params, request_headers)
        # raw_response = self.execute_curl(body, method, path, query_params, request_headers)

        if raw_response.status_code != 200:
            self.__handle_error(raw_response)

        # return raw_response.json()
        return self.prepare_response(raw_response.content)

    def prepare_response(self, response):
        try:
            xml = OpenSSLHelper.decrypt_pkcs7(response.decode("utf-8"), self.configuration.yandex_cert)
            xml = xml.replace(b'\r', b'')
            return XMLHelper.xml_to_object(xml.decode("utf-8"))
        except Exception:
            return None

    def execute_curl(self, body, method, path, params, headers):
        b = BytesIO()
        c = pycurl.Curl()
        url = self.endpoint + path

        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.WRITEFUNCTION, b.write)
        # c.setopt(pycurl.RETURNTRANSFER, True)
        c.setopt(pycurl.HEADER, True)
        # c.setopt(pycurl.TRANSFER_ENCODING, True)
        c.setopt(pycurl.POST, True)
        c.setopt(pycurl.SSL_VERIFYPEER, False)
        c.setopt(pycurl.SSL_VERIFYHOST, False)
        # c.setopt(pycurl.CAINFO, "/path/cacert.pem")
        c.setopt(pycurl.SSLCERT, self.keychain.public_cert)
        c.setopt(pycurl.SSLKEY, self.keychain.private_key)
        c.setopt(pycurl.SSLKEYPASSWD, self.keychain.key_password)
        c.setopt(pycurl.CUSTOMREQUEST, method)
        if body:
            c.setopt(pycurl.POSTFIELDS, body)
        if headers:
            c.setopt(pycurl.HTTPHEADER, headers)
        c.setopt(pycurl.CONNECTTIMEOUT, self.configuration.timeout)
        c.setopt(pycurl.TIMEOUT, self.configuration.timeout)
        c.setopt(pycurl.VERBOSE, True)

        c.perform()
        ret = {
            "status_code": c.getinfo(pycurl.RESPONSE_CODE),
            "total_time": c.getinfo(c.TOTAL_TIME),
            "content_type": c.getinfo(pycurl.CONTENT_TYPE),
            "content_length_download": c.getinfo(pycurl.CONTENT_LENGTH_DOWNLOAD),
            "content": b.getvalue().decode("utf-8")
        }
        c.close()

        return ret

    def execute(self, body, method, path, query_params, request_headers):
        session = self.get_session()
        # var_dump.var_dump([
        #     method,
        #     self.endpoint + path,
        #     query_params,
        #     request_headers,
        #     body,
        #     self.keychain
        # ])
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

    def get_session(self):
        session = requests.Session()
        retries = Retry(total=self.max_attempts,
                        backoff_factor=self.timeout / 1000,
                        method_whitelist=['POST'],
                        status_forcelist=[202])
        session.mount('https://', SSLAdapter(keychain=self.keychain, max_retries=retries))
        return session

    def prepare_request_headers(self, headers):
        # request_headers = ['Content-type: application/pkcs7-mime']
        request_headers = {'Content-type': 'application/pkcs7-mime'}
        # if self.auth_token is not None:
        #     auth_headers = {"Authorization": "Bearer " + self.auth_token}
        # else:
        #     auth_headers = {"Authorization": _basic_auth_str(self.shop_id, self.shop_password)}

        # request_headers.update(auth_headers)

        # request_headers.update({"YM-User-Agent": self.user_agent.get_header_string()})

        if isinstance(headers, dict):
            request_headers.extend(headers)
        return request_headers

    def __handle_error(self, raw_response):
        http_code = raw_response.status_code
        if http_code == BadRequestError.HTTP_CODE:
            raise BadRequestError(raw_response.json())
        elif http_code == ForbiddenError.HTTP_CODE:
            raise ForbiddenError(raw_response.json())
        elif http_code == NotFoundError.HTTP_CODE:
            raise NotFoundError(raw_response.json())
        elif http_code == TooManyRequestsError.HTTP_CODE:
            raise TooManyRequestsError(raw_response.json())
        elif http_code == UnauthorizedError.HTTP_CODE:
            raise UnauthorizedError(raw_response.json())
        elif http_code == ResponseProcessingError.HTTP_CODE:
            raise ResponseProcessingError(raw_response.json())
        else:
            raise ApiError(raw_response.text)


class SSLAdapter(HTTPAdapter):
    def __init__(self, keychain, *args, **kwargs):
        self._keychain = keychain
        return super(self.__class__, self).__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        self._add_ssl_context(kwargs)
        return super(self.__class__, self).init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        self._add_ssl_context(kwargs)
        return super(self.__class__, self).proxy_manager_for(*args, **kwargs)

    def _add_ssl_context(self, kwargs):
        context = create_urllib3_context()
        context.load_cert_chain(certfile=self._keychain.public_cert,
                                keyfile=self._keychain.private_key,
                                password=str(self._keychain.key_password))
        kwargs['ssl_context'] = context
