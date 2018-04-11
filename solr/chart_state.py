# -*- coding: utf-8 -*-
# coding=utf-8


class ChartState:
    def __init__(self):
        pass

    INVALID = -1
    UNSYNCED = 0
    SYNCED = 1
    UPDATED = 2
    DELETED = 3
    DEPRECATED = 4
    DEPRECATED_NEW = 5
    SYNCED_NEW = 6