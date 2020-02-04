from html.parser import HTMLParser
from datetime import datetime
import urllib.request as urllib3
import ssl
from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neofour"))

ssl._create_default_https_context = ssl._create_unverified_context

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
   def handle_starttag(self, tag, attrs):
       if tag == 'a':
           if attrs[0][0] == 'class':
               if attrs[0][1] == 'package-name':
                   self.foundPackage = True
                   self.curUrl = attrs[1][1]
   def handle_data(self,data):
       if self.foundPackage:
           lastLoc = data.rfind('-')
           self.packageName = data[:lastLoc]
           print("Checking for node ",self.packageName)
           if not driver.session().read_transaction(check_package, self.packageName):
               #Create Node in server if one by the same name does not exist
               print("Creating node ",self.packageName)
               driver.session().write_transaction(add_package, self.packageName)
           self.mainPageUrls.append(self.curUrl)
           self.foundPackage = False

class packagePageParser(HTMLParser):
   def handle_starttag(self, tag, attrs):
       if tag == 'div':
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
