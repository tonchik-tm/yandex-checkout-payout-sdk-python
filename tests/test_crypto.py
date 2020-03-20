# -*- coding: utf-8 -*-
import re
import unittest

from OpenSSL import crypto

from yandex_checkout_payout.domain.common.openssl_helper import OpenSSLHelper


class TestAll(unittest.TestCase):
    TYPE_RSA = crypto.TYPE_RSA
    TYPE_DSA = crypto.TYPE_DSA

    def createKeyPair(self, type, bits):
        """
            Create a public/private key pair.
            Arguments:
              type - Key type, must be one of TYPE_RSA and TYPE_DSA
              bits - Number of bits to use in the key
            Returns:   The public/private key pair in a PKey object
       """
        pkey = crypto.PKey()
        pkey.generate_key(type, bits)
        return pkey

    def createCertRequest(self, pkey, digest="md5", **name):
        """
            Create a certificate request.
            Arguments:
              pkey   - The key to associate with the request
              digest - Digestion method to use for signing, default is md5
              **name - The name of the subject of the request, possible arguments are:
                  C     - Country name
                  ST    - State or province name
                  L     - Locality name
                  O     - Organization name
                  OU    - Organizational unit name
                  CN    - Common name
                  emailAddress - E-mail address
            Returns:   The certificate request in an X509Req object
       """
        req = crypto.X509Req()
        subj = req.get_subject()

        for (key, value) in name.items():
            setattr(subj, key, value)

        req.set_pubkey(pkey)
        req.sign(pkey, digest)
        return req

    def createCertificate(self, req, issuerCertKey, serial, validityPeriod, digest="sha256"):
        """
            Generate a certificate given a certificate request.
            Arguments:
                req        - Certificate request to use
                issuerCert - The certificate of the issuer
                issuerKey  - The private key of the issuer
                serial     - Serial number for the certificate
                notBefore  - Timestamp (relative to now) when the certificate starts being valid
                notAfter   - Timestamp (relative to now) when the certificate stops being valid
                digest     - Digest method to use for signing, default is sha256
            Returns:   The signed certificate in an X509 object
        """
        issuerCert, issuerKey = issuerCertKey
        notBefore, notAfter = validityPeriod
        cert = crypto.X509()
        cert.set_serial_number(serial)
        cert.gmtime_adj_notBefore(notBefore)
        cert.gmtime_adj_notAfter(notAfter)
        cert.set_issuer(issuerCert.get_subject())
        cert.set_subject(req.get_subject())
        cert.set_pubkey(req.get_pubkey())
        cert.sign(issuerKey, digest)
        return cert

    def createSignature(self, request_file):
        output = OpenSSLHelper.exec_cmd(['openssl', 'req', '-in', request_file, '-noout', '-text'], '')
        match_obj = re.search(r'Signature Algorithm: (.*)', output.decode(), re.M | re.I | re.S | re.A)
        if match_obj:
            sign_lines = match_obj.group(1).split('         ')
            sign_lines.pop(0)
            signature = ''.join(sign_lines)
        else:
            signature = None

        return signature

    def test_all(self):
        cakey = self.createKeyPair(crypto.TYPE_RSA, 2048)
        careq = self.createCertRequest(cakey, CN='Certificate Authority')
        cacert = self.createCertificate(careq, (careq, cakey), 123456789, (0, 60 * 60 * 24 * 365))  # one year

        with open('clientkey.key', 'wb') as pem:
            pem.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, cakey, 'aes256', '12345678'.encode()))

        with open('clientcert.crt', 'wb') as cert:
            cert.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cacert))

        with open('clientreq.csr', 'wb') as req:
            req.write(crypto.dump_certificate_request(crypto.FILETYPE_PEM, careq))

        signature = self.createSignature('clientreq.csr')
        with open('signature.txt', 'wb') as sign:
            sign.write(signature.encode('utf-8'))

        # crypto.verify()

        certobj = cacert
        # crypto.load_certificate(crypto.FILETYPE_ASN1, cacert)

        issuer = certobj.get_issuer()
        subject = certobj.get_subject()
        cryptCert = certobj.to_cryptography()

        certDetails = {
            "SerialNumber": certobj.get_serial_number(),
            "Organization": subject.CN,
            "Signature": signature.encode(),
            "SignatureAlgorithm": certobj.get_signature_algorithm(),
            "CertificatePEM": crypto.dump_certificate(crypto.FILETYPE_PEM, certobj),
            "SubjectPublicKeyPEM": crypto.dump_publickey(crypto.FILETYPE_PEM, certobj.get_pubkey()),
            "Version": certobj.get_version()
        }
