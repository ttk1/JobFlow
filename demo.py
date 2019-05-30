#!/bin/python3
# coding:utf-8

from logging import INFO, basicConfig

from jobflow.job import Job, task


class Demo(Job):
    count = 0

    def __init__(self):
        super().__init__('DEMO')

    @task('タスク1')
    def task1(self):
        self.info('success!')

    @task('タスク2', retry_count=5, retry_interval_ms=1000)
    def task2(self):
        raise Exception('謎のエラー')

    @task('タスク3')
    def task3(self):
        self.info('これは実行されない')

    def process(self):
        self.task1()
        self.task2()
        self.task3()


if __name__ == '__main__':
    fmt = '%(asctime)s [%(levelname)s] [%(name)s] - %(message)s'
    basicConfig(level=INFO, format=fmt)
    Demo().execute()
