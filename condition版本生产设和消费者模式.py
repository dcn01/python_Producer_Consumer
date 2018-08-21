# -*- coding:utf-8 -*-
__author__ = 'youjia'
__date__ = '2018/8/3 21:35'
import threading
import time
import random
gCondition = threading.Condition()
gMoney = 1000
gTotal = 10
gTimes = 0


class Producer(threading.Thread):
    def run(self):
        global gMoney
        global gTimes
        while True:
            gCondition.acquire()
            money = random.randint(100, 1000)
            if gTimes >= gTotal:
                gCondition.release()
                break
            gMoney += money
            gTimes += 1
            gCondition.notify_all()  # 步骤2
            print('%s生产者生产了%d元，剩余金额%d元' % (threading.current_thread(), money, gMoney))
            gCondition.release()
            time.sleep(1)


class Consumer(threading.Thread):
    def run(self):
        global gMoney
        while True:
            gCondition.acquire()
            money = random.randint(100, 1000)
            while gMoney < money:  # 步骤1
                if gTimes >= gTotal:
                    gCondition.release()
                    return
                print('%s消费者准备消费%d元，剩余金额%d元，不足！' % (threading.current_thread(), money, gMoney))
                gCondition.wait()
                # 如果余额不足了就在这里等待，不会去执行while True循环，直到生产者中产的余额足够了
                # 步骤2 gCondition.notify_all()就会通知，苏醒后继续排队去获取锁，继续执行步骤1，如果还不满足就继续等待，反之则
                # 向下继续执行代码
            gMoney -= money
            print('%s消费者消费了%d元，剩余金额%d元' % (threading.current_thread(), money, gMoney))
            gCondition.release()
            time.sleep(1)


def main():
    for x in range(3):
        t = Consumer(name='消费者线程%d' % x)
        t.start()

    for x in range(5):
        t = Producer(name='生产者线程%d' % x)
        t.start()


if __name__ == '__main__':
    main()
