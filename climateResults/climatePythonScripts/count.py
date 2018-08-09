import csv
import sys
import datetime
import numpy
import os
import gzip
import shutil

directory = "climateResults/decades/"

def main():
    count=0;
    # print("Searching for: " + sys.argv[1] + " stations.")
    i = 0;
    for j in range(1929, 2018):
        for filename in os.listdir(directory):
            # print(j)
            # print(chr(27) + "[2J")
            # if i%100==0: print("On record: ", str(i), "\t", count, " stations found.")
            if filename.endswith(str(j) + ".op.gz"):
                i+=1;
            #     filenum = int(os.path.join(filename)[:6])
            #     for entry in station:
            #         if int(entry[0]) == filenum:
            #             if sys.argv[1] == entry[2]: count+=1;
            #             break;

        print(str(j) + " Count: ", str(i))

if __name__ == "__main__":
    main()
