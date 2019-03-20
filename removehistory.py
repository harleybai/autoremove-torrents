#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import json
import os


def convert_bytes(byte):
    units = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB', 'BiB', 'NiB', 'DiB', 'CiB']
    unit = units[0]
    for x in units:
        unit = x
        if divmod(byte, 1024)[0] == 0:
            break
        else:
            byte /= 1024
    return '%.2lf%s' % (byte, unit)


def save_history(torrents, torrents_backup):
    # get last result
    last_res = get_history()
    if len(last_res["history"]) > 9:
        last_res["history"] = last_res["history"][0:9]
    # get time
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # result of this tile
    result = {
        "info": last_res["info"],
        "history": [{'time': now, 'num': len(torrents), 'list': []}]
    }
    # get info
    result["info"]["num"] = len(torrents_backup) - len(torrents)
    result["info"]["size"] = 0
    result["info"]["upload"] = 0
    for t in torrents_backup:
        result["info"]["size"] += t.size
        result["info"]["upload"] += t.uploaded
    # handle remove torrents
    for t in torrents:
        result["info"]["size"] -= t.size
        result[0]['list'].append(t.__str__())
    result["history"].extend(last_res["history"])
    # byte convert
    result["info"]["size"] = convert_bytes(result["info"]["size"])
    result["info"]["upload"] = convert_bytes(result["info"]["upload"])
    # write file
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(result, f)
        f.flush()


def get_history():
    if not (os.path.exists('data.json') and os.path.isfile('data.json')):
        return {"info": {}, "history": []}

    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        data["history"] = sorted(data["history"], key=lambda t: t["time"], reverse=True)
    return data
