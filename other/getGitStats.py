import urllib3
import json
import csv
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
myToken = "9c4c4d852921de9b021b484e9bee695e82c06ecc"
headersA = {'User-Agent':"Parnold-TCD",'Authorization': 'token %s' % myToken}

def getUser(GitURL,packageName):
    placeNum = GitURL.find(packageName)#Locates number char in url where pkg name starts
    choppedURL = GitURL[:placeNum-1] #brings it to form https://github.com/gitUser *
    # * OR potentially https://github.com/gitUser/xxx
    placeNum = choppedURL.rfind("/")
    gitUser = choppedURL[placeNum+1:] #extract username
    return gitUser

def getContributors(user,pkg):
    apiURL = "https://api.github.com/repos/" + user + "/" + pkg + "/stats/contributors"
    r = http.request('GET',apiURL, headers = headersA)
    jD = json.loads(r.data.decode('utf-8'))
    return(len(jD))

def generalApiCall(owner,repoName):
    inner1 = "{ repository(name: \\\""
    inner2 = "\\\", owner: \\\""
    inner3 = "\\\") { \
    name \
    url \
    watchers {\
        totalCount \
    } \
    stargazers { \
        totalCount \
    } \
    issues { \
        totalCount \
    } \
    mentionableUsers { \
        totalCount \
    } \
    } }"
    innerQuery = inner1 + repoName + inner2 + owner + inner3
    return "{ \"query\":\"" + innerQuery + "\" }"


http = urllib3.PoolManager()
# csvFileName = 'primeGithubList_copy.csv'
csvFileName = 'TrueGithubLinks.csv'


#commented
# url = "https://api.github.com/repos/haskell/bytestring/stats/contributors"
# myToken = "9c4c4d852921de9b021b484e9bee695e82c06ecc"
# headersA = {'User-Agent':"Parnold-TCD",'Authorization': 'token %s' % myToken}
# r = http.request('GET',url, headers = headersA)
# jD = json.loads(r.data.decode('utf-8'));
# # print(json.loads(r.data.decode('utf-8')))
#
# print(len(jD))

# json.loads(r.data.decode('utf-8'))
# {'User-Agent':"Parnold-TCD"},{
# ,headers={'Authorization':myToken}

# GitURL = "https://github.com/mstksg/advent-of-code-api/releases/tag/v0.1.2.2"
# packageName = "advent-of-code-api"
#
# placeNum = GitURL.find(packageName)#Locates number char in url where pkg name starts
# choppedURL = GitURL[:placeNum-1] #brings it to form https://github.com/gitUser
# placeNum = choppedURL.rfind("/")
# gitUser = choppedURL[placeNum+1:] #extract username

#

# pName = "lens"
# pOwner = "ekmett"
#
gitApiUrl = "https://api.github.com/graphql"
# headersB = {"Authorization": 'bearer %s' % myToken}
# hopeQ = generalApiCall(pOwner,pName)
# # print(hopeQ)
# r = http.request('POST',gitApiUrl, body=hopeQ, headers = headersA)
#
# # data processing, once json has been retrieved
# jData = json.loads(r.data.decode('utf-8'))
# repoData = jData["data"]["repository"]
# mentUsers = repoData["mentionableUsers"]["totalCount"]
# watchers = repoData["watchers"]["totalCount"]
# issues = repoData["issues"]["totalCount"]
# stars = repoData["stargazers"]["totalCount"]

# print("issues:",type(issues))

# gitFile = open('apiPrimeData.csv', 'w') DONT RE WRITE YET (THURS 5/3/2020 19:35)
# gitFile = open("first_test_true_links.csv", 'w')


# String bytestring
# test_url = "https://github.com/redneb/hs-adler32"
# Yurl = "https://github.com/ncaq/yesod-form-bootstrap4#readme"
# str_find = "github.com/"
# tname = "adler32"
# # nameLoc = test_url.rfind(tname)
# print("TEST 1:")
# print(test_url.find(str_find))
# print(len(str_find),"\n")
#
# splitUrl = Yurl.split('/')
# print(splitUrl)
# if len(splitUrl) > 4:
#     if '#' in splitUrl[4]:
#         ownerString = splitUrl[4]
#         charStop = ownerString.find('#')
#         print(ownerString[:charStop])


# !! ATTENTION PETER you need to chop the given url from
# test_url.find(str_find) + len(str_find) ... that should leave you with redneb/hs-adler32
#then you can find("/") and cut to there to get the owner name...

#Stupid past Peter... use string.split('/')


with open(csvFileName) as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[2]:
            pkg_id = row[0]
            git_url = row[2]
            pkg_name = row[1]
            split_url = git_url.split('/')
            if len(split_url) > 4:
                usr = split_url[3]
                repo_name = split_url[4]
                if '#' in repo_name:
                    charStop = repo_name.find('#')
                    repo_name = repo_name[:charStop]
            # usr = getUser(git_url,pkg_name)
            apiCall = generalApiCall(usr,repo_name)
            httpRequest = http.request('POST',gitApiUrl, body=apiCall, headers = headersA)
            jsonData = json.loads(httpRequest.data.decode('utf-8'))
            repoData = jsonData["data"]["repository"]
            # print(repoData)
            # print(type(repoData))
            print(repo_name)
            if repoData is None:
                errorData = jsonData["errors"][0]
                print(errorData["message"])
                # gitFile.write(pkg_id+",")
                # gitFile.write("error"+",")
                # gitFile.write(errorData["message"]+"\n")
            else:
                mentUsers = repoData["mentionableUsers"]["totalCount"]
                watchers = repoData["watchers"]["totalCount"]
                issues = repoData["issues"]["totalCount"]
                stars = repoData["stargazers"]["totalCount"]
                # print(type(pkg_id))
                gitFile.write(pkg_id+",")
                gitFile.write(str(mentUsers)+",")
                gitFile.write(str(stars)+",")
                gitFile.write(str(issues)+",")
                gitFile.write(str(watchers)+"\n")
            # contributors = getContributors(usr,pkg_name)
            # print(pkg_name,"  ",contributors)
