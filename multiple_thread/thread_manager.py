# -*- coding: utf-8 -*-
# coding=utf-8
import threading


class ThreadManager:
    def __init__(self, thread_count=6):
        self.__max_thread_count = thread_count
        self.__threads = []

    def run(self, data, dispose_func, **kwargs):
        if len(data) == 0:
            return True

        kwargs['__max_thread_count'] = self.__max_thread_count
        size = len(data) / self.__max_thread_count + 1
        for index in range(self.__max_thread_count):
            offset = size * index
            items = data[offset:offset + size]
            if len(items) == 0:
                continue

            kwargs['__thread_id'] = index
            self.__dispose(items, dispose_func, **kwargs)

        for thread in self.__threads:
            thread.join()
        self.__threads = []

    def __dispose(self, items, dispose_func, **kwargs):
        args = [items, kwargs]
        thread = threading.Thread(target=dispose_func, args=args)
        self.__threads.append(thread)
        thread.start()
