import argparse
from pathlib import Path
import json
import datetime as dt
from jinja2 import Template, Environment, FileSystemLoader
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import subprocess
import os

"""
email send scripts
"""

def parser():
  parse = argparse.ArgumentParser("Get MR data")
  parse.add_argument("--from_tag", "-f"       , type=str,  help="From Tag")
  parse.add_argument("--key_id"               , type=str, help="Jira key id")
  parse.add_argument("--jira_token"           , type=str, help="Jira token")
  parse.add_argument("--project_json"         , type=open, help="Project json")
  parse.add_argument("--html_jinja"           , type=Path, help="Html Jinja")
  return parse

def parse_description(token : str, ticket_num : str):
  api_url = f"https://aaroncheon.atlassian.net/rest/api/latest/issue/{ticket_num}/?fields=description&expand=renderedFields"
  cmd = f"curl  {api_url} --user {token}".split(" ")
  ticket_data = json.loads(subprocess.check_output(cmd).decode('utf-8'))

  return ticket_data['renderedFields']['description']

def renderHtml(project_json : dict):
  tmp = Environment(loader=FileSystemLoader("/")).get_template(str(os.path.abspath(str(project_json["html_jinja"]))))
  return tmp.render( project_json)

def sendMail(title : str, receive_list : list, body : str):

  mimemsg = MIMEMultipart()
  mimemsg['From']="jenkins@github.com"
  mimemsg['To']= ",".join(receive_list)
  mimemsg['Subject']=title
  mimemsg.attach(MIMEText(body, 'html'))

  connection = smtplib.SMTP(host='smtp.office365.com', port=587)
  connection.starttls()
  connection.login('jenkins@github.com','jenkins12!@')
  connection.send_message(mimemsg)
  connection.quit()


def emailSend(args):
  project_json = json.loads((args.project_json).read())
  x = dt.datetime.now()
  project_json["html_jinja"] = args.html_jinja
  project_json["fromTag"] = args.from_tag
  project_json["jiraURL"] = f"https://aaroncheon.atlassian.net/browse/{args.key_id}"
  project_json["todayDate"] = x.strftime('%Y.%m.%d')

  ticket_num = args.key_id
  ticket_description = parse_description(token = args.jira_token, ticket_num = ticket_num)

  project_json["ticketID"] = ticket_num
  project_json["ticketDescription"] = ticket_description

  tmp_body = renderHtml(project_json)

  with open("temp.html", "w") as fd_tmp:
    fd_tmp.write(tmp_body)
  receive_user = [project_json["leader"]]
  sendMail(title = f"[{project_json['project']}] {project_json['fromTag']} release - {project_json['todayDate']}", receive_list=receive_user, body=tmp_body )

if __name__ == '__main__':
  args = parser().parse_args()
  emailSend(args)
