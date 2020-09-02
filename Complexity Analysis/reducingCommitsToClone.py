import datetime
def handleCommitLog(logFileName):
    logFile = open(logFileName,"r") #commitFile, file of log of Commits
    lines = logFile.readlines()
    numLines = len(lines)
    if numLines < 50:
        #Return all
        return lines
    else:
        #get first and last lines
        newestCommit = lines[0]
        oldestCommit = lines[numLines-1]
        logCompsNew = newestCommit.split()
        # commitHashNew = logCompsNew[1]
        dateStrNew = logCompsNew[3]
        logCompsOld = oldestCommit.split()
        dateStrOld = logCompsOld[3]
        newDate = datetime.datetime.strptime(dateStrNew,'%Y-%m-%d')
        oldDate = datetime.datetime.strptime(dateStrOld,'%Y-%m-%d')
        deltaTime = newDate-oldDate
        if numLines < (deltaTime.days)/21:
            print("Return All Here")
            return lines
            #This means theres (roughly) < 1 commit / 3 weeks
        else:
            #Create New Log
            print("Commits are too frequent, creating shortened list")
            newLines = list()
            for i, line in enumerate(lines):
                if i == 0 or i == numLines-1:
                    newLines.append(line)
                else:
                    #Only take commits that are more than 3 weeks apart
                    lastLine = newLines[-1]
                    mRecentLogComps = lastLine.split()
                    mRecentDateStr = mRecentLogComps[3]
                    olderLogComps = line.split()
                    olderDateStr = olderLogComps[3]
                    mRecentDate = datetime.datetime.strptime(mRecentDateStr,'%Y-%m-%d')
                    olderDate = datetime.datetime.strptime(olderDateStr,'%Y-%m-%d')
                    deltaTime = mRecentDate-olderDate
                    if deltaTime.days > 21:
                        newLines.append(line)
            print("Log originally had ",numLines, " commits")
            print("New list has ",len(newLines), " commits")
            print("Diff: ",numLines-len(newLines))
            print(100-(len(newLines)/numLines)*100,"% less")
            return newLines

def getRepoName(gitUrl):
    splitUrl = gitUrl.split('/')
    print(splitUrl)
    for index, chunk in enumerate(splitUrl):
        if chunk.lower() == "github.com":
            gitIndex = index
    repoName = splitUrl[gitIndex+2]
    newUrl = ''
    for i in range(gitIndex+3):
        newUrl = newUrl + splitUrl[i] + '/'
    print("Repo Name: ", repoName)
    print("NewUrl ", newUrl)
    return((repoName,newUrl))
# fileName = 'lensCommitHistory.log'
# handleCommitLog(fileName)
# tUrl = "https://github.com/rubik/argon/"
# getRepoName(tUrl)
