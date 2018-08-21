# -*- coding:utf-8 -*-
__author__ = 'youjia'
__date__ = '2018/8/3 17:14'
import threading
value1 = 0
value2 = 0
gLock = threading.Lock()  # 创建一个锁


# 使用全局变量是需要用global来定义，以下代码当value值循环+1到1000次，
# 定义两个线程打印出的结果是没问题的，当+到1000000次时，结果就会出错，
# 线程执行顺序是无序的，造成了数据错误，就需要锁机制
class CodingThread(threading.Thread):
    def run(self):
        global value1
        for x in range(1000000):
            value1 += 1
        print('no lock value1:', value1)


class LockCodingThread(threading.Thread):
    def run(self):
        global value2
        gLock.acquire()  # 上锁（只在修改了全局变量时上锁，访问就不需要）
        for x in range(1000000):
            value2 += 1
        gLock.release()  # 释放
        print('lock value2:', value2)


def main():
    for x in range(2):
        t1 = CodingThread()
        t2 = LockCodingThread()
        t1.start()
        t2.start()


if __name__ == '__main__':
    main()
