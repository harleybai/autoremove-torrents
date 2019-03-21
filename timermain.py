#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
import sys
import _thread
import sched
from web import index
from getopt import getopt

schedule = sched.scheduler(time.time, time.sleep)


def timer_log(result):
    with open('timerrun.log', 'a', encoding='utf-8') as f:
        pre_log = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' Timer To Remove Torrents Running ...\n'
        f.write(pre_log)
        f.write(result)
        f.flush()


def execute_command(cmd, inc):
    output = os.popen(cmd)
    timer_log(output.read())
    schedule.enter(inc, 0, execute_command, (cmd, inc))


def main(cmd, inc=60):
    # enter四个参数分别为：间隔事件、优先级、被调用触发的函数、触发函数的参数（tuple形式）
    schedule.enter(0, 0, execute_command, (cmd, inc))
    schedule.run()


if __name__ == '__main__':
    # Get arguments
    opts = getopt(sys.argv[1:], 'i:h:p:', ['interval=', 'host=', 'port='])[0]
    inc = 7200
    host = '127.0.0.1'
    port = 17891
    for opt, arg in opts:
        if opt in ('-i', '--interval'):
            inc = int(arg)
        elif opt in ('-h', '--host'):
            host = arg
        elif opt in ('-h', '--host'):
            port = int(arg)
    # Run web
    try:
        _thread.start_new_thread(index.web_run, (host, port))
    except:
        print("Error: unable to start thread")
    # Run
    main("python main.py", inc)
