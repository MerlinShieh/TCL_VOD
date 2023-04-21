from genScript import APP
from case import Device
from concurrent.futures import ThreadPoolExecutor
from tools.logcat import Logcat
import time

if __name__ == '__main__':
    EXECUTOR = ThreadPoolExecutor(max_workers=4)
    # 初始化4个线程

    LoopTime = 10 * 60 * 60
    # 定义循环时间

    LogTime = 1 * 60
    # 定义每次日志的获取时间间隔

    dev = Device()
    # task1 = EXECUTOR.submit(dev.case__loopPlay, (dev.MangguoActivity, LoopTime))
    # task2 = EXECUTOR.submit(Logcat.getLogcat, LogTime)
    # dev.case__loopPlay(activity=dev.MangguoActivity, loopTime=LoopTime)
    dev.case__loopPlay(activity=dev.LeshiActivity, loopTime=LoopTime)
