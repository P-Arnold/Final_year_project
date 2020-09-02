import csv
import subprocess
filename = "../name_pageRank_lts_0.0.csv"
lastScore = 0
rank = 0

for lts in range(0,16):
    filename = "../name_pageRank_lts_" + str(lts) + ".0.csv"
    writeData = list()
    writeData.append(["Name","PR","Rank","NormRank","LTS"]) #Add header
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
        writeFilename = "new_scores_lts" + str(lts) +".csv"
        subprocess.run(["touch",writeFilename]) #Create File to write to
        rank = 0 #Reset rank variable
        csvFile.seek(0) #reset csv file for enumeration
        csvReader = csv.reader(csvFile) #ditto
        #This second loop is for creating the new rows of data that will be
        # written
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
                writeData.append(writeRow)
    print("Writing data, LTS: ", lts)
    writeFile = open(writeFilename,'w')
    with writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(writeData)
