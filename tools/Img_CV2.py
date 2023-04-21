import cv2
import numpy as np


# 原文：https://www.cnblogs.com/dcb3688/p/4610660.html


# 均值哈希算法
# 均值哈希算法
def aHash(img):
    # 缩放为8*8
    img = cv2.resize(img, (8, 8), interpolation=cv2.INTER_CUBIC)
    # 转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # s为像素和初值为0，hash_str为hash值初值为''
    s = 0
    hash_str = ''
    # 遍历累加求像素和
    for i in range(8):
        for j in range(8):
            s = s + gray[i, j]
    # 求平均灰度
    avg = s / 64
    # 灰度大于平均值为1相反为0生成图片的hash值
    for i in range(8):
        for j in range(8):
            if gray[i, j] > avg:
                hash_str = hash_str + '1'
            else:
                hash_str = hash_str + '0'
    return hash_str


if __name__ == '__main__':
    i = r'0.jpg'
    img = cv2.imread(i)
    print(aHash(img))
    i = r'1.jpg'
    img = cv2.imread(i)
    print(aHash(img))

    # i = r'3.jpg'
    # img = cv2.imread(i)
    # print(aHash(img))