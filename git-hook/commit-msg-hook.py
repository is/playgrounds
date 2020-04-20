#!/usr/bin/env python
import os
import sys
import re


def P(*args):
  return os.path.join(*args)

def exists(*args):
  return os.path.exists(P(*args))

def read_id_file(*args):
  with open(P(*args), 'r') as f:
    id = f.read()
  return id.strip()

def read_id_yml_file(*args):
  with open(P(*args), 'r') as f:
    lines = f.readlines()

  for line in lines:
    if line.startswith("id:"):
      return line.partition(":")[2].strip()
  return None


def get_current_id(path):
  while True:
    for k in [".id", ".branchtag", ".gittag", ".gitid", ".gitlabel"]:
      if exists(path, k):
        id = read_id_file(path, k)
        if id:
          return id

    if exists(path, ".desc"):
      id = read_id_yml_file(path, ".desc")
      if id:
        return id

    cur = os.path.basename(path)
    path = os.path.dirname(path)

    if cur == 'x':
      return None

    if path == '/':
      return None


def rewrite_message(id, msg):
  if id == None:
    return None

  lines = msg.split("\n")

  first_line = lines[0]
  re_h0 = re.compile(r'^. ')
  head = None
  match = re_h0.match(first_line)

  if match:
    head = match.group(0)
    first_line = first_line[2:]

  if first_line[0] == '[':
    return None

  first_line = '[{}] {}'.format(id, first_line)
  if head is not None:
    first_line = head + first_line
  lines[0] = first_line
  return "\n".join(lines)


def main():
  # print("-- call - commit-msg hook --")
  # print(prefix)
  prefix = P(os.getcwd(), os.environ['GIT_PREFIX'])
  fn = sys.argv[1]
  with open(fn, 'r') as f:
    msg = f.read()
  id = get_current_id(prefix)
  if id == None:
    return
  rewrite_msg = rewrite_message(id, msg)
  if rewrite_msg != None:
    with open(fn, 'w') as f:
      f.write(rewrite_msg)
  sys.exit(0)

if __name__ == '__main__':
  main()
