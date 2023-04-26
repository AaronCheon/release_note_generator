import argparse
import subprocess
import json
import os

"""
Set issue link
"""

def parser():
  parse = argparse.ArgumentParser("Set issue link")
  parse.add_argument("--now_tag"  , type = str, help="Now tag name")
  parse.add_argument("--pre_tag"  , type = str, help="Previous tag name")
  parse.add_argument("--token"    , type = str, help="Secreate token")
  parse.add_argument("--project_json",  type = open, help="Project json"  )
  return parse

def getKey( tagname, key, project, token):
  cmd = f'curl  --user {token} https://aaroncheon.atlassian.net/rest/api/3/search?jql=project%20%3D%20{key}'.split()

  tmp = json.loads(subprocess.check_output(cmd).decode('utf-8'))

  for now_issue in tmp["issues"]:
    if f"[{project}] {tagname} release" == now_issue["fields"]["summary"]:
      return now_issue["key"]

def setLink(nowkey, prekey, token):
  datajson = {"outwardIssue": {"key": prekey},"inwardIssue": {"key": nowkey},"type": {"name": "Hierarchy [Gantt]"}}
  datastring = json.dumps(datajson)
  cmd = f"curl --request POST --url 'https://aaroncheon.atlassian.net/rest/api/3/issueLink' --user '{token}' --header 'Accept:application/json' --header 'Content-Type:application/json'  --data '{datastring}'"
  os.system(cmd)


def setLinkMain(args):
  tmp_json = json.loads(args.project_json.read())
  now_key = getKey( tagname = args.now_tag, key = tmp_json['JiraKey'], project=tmp_json["project"], token = args.token)
  if args.pre_tag is not None:
    pre_key = getKey( tagname = args.pre_tag, key = tmp_json['JiraKey'], project=tmp_json["project"], token = args.token)
    setLink(nowkey=now_key, prekey=pre_key, token=args.token)
  else:
    pre_key = None

  return now_key, pre_key

#python3.7 setLink.py --now_tag=AL_REL02 --pre_tag=AL_REL01  --token=<user token> --project_json ../../sprint3/jenkins/release_report.json
if __name__ == '__main__':
  args = parser().parse_args()
  setLinkMain(args)
