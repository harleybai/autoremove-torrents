from .sortbase import ConditionWithSort


class TorrentNumberCondition(ConditionWithSort):
    def __init__(self, settings):
        ConditionWithSort.__init__(self, settings['sort_type'])
        self._max_num = settings['max_num']

    def apply(self, torrents):
        ConditionWithSort.sort_torrents(self, torrents)
        if self._max_num == 0:
            self.remove = torrents
        elif self._max_num < len(torrents):
            self.remain = torrents[0:self._max_num]
            self.remove = torrents[self._max_num:]
        else:
            self.remain = torrents
