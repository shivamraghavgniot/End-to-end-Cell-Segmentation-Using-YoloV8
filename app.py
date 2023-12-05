import sys
from cellSegmentation.logger import logging
from cellSegmentation.exception import AppException
logging.info("WELCOME TO THE FIRST LOG")

try:
    a = 4/"6"

except Exception as e:
    logging.info(f'Exception {e} Occured')
    raise AppException(e,sys)