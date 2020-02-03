from html.parser import HTMLParser
from datetime import datetime
import urllib.request as urllib3
import ssl
from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neofour"))

ssl._create_default_https_context = ssl._create_unverified_context

#driver.session().read_transaction(check_package, "atom")
#driver.session().write_transaction(add_package, "atom")
def add_package(tx, name):
    tx.run("CREATE (p:Package {name: $name}) ", name=name)

def set_num_rev_deps(tx, name, num_rev_deps):
    tx.run("MATCH (p:Package) WHERE p.name = $name SET p.num_rev_deps = $num_rev_deps", name=name, num_rev_deps=num_rev_deps)

def check_package(tx, name):
    for record in tx.run("MATCH (p:Package) WHERE p.name = $name RETURN p", name=name):
        return record
def check_reverse_dependency(tx,nameA,nameB):
    tx.run("RETURN EXISTS( (:Package {name:$nameA})-[:reverse_dependency]-(:Package {name:$nameB}))",nameA=nameA,nameB=nameB)

def create_reverse_dependency(tx,nameA,nameB):
    tx.run("MATCH (a:Package),(b:Package) WHERE a.name = $nameA AND b.name = $nameB CREATE (a)-[r:ReverseDepends]->(b)",nameA=nameA,nameB=nameB)

class primaryParser(HTMLParser):
   #Initializing lists

   # lsEndTags = list()
   # lsStartEndTags = list()
   # lsComments = list()
   #HTML Parser Methods
   def handle_starttag(self, tag, attrs):
       # if tag == 'meta':
       #     if attrs[1][0] == 'content':
       #         self.packageName = attrs[1][1]
       #         if not driver.session().read_transaction(check_package, self.packageName):
       #             driver.session().write_transaction(add_package, self.packageName)
       if tag == 'a':
           if attrs[0][0] == 'class':
               if attrs[0][1] == 'package-name':
                   self.foundPackage = True
                   self.curUrl = attrs[1][1]
               # print(attrs[1][1])
           # if attrs[0][0] == 'href':
           #     check_string = attrs[0][1]
           #     check_string = check_string[-7:]
           #     if check_string == 'revdeps':
           #         self.reversDep = True
           #         newParser.revDepsUrl = attrs[0][1]
                   #Really I need to call another html parser here...
       # if tag =='div':
       #     # if attrs[0][1] == 'dependencies':
       #     #     self.dep = True
       #     if attrs[0][1] == 'reverse-dependencies':
       #         self.reversDep = True
   def handle_data(self,data):
       if self.foundPackage:
           lastLoc = data.rfind('-')
           self.packageName = data[:lastLoc]
           print("Checking for node ",self.packageName)
           if not driver.session().read_transaction(check_package, self.packageName):
               #Create Node in server if one by the same name does not exist
               print("Creating node ",self.packageName)
               driver.session().write_transaction(add_package, self.packageName)
           # print("Creating new packagePageParser()")
           # newPackageParser = packagePageParser()
           # newPackageParser.packageName = self.packageName
           # newPackageParser.reverseDep = False
           # packageRevDepsNum = 0
           # newPackageParser.revDepsNum = packageRevDepsNum

           self.mainPageUrls.append(self.curUrl)

           # PackageMainPage = urllib3.urlopen(self.curUrl)
           # print("Opening: ", self.curUrl)
           # newPackageParser.feed(str(PackageMainPage.read()))


           #Go to PackagePageParser()

           #Probably don't need this stuff anymore
           # newParser = primaryParser()
           # new_html_page = urllib3.urlopen(self.curUrl)
           # newParser.feed(str(new_html_page.read()))
           # newParser.packageName = ''
           # # newParser.foundPackage = False
           # # newParser.packageDetails = list()
           # # newParser.packCount = 0
           # # newParser.curUrl = ''
           # # newParser.reversDep = False
           # # newParser.dep = False
           # newParser.revDepsUrl = ''

           # print("Encountered some data  :", data)
           # self.packageDetails.append((data,self.curUrl))
           # self.packCount += 1
           # print(self.packCount, data)
           self.foundPackage = False
       # if self.dep:
       #     print(data[:21], "\n")
       #     self.dep = False
       # if self.reversDep:
       #     print(data[:18], "\n")
       #     self.reversDep = False


class packagePageParser(HTMLParser):
   def handle_starttag(self, tag, attrs):
       if tag == 'div':
           # print(attrs)
           if attrs:
               if attrs[0][1] == 'reverse-dependencies':
                   self.reverseDep = True
                   print("reverseDep = True")
       if self.reverseDep:
           if attrs:
               if attrs[0][0] == 'href':
                   check_string = attrs[0][1]
                   check_string = check_string[-7:]
                   if check_string == 'revdeps':
                       self.revDepsUrl = attrs[0][1]
                       print("revDepsUrl: ",self.revDepsUrl)
                       #Enter full list link here
                       # reverseDepPageParser = revDepPageParser()
                       # reverseDepPageParser.mainPackageName = self.packageName
                       # reverseDepPageParser.foundPackName = False

                       # fullListPage = urllib3.urlopen(self.revDepsUrl)
                       # reverseDepPageParser.feed(str(fullListPage.read()))

                       #could also maybe add something here to stop these parsers generally once finished with the full reverse dependency list

                       #maybe untruth the reversDep at end

   def handle_data(self,data):
       if self.reverseDep:
           if len(data) > 12:
               numbPacks = data[8:]
               numbPacks = numbPacks[:-12]
               self.revDepsNum = numbPacks
               #I planned to add a cypher call here to check the number of stored reverse dependencies but I'm just gonna set it anyway
               # print("Setting reverse dependencie in ",self.packageName, " as: ",self.revDepsNum)
               # driver.session().write_transaction(set_num_rev_deps, self.packageName, int(self.revDepsNum)) #set the number of reverse dependencies found in html text


       #comments content


class revDepPageParser(HTMLParser):
   def handle_starttag(self, tag, attrs):
       if tag == 'a':
           if len(attrs)>1:
               if attrs[1][0] == 'title':
                   infoString = attrs[1][1]
                   # mainName = self.mainPackageName
                   if infoString.find(self.mainPackageName):
                       self.foundPackName = True
   def handle_data(self,data):
       if self.foundPackName:
           #extract new package name from data and write to server
           lastLoc = data.rfind('-')
           packageToAddName = data[:lastLoc]
           print("Checking for package ",packageToAddName)
           if not driver.session().read_transaction(check_package, packageToAddName):
               #Create Node in server if one by the same name does not exist
               print("Creating node ",packageToAddName)
               driver.session().write_transaction(add_package, packageToAddName)
           #check dependencies
           print("Checking for reverse dependency between ",self.mainPackageName, " and ", packageToAddName )
           if not driver.session().read_transaction(check_reverse_dependency,self.mainPackageName,packageToAddName):
               driver.session().write_transaction(create_reverse_dependency,self.mainPackageName,packageToAddName)
           self.foundPackName = False

       #comments content
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
# for pack in parser.packageDetails:
#     print("Package Name: ",pack[0])
#     print("URL: ", pack[1])
#     html_page = urllib3.urlopen(pack[1])
#     parser.feed(str(html_page.read()))

# urlLog = open("mainPageUrls.txt","a")
# urlLog.write("\n")
# urlLog.write(str(datetime.now()))
# urlLog.close()
# print(parser.mainPageUrls)
for url in parser.mainPageUrls:
    print("Handling url:", url)
    html_page = urllib3.urlopen(url)
    lastLoc = url.rfind('/')
    packageName = url[lastLoc+1:]
    lastLoc = packageName.rfind('-')
    packageName = packageName[:lastLoc]
    newPackageParser = packagePageParser()
    newPackageParser.packageName = packageName
    newPackageParser.reverseDep = False
    newPackageParser.revDepsUrl = ''
    packageRevDepsNum = 0
    newPackageParser.revDepsNum = packageRevDepsNum
    print("Beginning html parsing. Package: ", packageName)
    newPackageParser.feed(str(html_page.read()))
    #check if a reverse dependnecy full list has been create
    if newPackageParser.revDepsUrl:
        print("Reverse Dependency List URL Found for ",newPackageParser.packageName)
        #a url does exist, lets handle them shits
        fullListUrl = urllib3.urlopen(newPackageParser.revDepsUrl)
        reverseDepPageParser = revDepPageParser()
        reverseDepPageParser.mainPackageName = newPackageParser.packageName
        reverseDepPageParser.foundPackName = False
        reverseDepPageParser.feed(str(fullListUrl.read()))

#lets do the mainpage ur stuff here...
# print(len(parser.mainPageUrls))
#printing the extracted values
# print(parser.lsStartTags)
#print(“End tags”, parser.lsEndTags)
#print(“Start End tags”, parser.lsStartEndTags)
