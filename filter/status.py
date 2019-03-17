from .filter import Filter
from torrentstatus import TorrentStatus
import log


class StatusFilter(Filter):
    def __init__(self, all_status, ac, re):
        Filter.__init__(self, all_status, ac, re)
        self._logger = log.register(__name__)  # Register a logger

    def _convert_status(self, status_list):
        result = []
        for status in status_list:
            try:
                result.append(TorrentStatus[str(status).capitalize()])
            except KeyError:
                self._logger.warning(
                    "The status '%s' does not exist, so it won't be used."
                    % str(status)
                )
        return result

    def apply(self, torrents):
        # Generate accpet and reject lists
        accept = self._convert_status(self._accept)
        reject = self._convert_status(self._reject)

        # result remain_torrents, filtered_size, filtered_num
        result = [[], 0, 0]
        for torrent in torrents:
            if (self._all or torrent.status in accept) and torrent.status not in reject:
                result[0].append(torrent)
            else:
                result[1] += torrent.size
                result[2] += 1

        return result
