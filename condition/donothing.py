# -*- coding:utf-8 -*-

from .base import Condition


class EmptyCondition(Condition):
    def __init__(self):
        Condition.__init__(self)

    def apply(self, torrents):
        self.remain = torrents
