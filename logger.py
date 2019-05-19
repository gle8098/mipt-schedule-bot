import logging


class Logger:
    _logger = logging.getLogger(__name__)

    @staticmethod
    def init():
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    @staticmethod
    def error(text, exception):
        Logger._logger.warning('Exception occured: %s', text)
        Logger._logger.warning('%s', exception)
