# -*- coding:utf-8 -*-

from .filter import Filter


class CategoryFilter(Filter):
    def __init__(self, all_category, ac, re):
        Filter.__init__(self, all_category, ac, re)

    def apply(self, torrents):
        # result remain_torrents, filtered_size, filtered_num
        result = [[], 0, 0]
        for torrent in torrents:
            if (self._all or torrent.category in self._accept) and torrent.category not in self._reject:
                result[0].append(torrent)
            else:
                result[1] += torrent.size
                result[2] += 1

        return result
