# -*- coding: utf-8 -*-
import unittest
from yandex_checkout_payout.domain.models.organization import Organization


class TestOrganization(unittest.TestCase):

    def test_organization_cast(self):
        org = Organization()
        org.country_name = 'RU'
        org.state = 'Russia'
        org.locality = ''
        org.org_name = 'Yandex Money'
        org.org_unit_name = ''
        org.common_name = 'yamoney'
        org.email = 'cms@yamoney.ru'

        self.assertEqual({
            'country_name': 'RU',
            'state': 'Russia',
            'locality': '-',
            'org_name': 'Yandex Money',
            'org_unit_name': '-',
            'common_name': '/business/yamoney',
            'email': 'cms@yamoney.ru',
        }, dict(org))

    def test_organization_setters(self):
        org = Organization({
            'country_name': 'RU',
            'state': 'Russia',
            'locality': '',
            'org_name': 'Yandex Money',
            'org_unit_name': '',
            'common_name': '/business/yamoney',
            'email': 'cms@yamoney.ru',
        })

        self.assertIsInstance(org.country_name, str)
        self.assertEqual(org.country_name, 'RU')

        self.assertIsInstance(org.state, str)
        self.assertEqual(org.state, 'Russia')

        self.assertIsInstance(org.locality, str)
        self.assertEqual(org.locality, '-')

        self.assertIsInstance(org.org_name, str)
        self.assertEqual(org.org_name, 'Yandex Money')

        self.assertIsInstance(org.org_unit_name, str)
        self.assertEqual(org.org_unit_name, '-')

        self.assertIsInstance(org.common_name, str)
        self.assertEqual(org.common_name, '/business/yamoney')

        self.assertIsInstance(org.email, str)
        self.assertEqual(org.email, 'cms@yamoney.ru')

        with self.assertRaises(ValueError):
            org.common_name = 'invalid common_name'

        with self.assertRaises(ValueError):
            org.email = 'cms@yamoneyru'

    def test_organization_validate(self):
        org = Organization()

        with self.assertRaises(ValueError):
            org.validate()

        org.country_name = 'RU'
        with self.assertRaises(ValueError):
            org.validate()

        org.state = 'Russia'
        with self.assertRaises(ValueError):
            org.validate()

        org.org_name = 'Yandex Money'
        with self.assertRaises(ValueError):
            org.validate()

        org.common_name = 'yamoney'
        with self.assertRaises(ValueError):
            org.validate()

        org.locality = ''
        org.org_unit_name = ''
        with self.assertRaises(ValueError):
            org.validate()

        org.org_name = None
        org.email = 'cms@yamoney.ru'
        with self.assertRaises(ValueError):
            org.validate()

        self.assertEqual(org.verify(), False)

        org.org_name = 'Yandex Money'
        self.assertEqual(org.verify(), True)
