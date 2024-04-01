""" Elastic password setter """
import logging
import sys

from di import global_injector
from elastic_password_setter import ElasticPasswordSetter

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
global_injector.get(ElasticPasswordSetter).run()
