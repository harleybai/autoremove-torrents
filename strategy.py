# -*- coding:utf-8 -*-

import log
from condition.createtime import CreateTimeCondition
from condition.donothing import EmptyCondition
from condition.ratio import RatioCondition
from condition.seedingtime import SeedingTimeCondition
from condition.torrentnumber import TorrentNumberCondition
from condition.torrentsize import TorrentSizeCondition
from filter.category import CategoryFilter
from filter.status import StatusFilter
from filter.tracker import TrackerFilter


class Strategy(object):
    # Logger
    _logger = log.register(__name__)

    def __init__(self, name, conf):

        # Save name
        self._name = name

        # Configuration
        self._conf = conf

        # Results
        self.remain_list = []
        self.remove_list = []

        # Filter ALL
        self._all_categories = conf['all_categories'] if 'all_categories' in conf \
            else 'categories' not in conf
        self._all_trackers = conf['all_trackers'] if 'all_trackers' in conf \
            else 'trackers' not in conf
        self._all_status = conf['all_status'] if 'all_status' in conf \
            else 'status' not in conf
        self.filtered_size = 0
        self.filtered_num = 0

    # Apply Filters
    def _apply_filters(self):
        filter_conf = [
            {'all': self._all_categories, 'ac': 'categories', 're': 'excluded_categories'},  # Category filter
            {'all': self._all_trackers, 'ac': 'trackers', 're': 'excluded_trackers'},  # Tracker filter
            {'all': self._all_status, 'ac': 'status', 're': 'excluded_status'}  # Status filter
        ]
        filter_name = ['Category', 'Tracker', 'Status']
        filter_obj = [CategoryFilter, TrackerFilter, StatusFilter]
        for i in range(0, len(filter_conf)):
            if filter_conf[i]['ac'] in self._conf or filter_conf[i]['re'] in self._conf:
                # Logging
                self._logger.info(
                    'Filter `%s` is working to process %d torrent(s): Accept All: %s, Accept: %s, Reject: %s.' \
                    % (
                        filter_name[i],
                        len(self.remain_list),
                        'Yes' if filter_conf[i]['all'] else 'No',
                        str(self._conf[filter_conf[i]['ac']]) if filter_conf[i][
                                                                     'ac'] in self._conf else 'Not Specified',
                        str(self._conf[filter_conf[i]['re']]) if filter_conf[i][
                                                                     're'] in self._conf else 'Not Specified',
                    ))
                # Apply each filter
                filter_result = filter_obj[i](
                    filter_conf[i]['all'],
                    self._conf[filter_conf[i]['ac']] if filter_conf[i]['ac'] in self._conf else [],
                    self._conf[filter_conf[i]['re']] if filter_conf[i]['re'] in self._conf else []
                ).apply(self.remain_list)

                self.remain_list = filter_result[0]
                self.filtered_size += filter_result[1]
                self.filtered_num += filter_result[2]

    def conf_refresh(self):
        if 'seed_size' in self._conf:
            #  limit = limit * 1GiB, The unit of result is bytes.
            self._conf['seed_size']['max_size'] = self._conf['seed_size']['max_size'] * 1073741824 - self.filtered_size
        if 'maximum_number' in self._conf:
            self._conf['maximum_number']['max_num'] = self._conf['maximum_number']['max_num'] - self.filtered_num

    # Apply Conditions
    def _apply_conditions(self):
        # Condition collection
        condition_field = [
            'seeding_time', 'create_time',
            'ratio', 'seed_size', 'maximum_number', 'nothing'
        ]
        condition_obj = [
            SeedingTimeCondition, CreateTimeCondition,
            RatioCondition, TorrentSizeCondition, TorrentNumberCondition, EmptyCondition
        ]
        # refresh config
        self.conf_refresh()

        for i in range(0, len(condition_field)):
            # Apply each condition
            if condition_field[i] in self._conf:
                # Logging
                self._logger.info('Remove condition `%s` was specified to process %d torrent(s).' % (
                    condition_field[i], len(self.remain_list)))
                if 'sort_type' in self._conf[condition_field[i]]:
                    self._logger.info('Remove condition `%s`, its parameter was `%s`.' % (
                        condition_field[i], str(self._conf[condition_field[i]])))
                # Applying condition processor
                cond = condition_obj[i](self._conf[condition_field[i]])
                cond.apply(self.remain_list)
                # Output
                self.remain_list = cond.remain
                self.remove_list.extend(cond.remove)

    # Execute this strategy
    def execute(self, torrents):
        self._logger.info('Running strategy %s...' % self._name)
        self.remain_list = torrents
        # Apply Filters
        self._apply_filters()
        # Apply Conditions
        self._apply_conditions()
        # Print remove list
        self._logger.info("Total: %d seed(s). %d seed(s) can be removed." %
                          (len(self.remain_list) + len(self.remove_list), len(self.remove_list)))
        if len(self.remove_list) > 0:
            out_str = 'To be deleted:\n\n'
            for torrent in self.remove_list:
                out_str += torrent.__str__()
            self._logger.info(out_str)
        # self._logger.debug('To be remained:')
        # for torrent in self.remain_list:
        #    self._logger.debug(torrent)
        # return self.remove_list
