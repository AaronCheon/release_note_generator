import argparse
import subprocess
import json

"""
Returns the MR data of Gitlab via MR-iid, project name, and token. Use Gitlab rest api.
"""

def parser():
  parse = argparse.ArgumentParser("Get MR datas")
  parse.add_argument("--project_name", "--pn" , type = str, help="Gitlab project name")
  parse.add_argument("--token"                , type = str, help="Secreate token")
  parse.add_argument("--iid_lists"             , nargs='+', type=str, help="List of mr iid")
  return parse

def parseData(projectname, iid, token):
  tmp_projectname = projectname.replace("/","%2F")
  cmd = f"curl --header PRIVATE-TOKEN:{token} http://portal:8888/api/v4/projects/{tmp_projectname}/merge_requests/{iid}".split(" ")
  mr_datas = subprocess.check_output(cmd).decode('utf-8')
  return json.loads(mr_datas)

def getMRdata(args):
  mr_datas = []
  for now_iid in args.iid_lists:
    mr_datas.append(parseData( projectname =args.project_name, iid = now_iid, token = args.token))
  return mr_datas

if __name__ == '__main__':
  args = parser().parse_args()
  getMRdata(args)
