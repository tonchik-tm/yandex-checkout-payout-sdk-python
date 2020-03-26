# -*- coding: utf-8 -*-
import logging
import logging.config
import sys
import unittest

from yandex_checkout_payout.configuration import Configuration, ConfigurationError
from yandex_checkout_payout.domain.common.keychain import KeyChain


class TestConfiguration(unittest.TestCase):

    def test_configuration(self):
        # logging.config.fileConfig(Configuration.base_config)
        logging.config.dictConfig({
            "version": 1,
            "handlers": {
                "streamHandler": {
                    "class": "logging.StreamHandler",
                    "formatter": "myFormatter",
                    "stream": sys.stdout
                },
                "fileHandler": {
                    "class": "logging.FileHandler",
                    "formatter": "myFormatter",
                    "filename": "config.log"
                }
            },
            "loggers": {
                "app": {
                    "handlers": ["fileHandler"],
                    "level": "DEBUG",
                }
            },
            "formatters": {
                "myFormatter": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                }
            }
        })

        log = logging.getLogger('app')
        keychain = KeyChain('public_cert', 'private_key', 'key_password')
        Configuration.configure(250000, keychain, log)
        configuration = Configuration.instantiate()

        self.assertEqual(configuration.agent_id, 250000)
        self.assertEqual(configuration.timeout, 1800)
        self.assertEqual(configuration.max_attempts, 3)
        # var_dump(dict(configuration))
        self.assertIsInstance(configuration.logger, logging.Logger)
