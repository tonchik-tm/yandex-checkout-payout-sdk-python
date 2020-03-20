# -*- coding: utf-8 -*-
import logging
import os

from yandex_checkout_payout.domain.common.keychain import KeyChain


class ConfigurationError(Exception):
    pass


class Configuration:
    """
    A class representing the configuration.
    """
    api_url = "https://calypso.yamoney.ru:9094/"
    synonym_card_url = "https://paymentcard.yamoney.ru/"
    agent_id = None
    keychain = None
    logger = None
    timeout = 1800
    max_attempts = 3
    yandex_cert = os.path.dirname(os.path.abspath(__file__)) + '/artefacts/deposit.cer'

    def __init__(self, **kwargs):
        self.assert_has_api_credentials()

    @staticmethod
    def configure(agent_id, keychain, logger=None, **kwargs):
        Configuration.agent_id = agent_id
        Configuration.keychain = keychain
        Configuration.timeout = kwargs.get("timeout", 1800)
        Configuration.max_attempts = kwargs.get("max_attempts", 3)
        Configuration.configure_logger(logger)

    @staticmethod
    def configure_keychain(keychain):
        if not isinstance(keychain, KeyChain):
            raise ValueError('Invalid keychain type')
        Configuration.logger = keychain

    @staticmethod
    def configure_logger(logger):
        if isinstance(logger, logging.Logger):
            Configuration.logger = logger

    @staticmethod
    def instantiate():
        return Configuration(
            agent_id=Configuration.agent_id,
            keychain=Configuration.keychain,
            timeout=Configuration.timeout,
            max_attempts=Configuration.max_attempts
        )

    @staticmethod
    def api_endpoint(is_ssl=True):
        if is_ssl:
            return Configuration.api_url
        else:
            return Configuration.synonym_card_url

    def has_api_credentials(self):
        return self.agent_id is not None and self.keychain is not None

    def assert_has_api_credentials(self):
        if not self.has_api_credentials():
            raise ConfigurationError("agent_id and keychain are required")
