#!/bin/python3
# coding:utf-8

from logging import INFO, basicConfig

from jobflow.job import Job


class Demo(Job):
    count = 0

    def __init__(self):
        super().__init__('DEMO')

    def task1(self):
        self.info('success!')

    def task2(self):
        self.critical('ここでジョブがコケる')
        self.fail()

    def task3(self):
        self.info('これは実行されない')

    def process(self):
        self.executeTask(self.task1, 'タスク1')
        self.executeTask(self.task2, 'タスク2')
        self.executeTask(self.task3, 'タスク3')


def init():
    fmt = '%(asctime)s [%(levelname)s] [%(name)s] - %(message)s'
    basicConfig(level=INFO, format=fmt)


if __name__ == "__main__":
    init()
    Demo().execute()
