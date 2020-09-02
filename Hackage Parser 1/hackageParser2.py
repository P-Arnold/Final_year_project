# import cypherFuncs as cy
from html.parser import HTMLParser
from datetime import datetime
# import urllib.request as urllib3
import urllib3
import ssl
import csv
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()
readCsvName = "nameHackrlVers.csv"
writeCsvName = "oHUD3.csv"
writeFile = open(writeCsvName, 'w')
ssl._create_default_https_context = ssl._create_unverified_context


class hackagePageParserA(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if self.versionZero == False:
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
                                if attrs:
                                    for attr in attrs:
                                        if attr[0] == 'href':
                                            self.urlExtension = attr[1]
                                            self.versionZero = True

                                    
    def handle_endtag(self, tag):
        if self.versionZero == False:
            if tag == 'th':
                self.th = False
            if tag == 'td':
                self.td = False
            if tag == 'tr':
                self.tr = False
                if self.versions:
                    self.versions = False
    def handle_data(self,data):
        if self.versionZero == False:
            if self.th:
                if 'Versions' in data:
                    self.versions = True

class hackagePageParserB(HTMLParser):
    def handle_starttag(self, tag, attrs):
        # if self.dateFound == False:
        if tag == 'tbody':
            self.tbody = True
        if self.tbody:
            if tag == 'tr':
                self.tr = True
            if self.tr:
                if tag == 'th':
                    self.th = True
                if self.uploaded:
                    if tag == 'td':
                        self.td = True
    def handle_endtag(self, tag):
        # if self.dateFound == False:
        if tag == 'th':
            self.th = False
        if tag == 'td':
            self.td = False
        if tag == 'tr':
            self.tr = False
            if self.uploaded:
                self.uploaded = False
    def handle_data(self,data):
        # if self.dateCount < 3:
        if self.th:
            if 'Uploaded' in data:
                self.uploaded = True
        if self.uploaded:
            if self.td:
                # print(type(data))
                self.dateData = data
                # self.dateCount +=1
                # self.dateFound = True


writeFile.write("Name,Original Url,Date String\n")
continuing = False
with open(readCsvName) as csvfile:
    reader = csv.reader(csvfile)
    for index, row in enumerate(reader):
        if index > 0:
            packageName = row[0]
            hackageUrl = row[1]
            versionCount = int(row[2])
            if continuing:
                if versionCount > 1:
                    # Get the base version url
                    print("Searching for base URL at ", hackageUrl)
                    hackageUrl=hackageUrl.strip()
                    response = http.request('GET', hackageUrl)
                    # print(response.data.decode('utf-8'))
                    # hackge_url = urllib3.urlopen(hackageUrl)
                    newHackageParserA = hackagePageParserA()
                    newHackageParserA.tbody = False
                    newHackageParserA.tr = False
                    newHackageParserA.th = False
                    newHackageParserA.td = False
                    newHackageParserA.versionZero = False
                    newHackageParserA.versions = False
                    newHackageParserA.urlExtension = ''
                    # newHackageParserA.uploaded = False
                    # newHackageParserA.dateData = ''
                    newHackageParserA.feed(str(response.data.decode('utf-8')))
                    countA = hackageUrl.rfind("/")
                    baseUrl = hackageUrl[:countA]
                    countB = newHackageParserA.urlExtension.rfind("/")
                    thisUrlExtension = newHackageParserA.urlExtension[countB:]
                    hackageUrl = baseUrl + thisUrlExtension

                # Continue on and get the uploaded date
                response = http.request('GET', hackageUrl)
                # hackge_url = urllib3.urlopen(hackageUrl)
                newHackageParserB = hackagePageParserB()
                newHackageParserB.tbody = False
                newHackageParserB.tr = False
                newHackageParserB.th = False
                newHackageParserB.td = False
                newHackageParserB.urlExtension = ''
                newHackageParserB.uploaded = False
                newHackageParserB.dateData = ''
                newHackageParserB.dateFound = False
                newHackageParserB.dateCount = 0
                newHackageParserB.feed(str(response.data.decode('utf-8')))
                dateString = newHackageParserB.dateData
                print(packageName + "," + hackageUrl + "," + dateString)
                writeFile.write(packageName + "," + hackageUrl + "," + dateString + "\n")
            elif packageName == 'array-memoize':
                continuing = True
# Actually skipped almost-fix
