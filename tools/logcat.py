import os
import time
from tools.excecmd import run_sub
from concurrent.futures import ThreadPoolExecutor


class Logcat:

    @classmethod
    def __Logcat(cls, waitTime=10 * 60, logName=None):
        if not logName:
            logName = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())
        work_log = os.path.abspath('..')
        exceResult = os.popen("adb shell logcat -c")
        log_path = f"adb shell logcat -v time >{work_log}\log\logcat\{logName}.log"
        print(log_path)
        exceResult = os.popen(log_path)
        time.sleep(waitTime)
        cls.killProcess()

    @classmethod
    def killProcess(cls):
        exceResult = run_sub("adb shell ps -ef | findstr logcat")
        output = exceResult[0]
        for line in output.split('\n'):
            try:
                if line.split()[0] == 'shell':
                    logcat_pid = line.split()[1]
                    print(f'logcat_pid: {logcat_pid}')
                    run_sub(f"adb shell kill -9 {logcat_pid}")
                    break
                print(f'查询logcat: {exceResult}')
            except IndexError:
                pass

    @classmethod
    def getLogcat(cls, count: int) -> bool:
        for _ in range(count):
            cls.__Logcat(waitTime=1 * 60 * 60)
            time.sleep(10)
        return True


if __name__ == '__main__':
    Logcat.getLogcat(10)
