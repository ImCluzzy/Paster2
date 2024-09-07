import logging
import os

def loging():
    if not os.path.exists('logs'):
        os.makedirs('logs')

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    error_handler = logging.FileHandler('logs/errors.log', mode='a')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    info_warning_handler = logging.FileHandler('logs/lasted.log', mode='a')
    info_warning_handler.setLevel(logging.INFO)
    info_warning_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(error_handler)
    logger.addHandler(info_warning_handler)

    return logger