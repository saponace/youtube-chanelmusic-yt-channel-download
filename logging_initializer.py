import os
import json
import logging.config


class loggingInitializer(object):
    """
    Initialize a logger
    """

    @staticmethod
    def setup_logging(
            path='logging.json',
            default_level=logging.INFO,
    ):
        """
        Setup the logging configuration
        :param path: Path to the logging configuration file
        :param default_level: The default logging level if the config file
        is not found
        """
        if os.path.exists(path):
            with open(path, 'rt') as f:
                config = json.load(f)
            logging.config.dictConfig(config)
        else:
            logging.basicConfig(level=default_level)


