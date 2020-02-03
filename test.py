from html.parser import HTMLParser
import urllib.request as urllib3
import ssl
from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neofour"))

ssl._create_default_https_context = ssl._create_unverified_context

#driver.session().read_transaction(check_package, "atom")
#driver.session().write_transaction(add_package, "atom")
def add_package(tx, name):
    tx.run("CREATE (p:Package {name: $name}) ", name=name)

def set_rev_deps(tx, name, num_deps):
    tx.run("MATCH (p:Package) WHERE p.name = $name SET p.rev_deps = $num_deps", name=name)

def check_package(tx, name):
    for record in tx.run("MATCH (p:Package) WHERE p.name = $name RETURN p", name=name):
        return record

class primaryParser(HTMLParser):
   #Initializing lists
   # lsStartTags = list()
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


           newParser = primaryParser()
           new_html_page = urllib3.urlopen(self.curUrl)
           newParser.feed(str(new_html_page.read()))
           newParser.packageName = ''
           # newParser.foundPackage = False
           # newParser.packageDetails = list()
           # newParser.packCount = 0
           # newParser.curUrl = ''
           # newParser.reversDep = False
           # newParser.dep = False
           newParser.revDepsUrl = ''

           # print("Encountered some data  :", data)
           # self.packageDetails.append((data,self.curUrl))
           # self.packCount += 1
           # print(self.packCount, data)
           self.foundPackage = False
       # if self.dep:
       #     print(data[:21], "\n")
       #     self.dep = False
       if self.reversDep:
           print(data[:18], "\n")
           self.reversDep = False


class packagePageParser(HTMLParser):
   def handle_starttag(self, tag, attrs):
       #commentzzzzzzz
       
   def handle_data(self,data):
       #comments content


class revDepPageParser(HTMLParser):
   def handle_starttag(self, tag, attrs):
       if tag == 'a':
           if attrs[1][0] == 'title':
   def handle_data(self,data):
       #comments content
creating an object of the overridden class
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

# driver.session().write_transaction(add_package, "ptom")

html_page = urllib3.urlopen("https://www.stackage.org/lts-14.21")

#Feeding the content
parser.feed(str(html_page.read()))
# for pack in parser.packageDetails:
#     print("Package Name: ",pack[0])
#     print("URL: ", pack[1])
#     html_page = urllib3.urlopen(pack[1])
#     parser.feed(str(html_page.read()))


#printing the extracted values
# print(parser.lsStartTags)
#print(“End tags”, parser.lsEndTags)
#print(“Start End tags”, parser.lsStartEndTags)
#print(“Comments”, parser.lsComments)
