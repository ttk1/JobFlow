#!/bin/python3
# coding:utf-8

import time
import traceback
from logging import getLogger


class Job:
    def __init__(self, name):
        self.__logger = getLogger(name)
        self.__name = name
        self.__current_task_name = None
        self.__skipped = False

    def critical(self, message, *args):
        if self.__current_task_name:
            message = '(%s) ' + message
            args = (self.__current_task_name,) + args
        self.__logger.critical(message, *args)

    def warning(self, message, *args):
        if self.__current_task_name:
            message = '(%s) ' + message
            args = (self.__current_task_name,) + args
        self.__logger.warning(message, *args)

    def info(self, message, *args):
        if self.__current_task_name:
            message = '(%s) ' + message
            args = (self.__current_task_name,) + args
        self.__logger.info(message, *args)

    def skip(self):
        self.info('残りのタスクをスキップします.')
        self.__skipped = True

    @staticmethod
    def fail(*message):
        raise JobExecutionError(*message)

    def process(self):
        raise NotImplementedError

    def execute(self):
        self.info('ジョブを開始します.')
        self.process()
        self.info('ジョブが正常終了しました.')

    def executeTask(self, task_func, task_name, retry_count=0, retry_interval_ms=5000):
        if self.__skipped:
            return

        self.__current_task_name = task_name
        self.info('タスクを開始します.')

        count = 0
        while count <= retry_count:
            count += 1
            try:
                self.info('%s回目の試行中...', count)
                task_func()
            except JobExecutionError:
                self.critical('問題が発生したためジョブを緊急停止します.')
                raise
            except:
                self.warning('タスクが失敗しました.')
                self.warning(traceback.format_exc())
                time.sleep(retry_interval_ms / 1000.0)
            else:
                self.info('タスクが正常終了しました.')
                self.__current_task_name = None
                return

        self.critical('リトライ回数が上限に達しました.')
        self.__current_task_name = None
        raise JobExecutionError('タスクのリトライ回数が上限に達しました.')


class JobExecutionError(Exception):
    pass


def task(task_name, retry_count=0, retry_interval_ms=5000):
    def decorator(task_func):
        def wrapper(self, *args, **kwargs):
            self.executeTask(lambda: task_func(self, *args, **kwargs), task_name,
                             retry_count, retry_interval_ms)
        return wrapper
    return decorator
