import argparse
import subprocess

def parser():
  parse = argparse.ArgumentParser("Get list of MR between Tags")
  parse.add_argument("--from_tag", "-f", help="From Tag", type=str, required=True)
  parse.add_argument("--to_tag", "-t", help="To Tag", type=str, required=True)
  parse.add_argument("--dir","-d", help="Git top directory", type=str, default=".")
  return parse

def getCommitList(args):
  cmd = ["git", "-C", args.dir, "log", "--reverse", "--merges", "--pretty=oneline", "--format=format:'%H'", f"{args.from_tag}...{args.to_tag}", "--first-parent"]
  commit_list = subprocess.check_output(cmd).decode('utf-8').replace('\'','').splitlines()
  return commit_list

if __name__ == '__main__':
  args = parser().parse_args()
  out = getCommitList(args)
