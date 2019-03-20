#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
import sched

schedule = sched.scheduler(time.time, time.sleep)


def timer_log(result):
    with open('timer_remove_torrents.log', 'a', encoding='utf-8') as f:
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
    main("python main.py", 7200)
