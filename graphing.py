import csv

ifile = open('idPR.csv', 'r')
reader = csv.reader(ifile)
# ofile = open('new.csv', 'w')
# writer = csv.writer(ofile)

dataArray = []
for row in reader:
    # print(type(row))
    dataArray.append(row)

dataArray.pop(0)
# print(len(dataArray))
sum = 0
i = 0
thisRow = dataArray[i]
nextRow = dataArray[i+1]
newArray = []
bool = True
while bool:
    if float(nextRow[1]) == float(thisRow[1]):
        print("Same:",thisRow,nextRow,'\n')
        dataArray.pop(i+1)
    else:
        newArray.append(thisRow)
    if i < len(dataArray)-2:
        i+=1
        thisRow = dataArray[i]
        nextRow = dataArray[i+1]
    else:
        bool = False
print("Length: " , len(dataArray))

for r in newArray:
    print(r)
print("new Length: " , len(newArray))

# writer.writerows(newArray)
