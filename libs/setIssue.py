import argparse
import subprocess
import json
import os
import codecs
import requests
from requests.auth import HTTPBasicAuth
from pathlib import Path

"""
Set issue
"""

def parser():
  parse = argparse.ArgumentParser("Set issue")
  parse.add_argument("--issue_description"    , type = str, help="issue_description")
  parse.add_argument("--now_tag"              , type = str, help="Now tag name")
  parse.add_argument("--token"                , type = str, help="Secret token")
  parse.add_argument("--project_json"         , type = Path, help="Project json"  )
  return parse

def searchCustomfield(projectKey, token):
  url = "https://aaroncheon.atlassian.net/rest/api/3/field/"
  auth = HTTPBasicAuth(token.split(":")[0], token.split(":")[1])
  headers = {
    "Accept": "application/json"
  }
  response = requests.request(
    "GET",
    url,
    headers=headers,
    auth=auth
  )

  temp_all_json = json.loads(response.text)
  temp_cc_customid =  [ each for each in temp_all_json if "CC" in each["name"] or "cc" in each["name"] or "C.C" in each["name"] ]

  url = f"https://aaroncheon.atlassian.net/rest/api/3/project/{projectKey}"
  headers = {
    "Accept": "application/json"
  }
  response = requests.request(
    "GET",
    url,
    headers=headers,
    auth=auth
  )

  temp_project_json = json.loads(response.text)
  temp_key_id = str(temp_project_json['id'])
  search_key = str

  for each in temp_cc_customid:
    if 'scope' not in each:
      pass
    elif str(each['scope']['project']['id']) == temp_key_id:
      search_key = each['key']
      break
  return search_key

def userId(user, token):
  cmd = f"curl --request GET --url https://aaroncheon.atlassian.net/rest/api/3/groupuserpicker\?query\={user} --user {token} --header Accept:application/json"
  userjson = json.loads(os.popen(cmd).read())
  try :
    return userjson['users']['users'][0]['accountId']
  except :
    pass

def setIssue(dataJson, token):
  with open("data_tmp.json", 'w') as fp_tmp:
    json.dump(dataJson, fp_tmp, indent=2)
  cmd = f"curl -D- -u {token} -X POST -H Content-Type:application/json https://aaroncheon.atlassian.net/rest/api/latest/issue/ --data @data_tmp.json".split(" ")
  subprocess.run(cmd)

def setIssueMain(args):
  tmp_json = json.load(open(args.project_json))
  ccKey = searchCustomfield(tmp_json['JiraKey'], args.token)
  tmp_ccId = [ userId(each , args.token) for each in tmp_json['receivers'] ]
  ccAcount = [ { "accountId" : each } for each in tmp_ccId ]

  dataJson = {
    "fields": {
      "project":
      {
        "key": tmp_json['JiraKey']
      },
      "summary": f"[{tmp_json['project']}] {args.now_tag} release",
      "description": str(args.issue_description),
      "issuetype": {
        "name": "Task"
      },
      "labels": [
        tmp_json['lable']
      ],
      "assignee" : {
        "accountId" : userId(tmp_json["leader"], args.token)
      },
      ccKey : ccAcount
    }
  }

  return setIssue(dataJson=dataJson, token=args.token)

# python3.7 setIssue.py --now_tag=AL_REL02 --token=<user token> --project_json ../../sprint3/jenkins/release_report.json --issue_description "h2 testtest"
if __name__ == '__main__':
  args = parser().parse_args()
  setIssueMain(args)
