import csv
import sys
import os

def main():
    directory = "decades/"
    spreadsheet = "stationsraw.csv"
    outputFile = "subsetSpreadsheet_rerun.csv"
    os.remove(outputFile)

    with open(outputFile, 'a', encoding='utf-8', newline='') as outFile:
        writer = csv.writer(outFile)

        count = 0;
        for filename in os.listdir(directory):
            if count%500 == 0: print(str(count) + " files out of 11,311 processed.")
            if filename.endswith(".csv"):
                count+=1;
                stn = filename.split("_")[2].split(".")[0][3:]

                with open(spreadsheet, newline='', encoding='latin') as stationyear:
                    reader = list(csv.reader(stationyear))

                    for row in reader:
                        if row[0] == 'USAF': continue;
                        if row[0][0] == "A": continue;
                        # print(row[0]==stn)
                        if int(row[0]) == int(stn):
                            writer.writerow(row)
                            break;
main();
