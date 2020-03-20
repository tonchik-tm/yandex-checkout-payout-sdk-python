# -*- coding: utf-8 -*-


import unittest
import uuid
from os.path import abspath
from subprocess import Popen, PIPE
from OpenSSL import crypto
from lxml import etree

from yandex_checkout_payout import yandex_checkout_payout
from yandex_checkout_payout.configuration import Configuration
from yandex_checkout_payout.domain.common.currency import Currency
from yandex_checkout_payout.domain.common.generator_csr import GeneratorCsr
from yandex_checkout_payout.domain.common.keychain import KeyChain
from yandex_checkout_payout.domain.common.openssl_helper import OpenSSLHelper
from yandex_checkout_payout.domain.common.xml_helper import XMLHelper
from yandex_checkout_payout.domain.models.organization import Organization
from yandex_checkout_payout.domain.request.balance_request import BalanceRequest
from yandex_checkout_payout.domain.response.balance_response import BalanceResponse
from yandex_checkout_payout.yandex_checkout_payout import YandexCheckoutPayout


class TestYandexCheckoutPayout(unittest.TestCase):

    def test_yandex_checkout_payout(self):
        assert yandex_checkout_payout is not None

    def test_encrypt(self):
        # with open('./files/test.xml', encoding="utf-8") as data_file:
        #     data = data_file.read()

        # keychain = KeyChain(abspath('./files/250000.cer'), abspath('./files/privateKey.pem'), '12345')
        keychain = KeyChain(abspath('clientcert.crt'), abspath('clientkey.key'), '12345678')
        output = OpenSSLHelper.encrypt_pkcs7(OpenSSLHelper.from_file('./files/test.xml'), keychain=keychain)
        OpenSSLHelper.to_file('test.p7s', output)
        print(output.decode("utf-8"))

        assert output is not None

    def test_decrypt(self):
        # with open("./files/test.pkcs", encoding="utf-8") as pkcs_file:
        #     pkcs = pkcs_file.read()
        pkcs = OpenSSLHelper.from_file('./files/test.pkcs')
        # print(pkcs)

        output = OpenSSLHelper.decrypt_pkcs7(pkcs, cert=abspath('./files/deposit.cer'))
        # print(output)
        # var_dump.var_dump(str(output, "utf-8", 'ignore'))
        # var_dump.var_dump(output.decode("utf-8"))
        # var_dump.var_dump(output)
        parser = etree.XMLParser(recover=True, encoding='utf-8')
        root = etree.fromstring(output, parser)
        # var_dump.var_dump(root.attrib)

        assert output is not None

    def test_decrypt_key(self):
        p_key = crypto.load_privatekey(crypto.FILETYPE_PEM, OpenSSLHelper.from_file('./files/privateKey.pem'), "12345".encode('utf-8'))
        dump_privatekey = crypto.dump_privatekey(crypto.FILETYPE_PEM, p_key)
        OpenSSLHelper.to_file('./files/privateKey.open', dump_privatekey)

    def test_generate_private_key(self):
        # output = OpenSSLHelper.create_private_key(abspath('./files/output/privateKey.pem'), '12341')
        key = crypto.PKey()
        key.generate_key(crypto.TYPE_RSA, 2048)
        # print(output.decode("utf-8"))
        with open(abspath('./files/output/privateKeyNew.pem'), "w", encoding="utf-8") as f:
            f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key, passphrase="12345".encode()).decode())
        # assert output is not None

    def test_generator(self):
        org = Organization({
            "country_name": "RU",
            "state": "Russia",
            "locality": "NN",
            "org_name": "Yandex Money",
            "org_unit_name": "Yandex.Money",
            "common_name": "/business/yandexmoney",
            "email": "cms@yamoney.ru"
        })
        gen = GeneratorCsr('12345', org, abspath('./files/output2'))
        gen.generate_all()

    def test_balance_request(self):
        client_order_id = uuid.uuid4()
        request = BalanceRequest({"agent_id": 123456, "client_order_id": client_order_id})
        # var_dump.var_dump(request.map())

    def test_client_balance_request(self):
        keychain = KeyChain(abspath('./files/250000.cer'), abspath('./files/privateKey.pem'), '12345')
        Configuration.configure(250000, keychain)
        client_order_id = str(uuid.uuid4())
        # request = BalanceRequest({"agent_id": 123456, "client_order_id": client_order_id})
        response = YandexCheckoutPayout.get_balance(client_order_id)
        # var_dump.var_dump(response)
        self.assertIsInstance(response, BalanceResponse)
        self.assertEqual(response.client_order_id, client_order_id)

    def test_balance_response(self):
        client_order_id = uuid.uuid4()
        response = BalanceResponse({
            "status": 0,
            "clientOrderId": client_order_id,
            "balance": 1000.0,
            "processedDT": "2011-07-01T20:38:01.666Z"
        })
        # var_dump.var_dump(dict(response))

    def test_xml2object(self):
        xml_string = """
        <balanceResponse clientOrderId="12345"
                 status="0"
                 processedDT="2011-07-01T20:38:01.666Z"
                 balance="1000.00"/>
        """

        python_object = XMLHelper.xml_to_object(xml_string)

        # var_dump.var_dump(xml_string)
        # var_dump.var_dump(python_object)

        response = BalanceResponse(python_object['balanceResponse'])
        print(dict(response))

    def test_object2xml(self):
        client_order_id = uuid.uuid4()
        request = BalanceRequest({"agent_id": 123456, "client_order_id": client_order_id})
        python_object = request.map()
        # python_object = {"balanceRequest": {
        #     "agentId": "123",
        #     "clientOrderId": "12345",
        #     "requestDT": "2011-07-01T20:38:00.000Z"
        # }}

        xml_string = XMLHelper.object_to_xml(python_object)

        # var_dump.var_dump(python_object)
        # var_dump.var_dump(xml_string)

    def test_hard_object2xml(self):
        # client_order_id = uuid.uuid4()
        # request = BalanceRequest({"agent_id": 123456, "client_order_id": client_order_id})
        # python_object = request.map()
        python_object = {"makeDepositionRequest": {
            "agentId": "123",
            "clientOrderId": "12345",
            "requestDT": "2011-07-01T20:38:00.000+03:00",
            "dstAccount": "41001614575714",
            "amount": 10.00,
            "currency": Currency.RUB,
            "contract": "Зачисление на кошелек",
            "paymentParams": {
                "skr_destinationCardSynonim": ["oALesdd_h_YT6pzpJ10Kn5aB.SC.000.201906"],
                "pof_offerAccepted": ["1"],
                "smsPhoneNumber": ["79818932328"],
                "pdr_firstName": ["Эдуард"],
                "pdr_lastName": ["Запеканкин"],
                "pdr_docNumber": ["1013123456"],
                "pdr_docIssueDate": ["10.10.2013"],
                "pdr_country": ["643"],
                "pdr_birthDate": ["31.10.1973"]
            }
        }}

        xml_string = XMLHelper.object_to_xml(python_object)
        # var_dump.var_dump(python_object)
        # var_dump.var_dump(xml_string)
