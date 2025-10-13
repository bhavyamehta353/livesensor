from sensor.exception import SensorException
import sys
import os
from sensor.logger import logging

def test_exception():
    try:
        logging.info("Testing logging")
        a = 1/0
    except Exception as e:
        raise SensorException(e,sys)

if __name__ ==  "__main__":  # sets the module. Makes sure the variables of imported files are not confused with variables in this file
    try:
        test_exception()
    except Exception as e:
        print(e)
