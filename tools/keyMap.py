from tools.excecmd import run_sub
from time import sleep
from tools import log, logger, BASE_DIR


class Key:
    __UP = "adb shell input keyevent 19"
    __DOWN = "adb shell input keyevent 20"
    __LEFT = "adb shell input keyevent 21"
    __RIGHT = "adb shell input keyevent 22"
    __ENTER = "adb shell input keyevent 23"
    __BACK = "adb shell input keyevent 4"

    @classmethod
    def up(cls):
        sleep(1)
        run_sub(cls.__UP)

    @classmethod
    def down(cls):
        sleep(1)
        run_sub(cls.__DOWN)

    @classmethod
    def left(cls):
        sleep(1)
        run_sub(cls.__LEFT)

    @classmethod
    def right(cls):
        sleep(1)
        run_sub(cls.__RIGHT)

    @classmethod
    def enter(cls):
        sleep(1)
        run_sub(cls.__ENTER)

    @classmethod
    def back(cls):
        sleep(1)
        run_sub(cls.__BACK)


if __name__ == '__main__':
    Key.enter()
