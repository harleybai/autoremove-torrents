#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import json
import os


def save_history(torrents):
    history = get_history()
    if len(history) > 9:
        history = history[0:9]

    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    result = [{'time': now, 'num': len(torrents), 'list': []}]
    for t in torrents:
        result[0]['list'].append(t.__str__())
    result.extend(history)

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(result, f)
        f.flush()


def get_history():
    if not (os.path.exists('data.json') and os.path.isfile('data.json')):
        return []

    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        data = sorted(data, key=lambda t: t["time"], reverse=True)
    return data
