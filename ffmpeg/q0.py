#!/usr/bin/env python
import glob
import psutil
import time
import os
import sys

QUEUE_DIR = os.path.join(os.environ['HOME'], '.enc0/queue')
RUN_DIR = os.path.join(os.environ['HOME'], '.enc0/run')

INTERVAL = 5
TMUX = 'f2'
PARALLEL = 2

def find_running_ffmpeg():
    R = []
    pids = psutil.pids()
    for pid in pids:
        try:
            P = psutil.Process(pid)
        except psutil.NoSuchProcess:
            continue
        if (P.name().find("ffmpeg") >= 0):
            R.append(P)
    return R

def tip():
    n = find_running_ffmpeg()
    if len(n) >= PARALLEL:
        return

    fns = glob.glob(QUEUE_DIR + "/__*")
    if len(fns) == 0:
        return

    fn = fns[0]
    script_name = os.path.basename(fn)
    print("%s - %d . fire %s" % (time.strftime("%Y-%m-%d %H:%M:%S"), len(n), script_name))
    os.system(f"mv {fn} {RUN_DIR}")
    os.system(f"chmod a+x {RUN_DIR}/{script_name}")
    os.system(f"tmux neww -t {TMUX} {RUN_DIR}/{script_name}")

def main():
    while True:
        tip()
        time.sleep(INTERVAL)

if __name__ == '__main__':
    main()
