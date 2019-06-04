#!/bin/python3
# coidng: utf-8

from unittest import TestCase
from unittest.mock import call, patch, Mock

from jobflow.job import Job, JobExecutionError, task


class TestJob(TestCase):
    def test_logger_with_task_name(self):
        job = Job('job_name')
        job.logger = Mock()
        job.current_task_name = 'task_name'

        job.info('info: %s', 'arg')
        expected = [
            call('(%s) info: %s', 'task_name', 'arg')
        ]
        actual = job.logger.info.call_args_list
        self.assertEqual(expected, actual)

        job.warning('warning: %s', 'arg')
        expected = [
            call('(%s) warning: %s', 'task_name', 'arg')
        ]
        actual = job.logger.warning.call_args_list
        self.assertEqual(expected, actual)

        job.critical('critical: %s', 'arg')
        expected = [
            call('(%s) critical: %s', 'task_name', 'arg')
        ]
        actual = job.logger.critical.call_args_list
        self.assertEqual(expected, actual)

    def test_logger_without_task_name(self):
        job = Job('job_name')
        job.logger = Mock()

        job.info('info: %s', 'arg')
        expected = [
            call('info: %s', 'arg')
        ]
        actual = job.logger.info.call_args_list
        self.assertEqual(expected, actual)

        job.warning('warning: %s', 'arg')
        expected = [
            call('warning: %s', 'arg')
        ]
        actual = job.logger.warning.call_args_list
        self.assertEqual(expected, actual)

        job.critical('critical: %s', 'arg')
        expected = [
            call('critical: %s', 'arg')
        ]
        actual = job.logger.critical.call_args_list
        self.assertEqual(expected, actual)

    def test_skip(self):
        job = Job('job_name')
        job.skip()
        self.assertEqual(job.skipped, True)

    def test_fail(self):
        job = Job('job_name')
        with self.assertRaises(JobExecutionError):
            job.fail()

    def test_execute_task(self):
        job = Job('job_name')

        # 1回で成功
        task_func = Mock()
        job.executeTask(task_func, 'task_name')
        self.assertEqual(task_func.call_count, 1)

        # 2回で成功
        task_func = Mock()
        task_func.side_effect = [
            Exception(),
            None
        ]
        job.executeTask(task_func, 'task_name',
                        retry_count=1, retry_interval_ms=1)
        self.assertEqual(task_func.call_count, 2)

        # リトライ上限
        task_func = Mock()
        task_func.side_effect = [
            Exception(),
            Exception(),
            Exception()
        ]
        with self.assertRaises(JobExecutionError):
            job.executeTask(task_func, 'task_name',
                            retry_count=2, retry_interval_ms=1)
        self.assertEqual(task_func.call_count, 3)

    def test_task(self):
        task_func = Mock()
        _self = Mock()

        def executeTask(_task_func, task_name, retry_count, retry_interval_ms):
            _task_func()
            expected = [
                call(_self, 'arg', kwarg='kwarg')
            ]
            actual = task_func.call_args_list
            self.assertEqual(expected, actual)
            self.assertEqual(task_name, 'task_name')
            self.assertEqual(retry_count, 10)
            self.assertEqual(retry_interval_ms, 500)

        _self.executeTask = executeTask
        decorator = task('task_name', retry_count=10, retry_interval_ms=500)
        wrapper = decorator(task_func)
        wrapper(_self, 'arg', kwarg='kwarg')
