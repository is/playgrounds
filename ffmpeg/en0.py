#!/usr/bin/env -- python

import os
import sys
import glob
from os import path

P = path.join
OUT_DIR = P(os.environ.get("HOME"), ".enc0")
EXEC_PATH = P(path.abspath(sys.argv[0]))
EXEC_DIR = P(path.dirname(EXEC_PATH))
FFMPEG_PROFILE = P(EXEC_DIR, "profiles")

PROFILE_HEAD_TAG = '# --- profile'


def read_profiles_from_file(fn):
    fin = open(fn)
    lines = fin.readlines()

    profiles = {}

    state = 0
    for line in lines:
        line = line.strip()
        if state == 0:
            if line.startswith(PROFILE_HEAD_TAG):
                line = line[len(PROFILE_HEAD_TAG) + 1:]
                name, _, desc = line.partition(' ')
                state = 1
                opts = []
                continue

        if state == 1:
            if line.startswith("ffmpeg"):
                continue
            if line.endswith("\\"):
                opts.append(line[:-1].strip())
                continue
            if line.startswith("#"):
                continue
            if len(line) != 0:
                opts.append(line)
            profiles[name] = [desc, opts]
    fin.close()
    return profiles


def input_fn(dir):
    base = os.path.abspath(dir)
    fns = []
    for ext in "wmv,mp4,mkv,avi".split(","):
        fns.extend(glob.glob(base + "/*." + ext))
    print(fns)


def find_input(dir):
    base = os.path.abspath(dir)
    fns = []
    for ext in "wmv,mp4,mkv,avi".split(","):
        fns.extend(glob.glob(base + "/*." + ext))
    name = path.basename(base)
    return name, fns

def main():
    #print(EXEC_PATH)
    #print(EXEC_DIR)
    #print(FFMPEG_PROFILE)
    
    profile = None
    profile_fn = FFMPEG_PROFILE
    profiles = read_profiles_from_file(profile_fn)
    run_script = True
    source_dir = "."
    
    for arg in sys.argv:
        if (arg.endswith(".profile")):
            profile_fn = arg
            profiles = read_profiles_from_file(profile_fn)
            continue
        if arg in profiles:
            profile = arg
            continue
        if os.path.isdir(arg):
            source_dir = arg
            continue
        if arg == 'dry':
            run_script = False
            continue

    name, fns = find_input(source_dir)
    if profile == None:
        print('PROFILES: {}'.format(",".join(profiles.keys())))
        if name != None and len(fns) != 0:
            print("INPUTS: {}".format(",".join(fns)))
        sys.exit(0)

    I = fns[0]
    O = P(OUT_DIR, name, name + '__' + profiles[profile][0] + ".mp4")
    D = path.dirname(O)
    cmds = ["#!/bin/sh", "# --"]
    cmds.append(f"export I={I}")
    cmds.append(f"export O={O}")
    cmds.append(f"mkdir -p {D}")
    cmds.append(f'if [ "$TMUX" != "" ] ; then tmux renamew {name} ; fi')
    cmds.append("ffmpeg -hide_banner -y \\")
    cmds.append(" -i $I \\")
    cmds.append(" " + " \\\n ".join(profiles[profile][1]) + " \\")
    cmds.append(" $O")


    print("\n".join(cmds))
    print("\n----")
    script_path = P(OUT_DIR, "__" + name)
    fout = open(script_path, "w")
    fout.write("\n".join(cmds))
    fout.close()
    os.chmod(script_path, 0o500)
    print(script_path)

    if run_script:
        os.execl(script_path, script_path)

if __name__ == '__main__':
    main()
