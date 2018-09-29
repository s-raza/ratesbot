import colorlog
import logging

formatter = colorlog.ColoredFormatter(
    "%(asctime)s %(log_color)s%(levelname)-8s %(name)s %(funcName)s()-%(lineno)s %(reset)s %(message)s",
    datefmt='%d%b%y %I:%M:%S%p',
    reset=True,
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'white,bg_red',
        'ERROR':    'red',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%'
)

logger = colorlog.getLogger()

handler = colorlog.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)


##Root logger logging level
logger.setLevel(logging.DEBUG)


