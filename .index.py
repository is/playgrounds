import os
import sys
import glob
import operator
import time

import ruamel_yaml as yaml
import pprint

import warnings
warnings.simplefilter('ignore', yaml.error.UnsafeLoaderWarning)

def list_projects():
  dirs = [ d for d in glob.glob("*") if os.path.isdir(d)]
  for i in ['2019', '2020', '2021', '2021' ]:
    dirs.extend([d for d in glob.glob("%s/*" % i)
      if os.path.isdir(d)])
  return dirs

def project_infos(projs):
  infos = []
  for p in projs:
    if not os.path.isfile(os.path.join(p, ".desc")):
      continue
    with open(os.path.join(p, ".desc")) as f:
      x = yaml.load(f.read())
      if not 'serial' in x:
        x['serial'] = 40
      x['name'] = p
      infos.append(x)
  return infos


# ---
def project_infos_to_text(infos):
  res = []
  curdate = ''

  infos.sort(key = operator.itemgetter("date", "serial", "name"), reverse=True)
  res.append("  ///// LIVE PROJECT /////")
  for info in infos:
    if 'live' in info and info['live']:
      res.append("  - {name}: {desc} - {date}".format(**info))
      print(info)
  print("--")
  res.append("")
  for info in infos:
    if 'live' in info and info['live']:
      continue
    if curdate != '' and info['date'] != curdate:
      res.append("")
    curdate = info['date']
    print(info)
    res.append("  - {name}: {desc} - {date}".format(**info))
  print(res)
  return "\n".join(res)


def project_infos_to_link(infos, contents):
  BASE_URL = "http://github.com/is/playgrounds/tree/master"
  res = contents
  infos.sort(key = operator.itemgetter("date", "serial", "name"), reverse=True)
  c = 0
  for info in infos:
    name = info['name']
    serial = info['serial']
    if name.find('/') != -1:
      realname = name.partition('/')[2]
    else:
      realname = name
    line = "[`%s.%s`](%s/%s), " % (realname, serial, BASE_URL, name)
    c += len(realname)
    if c >= 60:
      line += "  "
      c = 0
    line += "\n"
    res.append(line)
  res.append("`__END__`\n")
  res.append("\n")

def update_readme():
  if not os.path.exists('README.md'):
    return

  contents = []

  pis = project_infos(list_projects())
  with open('README.md', 'r') as f:
    status = 0
    for line in f:
      row = line.strip()
      if status == 0 and row == '# PROJECT LIST':
        status = 1
      elif status == 1 and row == "```":
        status = 2
      elif status == 2 and row == "```":
        contents.append("# PROJECT LIST\n")
        contents.append("```\n")
        contents.append(project_infos_to_text(pis))
        contents.append("\n```\n")
        status = 0
      elif status == 0 and row == '# LINKS':
        status = 4
      elif status == 4 and len(row) == 0:
        contents.append('# LINKS\n')
        project_infos_to_link(pis, contents)
        status = 0
      elif status == 0:
        contents.append(line)


  with open('README.md', 'w') as f:
    f.write("".join(contents))


def new_project():
  name = sys.argv[1]
  with open('.serial') as fi:
    serial = int(fi.read().strip())
  os.mkdir(name)

  with open(name + '/.desc', 'w') as fo:
    fo.write("""---
desc: __
date: "{ds}"
serial: {serial}
tags: unset
""".format(ds=time.strftime("%Y.%m"), serial=serial))
  serial += 1
  with open('.serial', 'w') as fo:
    fo.write(str(serial))

if __name__ == '__main__':
  if len(sys.argv) > 1:
    new_project()
  else:
    update_readme()
