import csv
import sys
import datetime
import numpy
import os
import gzip
import shutil
import math

def main():
    directory = "climateResults/"
    # directory = "testing/"
    count = 0;
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            path = directory + filename

            count += 1;
            outputFile = directory + "decades/"
            with open(path, newline='', encoding='latin') as stnyrs:
                reader = list(csv.reader(stnyrs))
                complete = 0;
                incomplete = 0;
                years = [];
                yrmonth = [];
                stnnum = reader[0][0]

                for decade in range(192, 202):
                    # print(decade)
                    for month in range(1, 13):

                        monthdata = [];
                        precipdata = [];
                        for row in reader:
                            # print(row[0])
                            if row[1].startswith(str(decade)) and int(row[2])==month:
                                # print(decade, "\t", month)
                                # print(row[2], row[1])
                                monthdata.append(float(row[3]))
                                precipdata.append(float(row[4]))

                        avg = numpy.mean(monthdata)
                        precipsum = numpy.sum(precipdata)
                        # print(str(decade) + "0's", "\t", month, "\t", avg)
                        if not math.isnan(avg):
                            with open(outputFile + "decade_" + filename, 'a', encoding='utf-8', newline='') as outFile:
                                writer = csv.writer(outFile)
                                writer.writerow([stnnum, str(decade) + "0", month, avg, numpy.mean(precipdata), precipsum])

        if count % 1000 == 0: print(str(count) + " files processed.")
        
    print('Total processed: ' + str(count))
if __name__ == "__main__":
    main()
