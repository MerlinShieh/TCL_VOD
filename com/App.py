import platform
import pandas as pd
import os
import time
import re
from tools import excecmd
import traceback
import random
from tools import log, logger, BASE_DIR
from tools.excecmd import run_sub
from tools.screenCap import ADBtheardSrceenCap, Win32src


class APP:
    def __init__(self, packagename='com.tcl.vod'):
        """
        :param packagename: 指的需要测试的app的包名，默认为com.tcl.vod
        """
        self.LiyuanxingActivity = ''

        self.MangguoActivity = ''

        self.LeshiActivity = ''

        self.YueshitongActivity = ''

        self.YijiulingwuActivity = ''

        self.SouhuActivity = ''
        self.packagename = packagename
        self.pidList = self.pid()
        self.scrcpy_title = self.packagename

    @logger(__name__)
    def pid(self) -> list:
        cmd = 'adb shell ps -A | findstr {}'.format(self.packagename)
        pidList = []
        exceResult = excecmd.run_sub(cmd)
        log.debug(f"exceResult: {exceResult}")
        output = exceResult[0]
        try:
            for line in output.split('\n'):
                if len(line.split()):
                    pidList.append(int(line.split()[1]))
            log.debug(f"pidList: {pidList}")
            return pidList
        except IndexError:
            log.debug('获取应用pid异常，可能是应用被kill')
            return []

    def meminfo(self) -> int:
        cmd = "adb shell dumpsys meminfo {} | findstr TOTAL".format(self.packagename)
        exceResult = excecmd.run_sub(cmd)
        log.debug("exccmd {}, excresult {}".format(cmd, exceResult))
        if exceResult[1]:
            str_reult = exceResult[0].replace('\t', '').replace('\r', '').replace('\n', '')

            # 部分Android设备获取meminfo方式不同，采用三元方式进行选择
            re_str_1 = "(?<=L:\s).*?(?=\s*T)"
            re_str_2 = "(?<=S:\s).*?(?=\s*T)"
            memory = re.findall(re_str_1, str_reult) \
                if re_str_2 == "(?<=S:\s).*?(?=\s*T)" == [] else re.findall(
                re_str_2, str_reult)
            memory = int(memory[0].replace(' ', ''))
            log.info(f'memory: {memory}')
            return memory
        else:
            log.debug('获取应用数据异常，可能是进程被kill， 应用pid: {}', self.pid())
            log.debug('默认返回数据为0')
            return 0
            # log.error(exceResult)
            # raise Exception

    def iow(self) -> int:
        cmd = "adb shell top -m 1 -n 1 | findstr iow"
        exceResult = excecmd.run_sub(cmd)
        if exceResult[1]:
            log.debug(f"excResult: {exceResult}")
            str_reult = exceResult[0].replace('\t', '').replace('\r', '').replace('\n', '')
            re_str = "(?<=%idle\s).*?(?=\s*%iow)"
            iow = re.findall(re_str, str_reult)
            iow = int(iow[0].replace(' ', ''))
            log.info(f'iow: {iow}')
            return iow
        else:
            log.debug('获取应用数据异常，可能是进程被kill， 应用pid: {}', self.pid())
            log.debug('默认返回数据为0')
            return 0

    # def flash(self) -> int:
    #     cmd = f"adb shell du -m -s /data/data/{self.packagename}"
    #     exceResult = excecmd.run_sub(cmd)
    #     if exceResult[1]:
    #         log.debug(f"excResult: {exceResult}")
    #         str_reult = exceResult[0].replace('\t', '').replace('\r', '').replace('\n', '')
    #         re_str = "(?<=%idle\s).*?(?=\s*%iow)"
    #         iow = re.findall(re_str, str_reult)
    #         iow = int(iow[0].replace(' ', ''))
    #         log.info(f'iow: {iow}')
    #         return iow
    #     else:
    #         log.debug('获取应用数据异常，可能是进程被kill， 应用pid: {}', self.pid())
    #         log.debug('默认返回数据为0')
    #         return 0

    def cpu(self) -> float:
        """获取cpu"""
        cpu = []
        if 'Windows' in platform.system():
            cmd = f"adb shell top -b -d 1 -n 1 -m 1000 -s 6 -o PID,%CPU,ARGS|findstr {self.packagename}"
        else:
            cmd = f"adb shell top -b -d 1 -n 1 -m 1000 -s 6 -o PID,%CPU,ARGS|grep {self.packagename}"
        exceResult = excecmd.run_sub(cmd)
        log.debug(f"excResult: {exceResult}")
        if exceResult[1]:
            str_reult = exceResult[0].replace('\t', '').replace('\r', '').replace('\n', '')
            re_str = f"(?<=\d\s.).*?(?=\s{self.packagename})"
            cpu = re.findall(re_str, str_reult)
            cpu = float(cpu[0].replace(' ', ''))
            log.info(f'cpu: {cpu}')
            return cpu
        else:
            log.debug('获取应用数据异常，可能是进程被kill， 应用pid: {}', self.pid())
            log.debug('默认返回数据为0')
            return 0

    @staticmethod
    @logger(__name__)
    def getTime(_format='year'):
        """获取运行时间"""
        if _format.upper() == 'YEAR':
            return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        elif _format.upper() == 'DAYTIME':
            return time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())
        else:
            return time.strftime('%Y-%m-%d', time.localtime())

    @log.catch()
    @logger(__name__)
    def startActivity(self, activity=None):
        """
        :param activity: 默认调起芒果TV
        :return:
        """
        if activity:
            return run_sub(activity)
        else:
            return run_sub(self.MangguoActivity)

    @log.catch()
    @logger(__name__)
    def stopActivity(self, packagename='com.tcl.vod'):
        run_sub(f"adb shell am force-stop {packagename}")
        log.debug(f'终止{packagename}的所有进程')
        return True

    # @logger("获取性能数据")
    def exportGenData(self, runTime=10 * 60 * 60, waitTime=2):
        """
        :param runTime: 秒时长，就是运行多少个小时
        :waitTime: 执行间隔
        :return:
        """
        log.debug('runTime: {}', runTime)
        STARTTIME = time.time()
        _path = '../log/genData_{}.csv'.format(self.getTime('day'))
        _data = [("time", "memeinfo", "CPU", "IOW")]
        pd.DataFrame(data=_data).to_csv(_path, index=False, header=False, mode='a')
        log.debug('写入表头成功， {}', _path)
        # 写入表头
        while time.time() < STARTTIME + runTime:
            _TIME, _MEM, _CPU, _IOW = self.getTime(), self.meminfo(), self.cpu(), self.iow()
            _data = [(_TIME, _MEM, _CPU, _IOW)]
            # ADBtheardSrceenCap(os.path.join(BASE_DIR, 'screencap'), self.getTime("DAYTIME"))
            Win32src(self.scrcpy_title, imgName=self.getTime("DAYTIME"))
            _df = pd.DataFrame(data=_data)
            log.info('data: {}', _data)
            _df.to_csv(_path, index=False, header=False, mode='a')
            time.sleep(waitTime)
        return True


if __name__ == '__main__':
    a = APP(packagename='com.sankuai.meituan')
    # 启动投屏工具
    theardScrcpy = excecmd.theardScrcpy(title=a.scrcpy_title, isSave=False)
    # a = APP()
    try:
        a.exportGenData(runTime=1 * 60)
    except Exception as e:
        log.error(e)
    finally:
        run_sub("""taskkill /F /IM scrcpy.exe""")
