from sys import stderr
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] %(name)s: %(message)s',
    stream=stderr
)

logger = logging.getLogger('Server')
