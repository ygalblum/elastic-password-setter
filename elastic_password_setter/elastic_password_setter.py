import logging
import os

from elasticsearch import Elasticsearch
from injector import inject, singleton

from settings import Settings


built_in_users = [
    'kibana_system',
    'logstash_system',
    'beats_system',
    'apm_system',
    'remote_monitoring_user'
]

logger = logging.getLogger(__name__)


class ElasticPasswordSetterException(Exception):
    pass


@singleton
class ElasticPasswordSetter():

    @inject
    def __init__(self, settings: Settings) -> None:
        self._elastic_host = settings.elastic.host
        self._elastic_user = settings.elastic.user
        self._ca_certs = settings.elastic.ca_certs

    def run(self):
        client = self._get_client()
        for username in built_in_users:
            password = self._get_password_from_env(username)
            if not password:
                logger.info("Password was not provided for user %s", username)
                continue
            client.security.change_password(username=username, password=password)
            logger.info("Password for username %s was successfully set", username)

    def _get_client(self):
        elastic_password = self._get_password_from_env(self._elastic_user)
        if not elastic_password:
            raise ElasticPasswordSetterException("The password for the user 'elastic' was not provided")

        client_args = {
            "hosts": f"https://{self._elastic_host}",
            "basic_auth": (self._elastic_user, elastic_password),
        }
        if self._ca_certs:
            client_args['ca_certs'] = self._ca_certs
        return Elasticsearch(**client_args)


    @staticmethod
    def _get_password_from_env(username: str):
        return os.environ.get(f"{username.upper()}_PASSWORD")
