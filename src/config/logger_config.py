import logging
from decouple import config

log_format = '[%(asctime)s][%(levelname)s] %(message)s'
log_level = config('LOG_LEVEL')

if log_level == 'debug':
    logging.basicConfig(level=logging.DEBUG,
                    format=log_format)
    logger = logging.getLogger(__name__)
elif log_level == 'info':
    logging.basicConfig(level=logging.INFO,
                    format=log_format)
    logger = logging.getLogger(__name__)
elif log_level == 'warning':
    logging.basicConfig(level=logging.WARNING,
                    format=log_format)
    logger = logging.getLogger(__name__)
elif log_level == 'error':
    logging.basicConfig(level=logging.ERROR,
                    format=log_format)
    logger = logging.getLogger(__name__)
elif log_level == 'critical':
    logging.basicConfig(level=logging.CRITICAL,
                    format=log_format)
    logger = logging.getLogger(__name__)

