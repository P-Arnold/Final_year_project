import csv
import datetime
import json
import reducingCommitsToClone as commitProc
import statistics
import subprocess
from datetime import timedelta
# from datetime import datetime
# For url in urls:
# packageName = "lens"
# gitUrl = "https://github.com/ekmett/lens"

csvFile = open("githubUrls.csv",'r')
csvReader = csv.reader(csvFile)
continuing = True
for row in csvReader:
    packageName = row[0]
    originalGitUrl = row[1]
     #This was used becuase I hadn't incorporated a decent method of
     # handling errors when the processing was halted
    if packageName == 'flat-mcmc':
        continuing = False
    if continuing:
        continue
    if originalGitUrl == "Github url": #Skip the header
        continue

    print("PackageName:",packageName)
    print("Original Url:", originalGitUrl)
    toop = commitProc.getRepoName(originalGitUrl)
    gitRepoDir = toop[0]
    adjustedUrl = toop[1]
    #Cloning into repo, getting commit log
    subprocess.run(["zsh","clone.zsh",gitRepoDir,adjustedUrl]) #clones git repo, gets commit log
    commitFileName = gitRepoDir + "CommitHistory.log" #Where the log of commits will be stored
    commitFile = open(commitFileName,"r") #commitFile, file of log of Commits
    argonDirName = packageName+"Argon" #e.g lensArgon, a temporary file for storing the argon complexity scores
    jsonWriteFile = packageName +".json"
    jsonWriteFilePath = "jsons/" + jsonWriteFile
    subprocess.run(["mkdir",argonDirName]) #Create Directory To hold Argon data...
    subprocess.run(["touch",jsonWriteFilePath]) #Create file to hold compressed Argon Data
    jsonList = list()
    jsonData = {}
    jsonData[packageName] = []
    #Count number of commits
    num_lines = sum(1 for line in commitFile)
    print("Number of Commits in log: ",num_lines)
    manyCommits = False
    if num_lines >= 100:
        manyCommits = True
        print("WILL PROCESS THIS REPO")
    if manyCommits:
        newCommits = commitProc.handleCommitLog(commitFileName)
        #Handle each commit
        for line in newCommits:
            commitLogComponents = line.split()
            commitHash = commitLogComponents[1]
            dateStr = commitLogComponents[3]
            print(dateStr)
            print(commitHash)
            subprocess.run(["zsh","argon.zsh",packageName,commitHash,dateStr,gitRepoDir])
            jsonFileName = dateStr+"_"+commitHash+".json"
            jsonFilePath = packageName+"Argon/"+jsonFileName
            jsonFile = open(jsonFilePath,"r")
            argonData = json.load(jsonFile)
            complexityList = list()
            for path in argonData:
                if path["type"] == "result":
                    for block in path["blocks"]:
                        complexityList.append(block["complexity"])
            if len(complexityList) > 1:
                jsonObj = {
                "commit": commitHash,
                "date": dateStr,
                "compArray": complexityList
                }
            else:
                jsonObj = {}
            jsonData[packageName].append(jsonObj)
        with open(jsonWriteFilePath, 'w') as outfile:
            json.dump(jsonData, outfile)
    else:
        print("Too few commits... Probably done before")
    subprocess.run(["rm","-rf", gitRepoDir]) #Delete repository
    subprocess.run(["rm","-rf", argonDirName]) #Delete Argon files
    subprocess.run(["rm","-rf", commitFileName]) #Delete commit history


#Need to clean up / delete files that are not needed
