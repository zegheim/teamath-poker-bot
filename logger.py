import logging

FORMAT = '%(asctime)s.%(msecs)03d %(levelname)-5s - %(message)s'
DATE_FORMAT = '%m/%d/%Y %H:%M:%S'

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

fmt_fh = logging.Formatter(FORMAT, DATE_FORMAT)
fh = logging.FileHandler('game.log', mode='w')
fh.setLevel(logging.DEBUG)
fh.setFormatter(fmt_fh)

logger.addHandler(fh)

