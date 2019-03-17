# -*- coding:utf-8 -*-

from .base import Condition


class ConditionWithSort(Condition):
    def __init__(self, sort_type):
        Condition.__init__(self)
        self._sort_type = sort_type

    def sort_torrents(self, torrents):
        sort_types = [
            'remove-old-seeds-first',
            'remove-new-seeds-first',
            'remove-big-size-first',
            'remove-small-size-first',
            'remove-big-ratio-first',
            'remove-small-ratio-first',
        ]
        parameter = [
            {'key': lambda torrent: torrent.create_time, 'reverse': True},
            {'key': lambda torrent: torrent.create_time, 'reverse': False},
            {'key': lambda torrent: torrent.size, 'reverse': False},
            {'key': lambda torrent: torrent.size, 'reverse': True},
            {'key': lambda torrent: torrent.ratio, 'reverse': False},
            {'key': lambda torrent: torrent.ratio, 'reverse': True},
        ]
        for i in range(0, len(sort_types)):
            if self._sort_type == sort_types[i]:
                torrents.sort(key=parameter[i]['key'], reverse=parameter[i]['reverse'])
