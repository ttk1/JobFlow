#!/bin/python3
# coding:utf-8

import time
import traceback
from logging import getLogger


class Job:
    def __init__(self, name):
        self.name = name
        self.logger = getLogger(name)

    def process(self):
        raise NotImplementedError

    def execute(self):
        self.logger.info('ジョブを開始します.')
        self.process()
        self.logger.info('ジョブが正常終了しました.')

    def executeTask(self, task, task_name, retry_count=0, retry_interval_ms=5000):
        self.logger.info('%s を開始します.', task_name)

        count = 0
        while count <= retry_count:
            count += 1
            try:
                self.logger.info('(%s) %s回目の試行中...', task_name, count)
                task()
            except:
                self.logger.warning('(%s) 試行失敗', task_name)
                traceback.print_exc()
                time.sleep(retry_interval_ms / 1000.0)
            else:
                self.logger.info('%s が正常終了しました.', task_name)
                return

        self.logger.critical('%s のリトライ回数が上限に達しました.', task_name)
        raise TaskExecutionError('タスクのリトライ回数が上限に達しました.')


class TaskExecutionError(Exception):
    pass
