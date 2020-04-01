import csv
import math
from datetime import datetime

# csvFileName0 = "hackageData0.csv"
# # csvFileName = "hackageData.csv"
# csvFileName2 = "hackageData2.csv"
# csvFileName3 = "hackageData3.csv"

csvFileName = "originalHackUrlDates.csv"
writeFileName = "nameAgeMonths.csv"

today = datetime.today()
writeFile = open(writeFileName,'w')
# writeFile.write("Name,Upload Date\n")
writeFile.write("Name, Age (approx. months)\n")

# For date stuff...
with open(csvFileName) as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        #Process Date string and get approximate month
        packageName = row[0]
        if packageName != 'Name':
            dateString = row[2]
            dateString = dateString.strip()
            dateObject = datetime.strptime(dateString,'at %a %b %d %H:%M:%S UTC %Y')
            # print(str(dateObject))
            timeDelta = today - dateObject
            months = math.floor(timeDelta.days/29.53)
            # print(months)
            writeFile.write(packageName + "," + str(months) + "\n")
            # writeFile.write(packageName + "," + str(dateObject) + "\n")
            # print(math.floor(timeDelta.days/29.53))
            # writeFile.write(packageName + ',' + str(months) + '\n')
        # writeFile.write(packageName + ',' + newDateString + '\n')


# with open(csvFileName0) as csvfile:
#     reader = csv.reader(csvfile)
#     for row in reader:
#         #Process Date string and get approximate month
#         packageName = row[0]
#         # versionCount = int(row[1]) + 1
#         downloadString = row[3]
#         stringSplit = downloadString.split()
#         print(int(stringSplit[0]))
#         # print(versionCount)
#         writeFile.write(packageName + ',' + stringSplit[0] + '\n')
