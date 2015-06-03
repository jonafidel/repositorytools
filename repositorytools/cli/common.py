from abc import ABCMeta, abstractmethod
import logging
import httplib as http_client
import sys

import repositorytools

logger = logging.getLogger(sys.argv[0])


def configure_logging(debug):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
        http_client.HTTPConnection.debuglevel = 1
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.INFO)
        requests_log.propagate = True
    else:
        logging.basicConfig(level=logging.INFO)


class CLI(object):
    """
    Base class for cli
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def _get_parser(self):
        """
        :return: argparse.ArgumentParser
        """
        pass

    def __init__(self):
        self.parser = self._get_parser()
        self.parser.add_argument("-D", "--debug", action="store_true", dest="debug", default=False,
                                 help="Print lots of debugging information")
        self.repository = repositorytools.repository_client_factory()

    def run(self, args=None):
        args_namespace = self.parser.parse_args(args)
        configure_logging(args_namespace.debug)
        # in tests we don't use 'str(sys.argv), so we can log actual arguments
        used_args = args or sys.argv[1:]
        logger.info('Started %s, with arguments %s', sys.argv[0], str(used_args))

        """
        This runs the function that is assigned to the sub-command by calling of set_defaults
        """
        return args_namespace.func(args_namespace)