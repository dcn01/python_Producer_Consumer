# -*- coding:utf-8 -*-
__author__ = 'youjia'
__date__ = '2018/8/3 17:41'
import threading
import random
import time
gMoney = 1000
gLock = threading.Lock()
gTotal = 10
gTimes = 0


class Producer(threading.Thread):
    def run(self):
        global gMoney
        global gTimes
        while True:
            money = random.randint(100, 1000)
            gLock.acquire()
            if gTimes >= gTotal:
                gLock.release()
                return
            gMoney += money
            gTimes += 1
            print('%s生产者生产了%d元，剩余金额%d元' % (threading.current_thread(), money, gMoney))
            gLock.release()
            time.sleep(1)


class Consumer(threading.Thread):
    def run(self):
        global gMoney
        while True:
            money = random.randint(100, 1000)
            gLock.acquire()
            if gMoney >= money:
                gMoney -= money
                print('%s消费者消费了%d元，剩余金额%d元' % (threading.current_thread(), money, gMoney))
            else:
                if gTimes >= gTotal:
                    gLock.release()
                    break
                print('%s消费者准备消费%d元，剩余金额%d元，不足！' % (threading.current_thread(), money, gMoney))
            gLock.release()
            time.sleep(1)


def main():
    for x in range(3):  # 3个消费者
        t = Consumer(name='消费者线程%d' % x)
        t.start()

    for x in range(5):  # 5个生产者
        t = Producer(name='生产者线程%d' % x)
        t.start()


if __name__ == '__main__':
    main()
