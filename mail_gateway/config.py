import os
import logging


smtp_server = os.environ.get('SMTP_SERVER', '10.8.0.5')
smtp_port = int(os.environ.get('SMTP_PORT', 25))
from_email = os.environ.get('FROM_EMAIL', 'duabi.lab.demo@gmail.com')
debug = os.environ.get('DEBUG', True)
log_level = os.environ.get('LOG_LEVEL', 'INFO')
debug = True if log_level == 'DEBUG' else False


# create application logger
log = logging.getLogger()
log.setLevel(log_level)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(log_level)
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
log.addHandler(ch)
