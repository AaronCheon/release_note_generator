import argparse
import subprocess
import re

def parser():
  parse = argparse.ArgumentParser("Get tag name")
  parse.add_argument("--dir","-d", help="Git top directory", type=str, default=".")
  parse.add_argument("--current","-c", help="Current tag. If not set use latest tag")
  return parse

def findCurrentTag(args) :
  currentTag = subprocess.check_output(["git", "-C", args.dir, "describe", "--tags", "--abbrev=0"]).decode('utf-8').strip()
  return currentTag

def findprevious(args, currentTag) :
  count = 1
  pattern = re.compile("([AL|BT|FN]*)[_]REL(\d)(\d)(.*)")
  tagNum = len(re.findall(pattern, subprocess.check_output(["git", "-C", args.dir, "tag"]).decode('utf-8').strip()))
  previous = None

  if tagNum == 1 :
    previous = subprocess.check_output(["git", "-C", args.dir, "rev-list", "--max-parents=0", "HEAD"]).decode('utf-8').strip()

  else :
    while True:
      cmd = ["git", "-C", args.dir, "describe", "--always", "--tags", "--abbrev=0", f"{currentTag}~{count}"]
      previous = subprocess.check_output(cmd).decode('utf-8').strip()
      if pattern.match(previous) != None:
        break

      else :
        count += 1
  return previous

def getTagName(args) :
  currentTag = args.current
  if currentTag == None :
    currentTag = findCurrentTag(args)
  previous = findprevious(args, currentTag)
  return currentTag, previous

if __name__ == '__main__' :
  args = parser().parse_args()
  getTagName(args)
