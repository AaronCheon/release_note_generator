import argparse
import subprocess
import json

"""
Returns the MR iid.
"""

def parser():
  parse = argparse.ArgumentParser("Get list of MR between Tags")
  parse.add_argument("--project_name", "--pn" , type = str, help="Gitlab project name")
  parse.add_argument("--token"                , type = str, help="Secreate token")
  parse.add_argument("--commit_lists"         , nargs='+', type=str, help="List of mr iid")
  return parse

def getMRiid(args):
  project_url = (args.project_name).replace("/","%2F")
  iid_lists = []
  for now_commit in args.commit_lists:
    cmd = f"curl --header PRIVATE-TOKEN:{args.token} http://portal:8888/api/v4/projects/{project_url}/repository/commits/{now_commit}/merge_requests".split(" ")
    iid_datas = subprocess.check_output(cmd).decode('utf-8')
    tmp_datas = (json.loads(iid_datas))
    iid_lists = iid_lists + [ each["iid"] for each in tmp_datas ]


  return list(set(iid_lists))

if __name__ == '__main__':
  args = parser().parse_args()
  getMRiid(args)
