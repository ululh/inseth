import logging
def logging_config():
    FORMAT = '%(levelname)s %(asctime)s %(filename)s : %(message)s'
    logging.basicConfig(format = FORMAT, level=logging.INFO)
