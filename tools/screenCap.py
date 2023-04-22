r"""
两种截图方式
一种是采用adb多线程截图，比较稳定，但是比较慢
一种通过scrcpy工具对Android设备进行投屏，采用的pyqt5对投屏窗口进行截图
"""
import os
import os.path
import sys
import threading
import time

import win32gui
from PyQt5.QtWidgets import QApplication

from tools import BASE_DIR, log, logger
from tools import excecmd


@logger('进行截图操作')
def __task(_path, _count=str(int(time.time()))):
    excecmd.run_sub(f'adb shell screencap -p /sdcard/tmp.jpg')
    excecmd.run_sub(f'adb pull /sdcard/tmp.jpg {_path}/{_count}.jpg')
    # return f"{_path}/{_count}.jpg"
    log.debug(f'截图成功, 路径 {_path}/{_count}.jpg')
    return os.path.join(_path, f'{_count}.jpg')


@logger('adb多线程方式进行截图')
def ADBtheardSrceenCap(_path, _count):
    t = threading.Thread(target=__task, args=[_path, _count])
    # 设置为守护线程，主线程结束时守护线程随之结束
    t.daemon = True
    t.start()
    return True


hwnd_title = dict()


def __get_all_hwnd(hwnd, mouse=0):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})


win32gui.EnumWindows(__get_all_hwnd, 0)


def Win32src(hwndTitle, path=r'screencap', imgName=str(int(time.time()))):
    log.info('窗口为{}， 保存路径为{}， 图片名称为{}', hwndTitle, path, imgName)
    win32gui.EnumWindows(__get_all_hwnd, 0)
    hwnd = win32gui.FindWindow(None, hwndTitle)
    app = QApplication(sys.argv)
    screen = QApplication.primaryScreen()
    img = screen.grabWindow(hwnd).toImage()
    _img_path = os.path.join(BASE_DIR, path, hwndTitle + '_' + imgName + '.jpg')
    # _img_path = os.path.join(BASE_DIR, path, imgName + '.jpg')
    log.info('保存图片 {}', _img_path)
    img.save(_img_path)
    return _img_path


@logger('获取所有的窗口句柄')
def hwnd_title_list() -> dict:
    win32gui.EnumWindows(__get_all_hwnd, 0)
    _dict = {}
    for h, t in hwnd_title.items():
        if t != "":
            _dict[str(h)] = t
    return _dict


if __name__ == '__main__':
    from pprint import pprint

    pprint(hwnd_title_list())
    Win32src(r'原神')

    # _path = os.path.join(BASE_DIR, 'screencap')
    # _count = 1
    # ADBtheardSrceenCap(_path, _count)
