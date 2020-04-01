import cypherFuncs2 as cy
from html.parser import HTMLParser
from datetime import datetime
# import urllib.request as urllib3
import urllib3
import ssl
from neo4j import GraphDatabase

ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()

#Parser for https://www.stackage.org/lts-x.x , goes through list of packages
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
           self.packageName = data[:lastLoc] #Extract package name
           print("Checking for node ",self.packageName)
           if not cy.checkPackage(self.packageName,self.lts):
               #Create Node in server if one by the same name does not exist
               print("Creating node ",self.packageName," LTS:",self.lts)
               cy.addPackage(self.packageName,self.lts)
           self.mainPageUrls.append(self.curUrl) #This list stores all the Urls that are needed for the next parser
           self.foundPackage = False

#Parser for page such as https://www.stackage.org/lts-14.22/package/base-4.12.0.0
#Looks for full list of packages that depend on it (Reverse dependencies)
class packagePageParser(HTMLParser):
   def handle_starttag(self, tag, attrs):
       if self.revDepsUrl is None:
           if tag == 'div':
               if attrs:
                   if attrs[0][1] == 'reverse-dependencies':
                       self.reverseDep = True
                       print("Reverse Deps. for ",self.packageName, "exist.")
           if self.reverseDep:
               if attrs:
                   if attrs[0][0] == 'href':
                       check_string = attrs[0][1]
                       check_string = check_string[-7:]
                       if check_string == 'revdeps': #Looking for link to full list, such as https://www.stackage.org/lts-14.22/package/base-4.12.0.0/revdeps
                           self.revDepsUrl = attrs[0][1]
                           print("revDepsUrl: ",self.revDepsUrl)
                           #could also maybe add something here to stop these parsers generally once finished with the full reverse dependency list
                           #maybe untruth the reversDep at end
   def handle_data(self,data):
       pass
       # if self.revDepsUrl is None:
       #     if self.reverseDep:
       #         if len(data) > 12:
       #             numbPacks = data[8:]
       #             numbPacks = numbPacks[:-12]
       #             self.revDepsNum = numbPacks
       #             print("Setting reverse dependencies in ",self.packageName, " as: ",self.revDepsNum)
       #             cy.setNumRevDeps(self.packageName,self.lts, int(self.revDepsNum)) #set the number of reverse dependencies found in html text
           #comments content

#This is the parser for the page containing the full list of reverse dependencies,
#E.g. https://www.stackage.org/lts-14.22/package/base-4.12.0.0/revdeps
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
           if not cy.checkPackage(packageToAddName,self.lts):
               #Create Node in server if one by the same name does not exist
               print("Creating node ",packageToAddName)
               cy.addPackage(packageToAddName,self.lts)
           #check dependencies
           print("Checking for reverse dependency between ",self.mainPackageName, " and ", packageToAddName )
           if not cy.checkRevDep(self.mainPackageName,packageToAddName,self.lts):
               cy.createRevDep(self.mainPackageName,packageToAddName,self.lts)
           self.foundPackName = False

lts_list = ["13.0","14.0","15.0"]

for lts in lts_list:
    print("*"*20,"GATHERING PACKAGES IN LTS: ",lts,"*"*20)
    # creating an object of the overridden class
    newPrimaryParser = primaryParser()
    newPrimaryParser.foundPackage = False
    newPrimaryParser.curUrl = ''
    newPrimaryParser.packageName = ''
    newPrimaryParser.lts = lts
    newPrimaryParser.mainPageUrls = list()
    currentUrl = "https://www.stackage.org/lts-" + lts
    print("Sending GET Request to ",currentUrl)
    primaryResponse = http.request('GET',currentUrl)
    #Feeding the content
    newPrimaryParser.feed(str(primaryResponse.data.decode('utf-8')))
    print("Approx. ",str(len(newPrimaryParser.mainPageUrls)), "Packages in LTS ",lts )
    #Go through each url from the list of packages at https://www.stackage.org/lts-x.x
    for url in newPrimaryParser.mainPageUrls:
        print("Handling url:", url)
        packageResponse = http.request('GET',url)
        # html_page = urllib3.urlopen(url)
        lastLoc = url.rfind('/')
        packageName = url[lastLoc+1:]
        lastLoc = packageName.rfind('-')
        packageName = packageName[:lastLoc] #The name of the package we are dealing with, extracted from the url
        newPackageParser = packagePageParser()
        newPackageParser.revDepsUrl = None
        newPackageParser.reverseDep = False
        newPackageParser.packageName = packageName
        # newPackageParser.lts = lts
        # newPackageParser.revDepsNum = 0
        print("Beginning html parsing. Package: ", packageName)
        newPackageParser.feed(str(packageResponse.data.decode('utf-8')))
        #check if a reverse dependnecy full list has been created
        if newPackageParser.revDepsUrl:
            print("Reverse Dependency List URL Found for ",newPackageParser.packageName)
            #A url does exist, lets handle them shits
            print("Sending GET Request to ", newPackageParser.revDepsUrl)
            fullListResponse = http.request('GET',newPackageParser.revDepsUrl)
            # fullListUrl = urllib3.urlopen(newPackageParser.revDepsUrl)
            reverseDepPageParser = revDepPageParser()
            reverseDepPageParser.mainPackageName = newPackageParser.packageName
            reverseDepPageParser.foundPackName = False
            reverseDepPageParser.lts = lts
            reverseDepPageParser.feed(str(fullListResponse.data.decode('utf-8')))
