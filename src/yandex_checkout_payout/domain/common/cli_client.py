# -*- coding: utf-8 -*-
import os
from getpass import getpass
from os.path import abspath

from yandex_checkout_payout.domain.common.generator_csr import GeneratorCsr
from yandex_checkout_payout.domain.models.organization import Organization


class CliClient:

    org_fields = {
        'country_name': {'name': 'Country Name', 'hint': '2 letter code', 'req': True, 'default': 'RU', },
        'state': {'name': 'State or Province Name', 'hint': 'full name', 'req': True, 'default': 'Russia', },
        'locality': {'name': 'Locality Name', 'hint': 'eg, city', 'req': False, 'default': None, },
        'org_name': {'name': 'Organization Name', 'hint': 'eg, company', 'req': True, 'default': None, },
        'org_unit_name': {'name': 'Organizational Unit Name', 'hint': 'eg, section', 'req': False, 'default': None, },
        'common_name': {'name': 'Common Name', 'hint': 'eg, YOUR name', 'req': True, 'default': None, },
        'email': {'name': 'Email Address', 'hint': None, 'req': True, 'default': None, },
    }

    def generate(self):
        org = self.fill_org()
        output = self.fill_output()
        password = self.fill_password()
        self.print_data(org, output, password)
        self.run_generator(password, org, output)

    def print_data(self, org, output, password):
        ret = C.c(C.CYELLOW2, "\nYour data:\n")
        for name, item in self.org_fields.items():
            attr = getattr(org, name)
            ret += "{}: {}\n".format(item['name'], C.c(C.CRED2, '-') if attr == '' else C.c(C.CGREEN2, attr))
        ret += "Output dir: {}\n".format(C.c(C.CGREEN2, output))
        ret += "Password for privateKey: {}\n".format(C.c(C.CGREEN2, "*".ljust(len(password), '*')))
        print(ret)

    def fill_org(self):
        org = Organization()
        for name, item in self.org_fields.items():
            successful = False
            while not successful:
                prompt = "Type {}{} [{}{}]: ".format(
                    item['name'],
                    '' if item['hint'] is None else " (" + item['hint'] + ")",
                    '' if item['default'] is None else str(item['default']),
                    '' if not item['req'] else C.c(C.CRED2, '*'),
                )
                print(prompt)

                while True:
                    val = input()
                    if item['default'] and not val:
                        val = item['default']

                    if item['req'] and not val:
                        print(C.c(C.CRED2, "Error. {} cannot be empty!".format(item['name'])))
                        print(prompt)
                    else:
                        break

                if item['default'] and not val:
                    val = item['default']

                try:
                    setattr(org, name, val)
                    successful = True
                except ValueError as e:
                    print(C.c(C.CRED2, "Error. {}".format(str(e))))

        return org

    def fill_output(self):
        default = os.getcwd()
        prompt = "Type output dir for privateKey and request.csr [{}]: ".format(default)
        print(prompt)
        val = input()

        return default if not val else str(val)

    def fill_password(self):
        prompt = "Type password for privateKey {}: ".format(C.c(C.CRED2, '*'))
        print(prompt)
        while True:
            val = getpass()
            if not val:
                print(C.c(C.CRED2, "Error. Password cannot be empty!"))
                print(prompt)
            else:
                break

        return str(val)

    def run_generator(self, password, org, output):
        default = "no"
        prompt = "Are you ready to generate files? (yes|no) [{}]: ".format(default)
        print(prompt)
        val = input()

        if val == 'yes':
            gen = GeneratorCsr(password, org, abspath(output))
            gen.generate_all()

            print(C.c(C.CYELLOW2, "\nGenerating is done!:"))
            for ftype, fdata in gen.get_file_list().items():
                print("{}: {}".format(ftype, C.c(C.CGREEN2 if fdata['exist'] else C.CRED2, fdata['path'])))
        else:
            print(C.c(C.CRED2, "You cancelled generating!"))


class C:

    CEND = '\33[0m'
    CBOLD = '\33[1m'
    CITALIC = '\33[3m'
    CURL = '\33[4m'
    CBLINK = '\33[5m'
    CBLINK2 = '\33[6m'
    CSELECTED = '\33[7m'

    CBLACK = '\33[30m'
    CRED = '\33[31m'
    CGREEN = '\33[32m'
    CYELLOW = '\33[33m'
    CBLUE = '\33[34m'
    CVIOLET = '\33[35m'
    CBEIGE = '\33[36m'
    CWHITE = '\33[37m'

    CBLACKBG = '\33[40m'
    CREDBG = '\33[41m'
    CGREENBG = '\33[42m'
    CYELLOWBG = '\33[43m'
    CBLUEBG = '\33[44m'
    CVIOLETBG = '\33[45m'
    CBEIGEBG = '\33[46m'
    CWHITEBG = '\33[47m'

    CGREY = '\33[90m'
    CRED2 = '\33[91m'
    CGREEN2 = '\33[92m'
    CYELLOW2 = '\33[93m'
    CBLUE2 = '\33[94m'
    CVIOLET2 = '\33[95m'
    CBEIGE2 = '\33[96m'
    CWHITE2 = '\33[97m'

    CGREYBG = '\33[100m'
    CREDBG2 = '\33[101m'
    CGREENBG2 = '\33[102m'
    CYELLOWBG2 = '\33[103m'
    CBLUEBG2 = '\33[104m'
    CVIOLETBG2 = '\33[105m'
    CBEIGEBG2 = '\33[106m'
    CWHITEBG2 = '\33[107m'

    @staticmethod
    def c(color, text):
        return color + text + C.CEND
