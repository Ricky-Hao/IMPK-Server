import os
from Server.util.logger import logger
from Server.util.utils import *

script_path = os.path.abspath(__file__)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(script_path)))
KEY_ROOT = os.path.join(PROJECT_ROOT, 'key')
DB_ROOT = os.path.join(PROJECT_ROOT, 'db')

__all__ = ['PROJECT_ROOT', 'KEY_ROOT', 'DB_ROOT', 'logger', 'Alist', 'AsyncIter']