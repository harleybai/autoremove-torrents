# -*- coding:utf-8 -*-
import requests
from requests.auth import HTTPBasicAuth

from exception.connectionfailure import ConnectionFailure
from exception.loginfailure import LoginFailure
from exception.nosuchclient import NoSuchClient
from exception.remotefailure import RemoteFailure
from torrent import Torrent
from torrentstatus import TorrentStatus


class Transmission(object):
    def __init__(self, host):
        # Host
        self._host = host
        # X-Transmission-Session-id
        self._session_id = ''
        # Request id
        self._request_id = 0
        # username & password
        self._username = None
        self._password = None

    # Login to Transmission
    def login(self, username, password):
        # Login when requesting
        self._username = username
        self._password = password

    # Make Transmission Request
    def _make_transmission_request(self, method, arguments=None):
        retry = 3
        while retry > 0:
            retry -= 1
            # Make request
            try:
                request = requests.post(self._host + '/transmission/rpc',
                                        json={'method': method, 'arguments': arguments, 'tag': self._request_id},
                                        headers={'X-Transmission-Session-Id': self._session_id},
                                        auth=HTTPBasicAuth(self._username, self._password))
                self._request_id += 1
            except Exception as exc:
                raise ConnectionFailure(str(exc))

            if request.status_code == 409:  # Save Session ID and retry
                self._session_id = request.headers['X-Transmission-Session-Id']
            elif request.status_code == 401:  # Unauthorized user
                raise LoginFailure('Unauthorized user.')
            elif request.status_code == 200:
                result = request.json()
                if result['result'] == 'success':  # Success
                    return result['arguments']
                else:
                    raise RemoteFailure(result['result'])
        raise RemoteFailure('The server responsed %d on method %s.' \
                            % (request.status_code, method)
                            )

    # Get Transmission Version
    def version(self):
        ver = self._make_transmission_request('session-get')['version']
        return ('Transmission %s' % ver)

    # Get Torrents List
    def torrents_list(self):
        torrents_hash = []
        for torrent in self._make_transmission_request('torrent-get', {'fields': ['hashString']})['torrents']:
            torrents_hash.append(torrent['hashString'])
        return torrents_hash

    # Get Torrent Properties
    def torrent_properties(self, torrent_hash):
        result = self._make_transmission_request('torrent-get',
                                                 {'ids': [torrent_hash],
                                                  'fields': ['hashString', 'name', 'trackers', 'status', 'totalSize',
                                                             'uploadRatio', 'uploadedEver', 'addedDate',
                                                             'secondsSeeding']}
                                                 )
        if len(result['torrents']) == 0:  # No such torrent
            raise NoSuchClient("No such torrent of hash '%s'." % torrent_hash)
        torrent = result['torrents'][0]
        # Judge status
        status_list = [
            TorrentStatus.Stopped,  # 0:STOPPED
            TorrentStatus.Queued,  # 1:CHECK_WAIT
            TorrentStatus.Checking,  # 2:CHECK
            TorrentStatus.Queued,  # 3: DOWNLOAD_WAIT
            TorrentStatus.Downloading,  # 4:DOWNLOAD
            TorrentStatus.Queued,  # 5:SEED_WAIT
            TorrentStatus.Uploading,  # 6:SEED
            TorrentStatus.Unknown  # 7:ISOLATED(Torrent can't find peers)
        ]
        status = status_list[torrent['status']]
        return Torrent(
            torrent['hashString'], torrent['name'], '',
            [tracker['announce'] for tracker in torrent['trackers']],
            status, torrent['totalSize'], torrent['uploadRatio'],
            torrent['uploadedEver'], torrent['addedDate'], torrent['secondsSeeding'])

    # Remove Torrent
    def remove_torrent(self, torrent_hash):
        self._make_transmission_request('torrent-remove',
                                        {'ids': [torrent_hash], 'delete-local-data': False})

    # Remove Data
    def remove_data(self, torrent_hash):
        self._make_transmission_request('torrent-remove',
                                        {'ids': [torrent_hash], 'delete-local-data': True})
