import csv
import subprocess
filename = "../name_pageRank_lts_0.0.csv"
















datesAr = ["2020-02-16","2019-08-05","2018-12-23","2018-07-09","2018-03-12","2017-12-19","2017-07-26","2017-02-12","2016-09-14","2016-05-25","2016-01-26","2016-01-06","2015-08-12","2015-04-02","2015-01-01","2014-12-12"]
writeData = list()
writeData.append(["Name","PR","Rank","NormRank","LTS","Date"]) #Add header
for lts in range(0,16):
    rank = 0
    lastScore = 0
    filename = "../name_pageRank_lts_" + str(lts) + ".0.csv"
    # writeData = list()
    # writeData.append(["Name","PR","Rank","NormRank","LTS"]) #Add header
    # writeData will hold all data to be written to a single csv, per lts
    with open(filename,'r') as csvFile:
        csvReader = csv.reader(csvFile)
        #This initial loop will get the count of packages and lowest score
        for i, row in enumerate(csvReader):
            if i == 0:
                continue
            else:
                # print(row)
                packName = row[0]
                packScore = row[1]
                #This if condition allows the same rank to be given to packages
                #With the same score.
                if packScore != lastScore:
                    rank += 1
                    lastScore = packScore
                # print(packName,": ",rank)
        lowestRank = rank
        N = i #Number of packages
        # writeFilename = "new_scores_lts" + str(lts) +".csv"
        # subprocess.run(["touch",writeFilename]) #Create File to write to
        rank = 0 #Reset rank variable
        csvFile.seek(0) #reset csv file for enumeration
        csvReader = csv.reader(csvFile) #ditto
        #This second loop is for creating the new rows of data that will be
        # written
        print("lowest Rank: ", lowestRank)
        for j, row in enumerate(csvReader):
            writeRow = []
            if j == 0:
                continue
            else:
                # print(row)
                packName = row[0]
                writeRow.append(packName)
                packScore = row[1]
                writeRow.append(packScore)
                if packScore != lastScore:
                    rank += 1
                    lastScore = packScore
                writeRow.append(rank)
                #if below for giving max normalised score of 1 to all bottom
                #packages
                if rank == lowestRank:
                    writeRow.append(1)
                else:
                    writeRow.append(rank/N)
                writeRow.append(lts)
                writeRow.append(datesAr[15-lts])
                writeData.append(writeRow)
writeFilename = "master_new_scores.csv"
print("Writing data to master...")
writeFile = open(writeFilename,'w')
with writeFile:
    writer = csv.writer(writeFile)
    writer.writerows(writeData)
