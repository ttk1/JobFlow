#!/bin/python3
# coding:utf-8

from logging import INFO, basicConfig

from jobflow.job import Job, task


class Demo(Job):
    count = 0

    def __init__(self):
        super().__init__('DEMO')

    @task('タスク1')
    def task1(self, **kwargs):
        msg = kwargs.get('message', 'NO_MESSAGE')
        self.info(msg)

    @task('タスク2', retry_count=3, retry_interval_ms=1000)
    def task2(self):
        if self.count < 3:
            self.count += 1
            self.warning('エラーが起きても指定した回数リトライ')
            raise Exception('謎のエラー')
        self.info('SUCCESS')

    @task('タスク3')
    def task3(self):
        try:
            self.critical('ここでジョブがコケる')
            raise FatalError('致命的なエラー')
        except FatalError as e:
            # 致命的なエラーが起きたらジョブを即座に失敗させる
            self.fail(e)

    def process(self):
        self.task1(message='何かのメッセージ')
        self.task2()
        self.task3()


class FatalError(Exception):
    pass


if __name__ == '__main__':
    fmt = '%(asctime)s [%(levelname)s] [%(name)s] - %(message)s'
    basicConfig(level=INFO, format=fmt)
    Demo().execute()
