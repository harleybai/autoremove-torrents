# -*- coding:utf-8 -*-

import urllib.parse
from .filter import Filter


class TrackerFilter(Filter):
    def __init__(self, all_tracker, ac, re):
        Filter.__init__(self, all_tracker, ac, re)

    def apply(self, torrents):
        # result remain_torrents, filtered_size, filtered_num
        result = [[], 0, 0]
        for torrent in torrents:
            for tracker in torrent.tracker:  # For each tracker
                tracker = urllib.parse.urlparse(tracker).netloc
                if self._all or tracker in self._accept:
                    if torrent not in result[0]:
                        result[0].append(torrent)
                if tracker in self._reject:
                    result[0].remove(torrent)
                    result[1] += torrent.size
                    result[2] += 1
                    break  # Reject this seed
        return result
