import os

filename = r"Mango1905.log"  # 需要进行分割的文件
size = 80000000  # 分割大小10M


def createSubFile(srcName, sub, buf):
    [des_filename, extname] = os.path.splitext(srcName)
    filename = des_filename + '_' + str(sub) + extname
    print('正在生成子文件: %s' % filename)
    with open(filename, 'wb') as fout:
        fout.write(buf)
        return sub + 1


def cutFile(filename, size):
    with open(filename, 'rb') as fin:
        buf = fin.read(size)
        sub = 1
        while len(buf) > 0:
            sub = createSubFile(filename, sub, buf)
            buf = fin.read(size)
    print("ok")


if __name__ == "__main__":
    cutFile(filename, size)
