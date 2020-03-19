"""Console script for yandex_checkout_payout."""
import argparse
import sys

from var_dump import var_dump

# from yandex_checkout_payout.yandex_checkout_payout import YandexCheckoutPayout
import yandex_checkout_payout
from yandex_checkout_payout.domain.common.cli_client import CliClient, C


def main():

    parser = argparse.ArgumentParser(
        description='Console script for yandex_checkout_payout.',
        epilog='Author: {}\nE-mail: {}\nVersion: {}'.format(yandex_checkout_payout.__author__,
                                                            yandex_checkout_payout.__email__,
                                                            yandex_checkout_payout.__version__)
    )
    # parser.add_argument('_', nargs='*')
    parser.version = yandex_checkout_payout.__version__
    # parser.add_argument('generate')
    parser.add_argument('-a', action='append', choices=['generate', 'balance', 'test'])
    # parser.add_argument('-p', action='store')
    # parser.add_argument('-a', action='store')
    # parser.add_argument('-b', action='store_const', const=42)
    # parser.add_argument('-c', action='store_true')
    # parser.add_argument('-d', action='store_false')
    # parser.add_argument('-e', action='append')
    # parser.add_argument('-f', action='append_const', const=42)
    # parser.add_argument('-g', action='count')
    # parser.add_argument('-h', action='help')
    parser.add_argument('-v', action='version')
    args = parser.parse_args()

    # print("Arguments: " + str(args.a))
    # calling functions depending on type of argument
    if args.a is not None:
        # var_dump(args.a)
        action = args.a[0]
        cli = CliClient()
        if action == 'generate':
            cli.generate(args)
        elif action == 'balance':
            cli.balance(args)
        elif action == 'test':
            cli.test(args)
        return 0

    parser.print_help()

    # print("There are several actions that are already defined and ready to be used. Let’s analyze them in detail:\n"
    #       "store        - stores the input value to the Namespace object. (This is the default action.)\n"
    #       "store_const  - stores a constant value when the corresponding optional arguments are specified.\n"
    #       "store_true   - stores the Boolean value True when the corresponding optional argument is specified and "
    #       "stores a False elsewhere.\n"
    #       "store_false  - stores the Boolean value False when the corresponding optional argument is specified and "
    #       "stores True elsewhere.\n"
    #       "append       - stores a list, appending a value to the list each time the option is provided.\n"
    #       "append_const - stores a list appending a constant value to the list each time the option is provided.\n"
    #       "count        - stores an int that is equal to the times the option has been provided.\n"
    #       "help         - shows a help text and exits.\n"
    #       "version      - shows the version of the program and exits.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
