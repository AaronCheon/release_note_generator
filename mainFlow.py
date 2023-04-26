import argparse
from pathlib import Path
from libs import descriptionMerger,  emailSend,  getCommitList,  getMRdata,  getMRiid,  getTagName, setIssue,  setLink
import re

def parser():
    parse = argparse.ArgumentParser("generating inteflow")
    parse.add_argument("--link")
    parse.add_argument("--tag")
    parse.add_argument("--jira_token")
    parse.add_argument("--gitlab_token")
    parse.add_argument("--project_json", type=Path, help="Project json")
    parse.add_argument("--html_jinja", type=Path, help="Html Jinja")
    parse.add_argument("--option", default="rtl")
    return parse


def totalRunner(args):
    totalPath   = args.link  # git@portal:examples/mga/sprint3.git
    projectName = totalPath.split(":")[1].split(".git")[0]  #examples/mga/sprint3
    gitDir      = totalPath.split(":")[1].split("/")[-1].split(".git")[0]  #sprint3


    pattern = re.compile("([AL|BT|FN]*)[_]REL(\d)(\d)(.*)")
    if pattern.match(args.tag) is None:
        print("None tag")
        return "None tag"

    currentTag, previousTag = getTagName.getTagName(argparse.Namespace(dir=gitDir, current=args.tag))
    commit_list             = getCommitList.getCommitList(argparse.Namespace(from_tag=currentTag, to_tag=previousTag, dir=gitDir))
    iid_lists               = getMRiid.getMRiid(argparse.Namespace(project_name=projectName, token=args.gitlab_token, commit_lists=commit_list))
    mr_data                 = getMRdata.getMRdata(argparse.Namespace(project_name=projectName, token=args.gitlab_token, iid_lists=iid_lists))
    description             = descriptionMerger.descriptionMerger(mrData=mr_data, option=args.option)
    setIssue.setIssueMain(argparse.Namespace(issue_description=str(description), now_tag=currentTag, token=args.jira_token, project_json=args.project_json))
    now_key, pre_key        = setLink.setLinkMain(argparse.Namespace(now_tag=currentTag, pre_tag=previousTag, token=args.jira_token, project_json=open(args.project_json)))
    emailSend.emailSend(argparse.Namespace(from_tag=currentTag, key_id=now_key, jira_token=args.jira_token, project_json=open(args.project_json), html_jinja=args.html_jinja))

    print("exit tag")
    return "exit tag"

#python3.7 mainFlow.py  --link="git@portal:examples/mga/sprint3.git" --tag="AL_REL11" --jira_token=<user token> --gitlab_token=<user token> --project_json releaseData.json --html_jinja emailSend.html.jinja
if __name__ == '__main__':
    args = parser().parse_args()
    totalRunner(args)
