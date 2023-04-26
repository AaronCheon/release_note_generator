import argparse
import subprocess
import re

def parser():
    parse = argparse.ArgumentParser(description=".description merge to generate a integrated update /release note")
    parse.add_argument("--mrdata")  # example --mr_data=target/example.json
    parse.add_argument("--option", default="rtl")
    return parse

class MR:
    def __init__(self):
        self.rtl = []
        self.verification = []
        self.design = []
        self.etc = []

def descriptionMerger(mrData, option):
    mr_data = mrData
    rtlUpdatesPart = "\nh2. RTL Updates\n"
    verificationUpdates = "\nh2. Verification Updates\n"
    designUpdates = "\nh2. Design Updates\n"
    etcUpdate = "\nh2. ETC Updates\n"
    pattern = re.compile("- \w+ Updates")
    linkPattern = re.compile("\[.+-.+\]")
    linkKey = re.compile("\w+-\w+")
    allMr = MR()

    for iid in mr_data:
        try :
            releaseNote = iid['description'].replace("## Updates","")
            lsts = pattern.findall(releaseNote)
            for index, update in enumerate(lsts):
                data = ""
                if(index != len(lsts) - 1):
                    data = releaseNote.split(update)[1].split(lsts[index+1])[0].split("- ETC")[0]
                else:
                    data = releaseNote.split(update)[1].split("- ETC")[0]
                if "RTL" in update:
                    allMr.rtl.append(data)
                elif "Verification" in update:
                    allMr.verification.append(data)
                elif "Design" in update:
                    allMr.verification.append(data)
            etc = releaseNote.split("- ETC")
            if len(etc) > 1:
                allMr.etc.append(etc[1])

        except Exception as e:
            print(e)
            pass

    mediator = ""
    if option == "full" or option == "rtl":
        if(len(allMr.rtl)) != 0:
            mediator += rtlUpdatesPart
            mediator  += "".join(allMr.rtl)
    if option == "full" or option == "design":
        if(len(allMr.design)) != 0:
            mediator += designUpdates
            mediator += "".join(allMr.design)

    if option == "full" or option == "verification":
        if(len(allMr.verification)) != 0:
            mediator += verificationUpdates
            mediator += "".join(allMr.verification)
    if option == "full" or option == "etc":
        if (len(allMr.etc)) != 0:
            mediator += etcUpdate
            mediator += "".join(allMr.etc)

    linkList = list(set(linkPattern.findall(mediator)))

    for each in linkList:
        tmp = linkKey.findall(each)[0]
        mediator =  mediator.replace(tmp,f"[{tmp}|https://aaroncheon.atlassian.net/browse/{tmp}] ")

    return "h1. Release Note \n" + mediator.replace("\n\n","\n").replace("\n\n","\n").replace("\nh2.","\n\nh2.")

if __name__ == "__main__":
    args = parser().parse_args()
    with open(args.mrdata) as f :
        mr_data = json.load(f)
    descriptionMerger(mr_data, args.option)
