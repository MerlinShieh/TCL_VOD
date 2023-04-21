import sys
import os
from tools import _log

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


BASE_LIB_SCRCPY = os.path.join(BASE_DIR, 'lib', 'scrcpy')
BASE_LIB_ADB = os.path.join(BASE_DIR, 'lib', 'adb')

sys.path.append(BASE_DIR)
sys.path.append(BASE_LIB_SCRCPY)
sys.path.append(BASE_LIB_ADB)

log = _log.log
logger = _log.logger
