import os
import logging


class Config:
    smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('SMTP_PORT', 587))
    use_starttls = os.environ.get('USE_STARTTLS', True)
    smtp_username = os.environ.get('SMTP_USERNAME')
    smtp_password = os.environ.get('SMTP_PASSWORD')
    from_email = os.environ.get('FROM_EMAIL', smtp_username)
    debug = os.environ.get('DEBUG', True)
    log_level = os.environ.get('LOG_LEVEL', 'INFO')
    debug = True if log_level == 'DEBUG' else False


# create application logger
log = logging.getLogger()
log.setLevel(Config.log_level)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(Config.log_level)
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
log.addHandler(ch)
