# -*- coding:utf-8 -*-

from .sortbase import ConditionWithSort


class TorrentSizeCondition(ConditionWithSort):
    def __init__(self, settings):
        ConditionWithSort.__init__(self, settings['sort_type'])
        self._limit = settings['max_size']

    def apply(self, torrents):
        ConditionWithSort.sort_torrents(self, torrents)
        size_sum = 0
        for torrent in torrents:
            if size_sum + torrent.size < self._limit:
                size_sum += torrent.size
                self.remain.append(torrent)
            else:
                self.remove.append(torrent)
