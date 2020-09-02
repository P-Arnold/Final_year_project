from html.parser import HTMLParser
from datetime import datetime
import urllib.request as urllib3
import ssl
from neo4j import GraphDatabase
import csv
# gitFile = open('githubList.csv', 'w')
# primeGitFile = open('primeGithubList.csv', 'w')


# writer = csv.writer(ofile)
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neofour"))

ssl._create_default_https_context = ssl._create_unverified_context

#Neo4J Cypher commands
#Create Node
def add_package(tx, name):
    tx.run("CREATE (p:Package {name: $name}) ", name=name)

#Set git link exists = true
def set_git_true(tx,name):
    tx.run("MATCH (p:Package) WHERE p.name = $name SET p.gitLinkExists = TRUE",name=name)

#Set number of reverse dependencies
def set_num_rev_deps(tx, name, num_rev_deps):
    tx.run("MATCH (p:Package) WHERE p.name = $name SET p.num_rev_deps = $num_rev_deps", name=name, num_rev_deps=num_rev_deps)

#Get ID
def get_package_id(tx, name):
    for id in tx.run("MATCH (p:Package) WHERE p.name = $name RETURN ID(p)", name=name):
        return id

def get_package_name(tx, id):
    for name in tx.run("MATCH (p:Package) WHERE ID(p) = $id RETURN p.name", id=id):
        return name


def get_num__rev_deps(tx, id):
    for count in tx.run("MATCH (a:Package) -[r:ReverseDepends] -> (b:Package) WHERE ID(a) = $id RETURN count(r)", id=id):
        return count

#Check if node exists
def check_package(tx, name):
    for record in tx.run("MATCH (p:Package) WHERE p.name = $name RETURN p", name=name):
        return record

#Check if reverse dependency relationship exists between two nodes
def check_reverse_dependency(tx,nameA,nameB):
    tx.run("RETURN EXISTS( (:Package {name:$nameA})-[:reverse_dependency]-(:Package {name:$nameB}))",nameA=nameA,nameB=nameB)

#Create reverse dependency relationship
def create_reverse_dependency(tx,nameA,nameB):
    tx.run("MATCH (a:Package),(b:Package) WHERE a.name = $nameA AND b.name = $nameB CREATE (a)-[r:ReverseDepends]->(b)",nameA=nameA,nameB=nameB)

#Parser for https://www.stackage.org/lts-14.22 , goes through list of packages
class primaryParser(HTMLParser):
   def handle_starttag(self, tag, attrs):
       if tag == 'a':
           if attrs[0][0] == 'class':
               if attrs[0][1] == 'package-name':
                   self.foundPackage = True
                   self.curUrl = attrs[1][1]
   def handle_data(self,data):
       if self.foundPackage:
           # lastLoc = data.rfind('-')
           # self.packageName = data[:lastLoc] #Extract package name
           # print("Checking for node ",self.packageName)
           # if not driver.session().read_transaction(check_package, self.packageName):
           #     #Create Node in server if one by the same name does not exist
           #     print("Creating node ",self.packageName)
           #     driver.session().write_transaction(add_package, self.packageName)
           self.mainPageUrls.append(self.curUrl) #This list stores all the Urls that are needed for the next parser
           self.foundPackage = False

#Parser for page such as https://www.stackage.org/lts-14.22/package/base-4.12.0.0
#Looks for full list of packages that depend on it (Reverse dependencies)
class packagePageParser(HTMLParser):
   def handle_starttag(self, tag, attrs):
       if attrs:
           for attribute in attrs:
               if attribute[0] == 'href':
                   testUrl = attribute[1]
                   if 'github' in testUrl:
                       # self.gitUrls.append(idRecord[0])
                       driver.session().write_transaction(set_git_true, self.packageName)
                       print(self.packageName," GitHub URL:", testUrl)
                       gitFile.write(testUrl+",")
                       if self.packageName in testUrl:
                           primeGitFile.write(testUrl+",")

   # def handle_data(self,data):


# idx = driver.session().read_transaction(get_package_id, "base")
# print(idx[0])

# idsArray = [467,214,68,2191,2112,363,1087,2133,1379,2092,2299,155,613,835,2263,516,1647,5,1592,1992,2272,1831,88,1686,742,545,1699,2058,1651,1525,1427,1134,2194,1838,80,344,113,967,2287,34,2192,431,52,251,1746,1830,1501,238,1291,2285,1311,1623,430,2268,2048,172,308,1973,364,2321]
# names_array = []
# for id in idsArray:
#     revCount = driver.session().read_transaction(get_package_name, id)
#     names_array.append(revCount[0])
# writer.writerows(map(lambda x: [x], names_array))
# ofile.close()


# writer.writerows(rev_deps)
# creating an object of the overridden class
curUrl = ''
packCount = 0
packageDetails = list()
packageName = ''
foundPackage = False
reverseDep = False
dep = False

parser = primaryParser()
parser.packageName = packageName
parser.foundPackage = foundPackage
parser.packageDetails = packageDetails
parser.packCount = packCount
parser.curUrl = curUrl
parser.reversDep = reverseDep
parser.dep = dep
#Opening NYTimes site using urllib3
parser.mainPageUrls = list()
# driver.session().write_transaction(add_package, "ptom")

html_page = urllib3.urlopen("https://www.stackage.org/lts-14.21")

#Feeding the content
parser.feed(str(html_page.read()))

mainGithubArray = []
#Go through each url from the list of packages at https://www.stackage.org/lts-14.21

for url in parser.mainPageUrls:
    # print("Handling url:", url)
    html_page = urllib3.urlopen(url)
    lastLoc = url.rfind('/')
    packageName = url[lastLoc+1:]
    lastLoc = packageName.rfind('-')
    packageName = packageName[:lastLoc] #The name of the package we are dealing with, extracted from the url
    newPackageParser = packagePageParser()
    newPackageParser.packageName = packageName
    newPackageParser.reverseDep = False
    newPackageParser.revDepsUrl = ''
    packageRevDepsNum = 0
    newPackageParser.revDepsNum = packageRevDepsNum
    # prepare github urls
    idRecord = driver.session().read_transaction(get_package_id, packageName)
    # print(type(idRecord[0]))
    newPackageParser.gitUrls = []

    gitFile.write(str(idRecord[0])+",")
    gitFile.write(packageName+",")
    primeGitFile.write(str(idRecord[0])+",")
    primeGitFile.write(packageName+",")
    # print("Beginning html parsing. Package: ", packageName)
    newPackageParser.feed(str(html_page.read()))
    gitFile.write("\n")
    primeGitFile.write("\n")
    # mainGithubArray.append(newPackageParser.gitUrls)
    # writer.writerows(newPackageParser.gitUrls)

# writer.writerows(mainGithubArray)
gitFile.close()
primeGitFile.close()
