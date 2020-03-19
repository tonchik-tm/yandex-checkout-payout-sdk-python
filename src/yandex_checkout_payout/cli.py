# -*- coding: utf-8 -*-
import argparse
import sys
import yandex_checkout_payout
from yandex_checkout_payout.domain.common.cli_client import CliClient


def main():

    parser = argparse.ArgumentParser(
        description='Console script for yandex_checkout_payout.',
        epilog='Author: {}\nE-mail: {}\nVersion: {}'.format(yandex_checkout_payout.__author__,
                                                            yandex_checkout_payout.__email__,
                                                            yandex_checkout_payout.__version__)
    )

    parser.version = yandex_checkout_payout.__version__
    parser.add_argument('-a', action='append', choices=['generate'])
    parser.add_argument('-v', action='version')
    args = parser.parse_args()

    if args.a is not None:
        # var_dump(args.a)
        action = args.a[0]
        cli = CliClient()
        if action == 'generate':
            cli.generate()
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
