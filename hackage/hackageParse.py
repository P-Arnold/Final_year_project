# import cypherFuncs as cy
from html.parser import HTMLParser
from datetime import datetime
import urllib.request as urllib3
import ssl
import csv

ssl._create_default_https_context = ssl._create_unverified_context


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
           lastLoc = data.rfind('-')
           self.packageName = data[:lastLoc] #Extract package name
           print("Checking for node ",self.packageName)
           self.mainPageUrls.append(self.curUrl) #This list stores all the Urls that are needed for the next parser
           self.foundPackage = False

parser = primaryParser()
parser.packageName = ''
parser.foundPackage = False
parser.mainPageUrls = list()
parser.curUrl = ''

class packagePageParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if self.hackageFound == False:
            if tag == 'a':
                if attrs:
                    if attrs[0][0] == 'href':
                        if "hackage.haskell.org/package/" in attrs[0][1]:
                            print(attrs[0][1])
                            self.hackageUrl = attrs[0][1]
                            self.hackageFound = True

   # def handle_data(self,data):


class hackagePageParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if self.downloadData is None:
            if tag == 'tbody':
                self.tbody = True
            if self.tbody:
                if tag == 'tr':
                    self.tr = True
                if self.tr:
                    if tag == 'th':
                        self.th = True
                    if self.versions:
                        if tag == 'td':
                            self.td = True
                        if self.td:
                            if tag == 'a':
                               self.versionCount = self.versionCount + 1
                    if self.uploaded:
                        if tag == 'td':
                            self.td = True
                    if self.downloads:
                        if tag == 'td':
                            self.td = True
    def handle_endtag(self, tag):
        if self.downloadData is None:
            if tag == 'th':
                self.th = False
            if tag == 'td':
                self.td = False
            if tag == 'tr':
                self.tr = False
                if self.versions:
                    self.versions = False
                if self.uploaded:
                    self.uploaded = False
                if self.downloads:
                    self.downloads = False
    def handle_data(self,data):
        if self.downloadData is None:
            if self.th:
                if 'Versions' in data:
                    self.versions = True
                if 'Uploaded' in data:
                    self.uploaded = True
                if 'Downloads' in data:
                    self.downloads = True
            if self.uploaded:
                if self.td:
                    self.dateData = data
            if self.downloads:
                if self.td:
                    self.downloadData = data

html_page = urllib3.urlopen("https://www.stackage.org/lts-14.21")

parser.feed(str(html_page.read()))

# csvFileName = 'hackageLinks2.csv'
# hackageFile =  open(csvFileName, 'w')
# hackageFile.write("Name,Url\n")
# Go through each url from the list of packages at https://www.stackage.org/lts-14.21

continuingScan = False

for url in parser.mainPageUrls:
    print("Handling url:", url)

    lastLoc = url.rfind('/')
    packageName = url[lastLoc+1:]
    lastLoc = packageName.rfind('-')
    packageName = packageName[:lastLoc] #The name of the package we are dealing with, extracted from the url

    if continuingScan:
        html_page = urllib3.urlopen(url)
        newPackageParser = packagePageParser()
        newPackageParser.packageName = packageName
        newPackageParser.hackageFound = False
        newPackageParser.hackageUrl = ''

        print("Searching for Hackage link of ", packageName)
        newPackageParser.feed(str(html_page.read()))
        #Check for Hackage URL
        if newPackageParser.hackageUrl:
            print("Hackage URL Found for ",newPackageParser.packageName)
            #write to file
            # hackageFile.write(packageName + ',' + newPackageParser.hackageUrl + '\n')

            # hackge_url = urllib3.urlopen(newPackageParser.hackageUrl)
            # newHackageParser = hackagePageParser()
            # newHackageParser.tbody = False
            # newHackageParser.tr = False
            # newHackageParser.th = False
            # newHackageParser.td = False
            # newHackageParser.versions = False
            # newHackageParser.versionCount = 0
            # newHackageParser.uploaded = False
            # newHackageParser.downloads = False
            # newHackageParser.downloadData = None
            # newHackageParser.dateData = ''
            # newHackageParser.feed(str(hackge_url.read()))

            # reverseDepPageParser.mainPackageName = newPackageParser.packageName
            # reverseDepPageParser.foundPackName = False
            # hackageFile.write(packageName + ',' + str(newHackageParser.versionCount) + ',')
            # hackageFile.write(newHackageParser.dateData + ',' + newHackageParser.downloadData + '\n')
    elif packageName == "graphviz":
        continuingScan = True
