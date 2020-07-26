import datetime
import logging
import sys
import warnings

APPNAME = 'weblogicscanner'
LOG_LEVEL = logging.INFO

logger = logging.getLogger(APPNAME)

formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s', datefmt='%H:%M:%S')
# 文件日志
file_handler = logging.FileHandler('%s_%s.log' % (APPNAME, datetime.datetime.now().strftime('%Y%m%d')),
                                   encoding='utf-8')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# 控制台日志
console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = formatter
logger.addHandler(console_handler)

logger.setLevel(LOG_LEVEL)

warnings.filterwarnings('ignore')
# fix: next warn
# C:\weblogicScanner\venv\lib\site-packages\urllib3\connectionpool.py:1004: InsecureRequestWarning: Unverified HTTPS request is being made to host 'localhost'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
#   InsecureRequestWarning,
