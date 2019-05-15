#!/bin/python3
# coding:utf-8

from logging import INFO, basicConfig

from jobflow.job import Job


class Demo(Job):
    count = 0

    def __init__(self):
        super().__init__('DEMO')

    def task1(self):
        if self.count < 3:
            self.count += 1
            raise Exception('エラー')
        print('success!')

    def task2(self):
        print('skip!')
        self.skip()

    def task3(self):
        print('これは実行されない')

    def process(self):
        self.executeTask(self.task1, 'タスク1', retry_count=5,
                         retry_interval_ms=1000)
        self.executeTask(self.task2, 'タスク2')
        self.executeTask(self.task3, 'タスク3')


def init():
    fmt = "%(asctime)s [%(levelname)s] [%(name)s] - %(message)s"
    basicConfig(level=INFO, format=fmt)


if __name__ == "__main__":
    init()
    Demo().execute()
