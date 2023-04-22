import os
import subprocess as sub
import sys
import threading
import time
import ctypes
import inspect
import serial
from tools import _log, logger, BASE_DIR, BASE_LIB_SCRCPY, BASE_LIB_ADB


def run_sub(cmd: str):
    output = sub.Popen(
        cmd, stdout=sub.PIPE, stderr=sub.PIPE, stdin=sub.PIPE, shell=True
    )
    data, err = output.communicate()

    if data.decode('utf-8'):
        return data.decode('utf-8'), True
    else:
        return err.decode('utf-8'), False


def __task_scrcpy(serial=None, title='scrcpy_Android', size='1400:3200:0:0', m=2048, b='4M', isSave=False):
    if isSave:
        cmdstr = f"{os.path.join(BASE_DIR, 'lib/scrcpy/scrcpy.exe')} " \
                 f"--crop={size} --window-title {title} -m {m} -b {b} --record {os.path.join(BASE_DIR, 'MP4', title)}.mp4"
    else:
        cmdstr = f"{os.path.join(BASE_DIR, 'lib/scrcpy/scrcpy.exe')} --crop={size} --window-title {title} -m {m} -b {b}"
    run_sub(cmdstr)  # 打开scrcpy
    time.sleep(3)


def theardScrcpy(serial=None, title='scrcpy_Android', size='1400:3200:0:0', m=2048, b='4M', isSave=False):
    t = threading.Thread(target=__task_scrcpy, args=[serial, title, size, m, b, isSave])
    # 设置为守护线程，主线程结束时守护线程随之结束
    # t.daemon = True
    t.start()
    return t


def run_ser():
    return serial.Serial('COM6', 115200, timeout=0.5)


if __name__ == '__main__':
    # cmd = b"""am start -n com.tcl.vod/.videosort.TVBSortActivity --es channe_name "yueshitong" --es channe_id "62d906228e33a32304ca8f25"  --ei vendorId 332"""
    # output = sub.Popen(
    #     'adb devices', stdout=sub.PIPE, stderr=sub.PIPE, stdin=sub.PIPE, shell=True
    # )
    # data, err = output.communicate()
    # print((data.decode('utf-8').split('\n')))
    #
    # ser = run_ser()
    # print(ser.isOpen())
    # ser.write(cmd)
    # ser.flush()
    #
    # print(ser.read(ser.in_waiting))
    theardScrcpy()
