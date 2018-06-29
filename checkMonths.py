import csv
import sys
import datetime
import numpy
import os
import gzip
import shutil

def main():
    directory = "climateResults/decades/"
    # directory = "testing/"
    count = 0;
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            path = directory + filename

            count += 1;

            with open(path, newline='', encoding='latin') as stnyrs:
                reader = list(csv.reader(stnyrs))
                complete = 0;
                incomplete = 0;
                years = [];
                yrmonth = [];
                stnnum = reader[0][0]
                for row in reader:
                    years.append(row[1])
                    yrmonth.append([row[1], row[2]])

                years = set(years)

                for year in years:
                    # print("checking: ", year)
                    monthcount = 0;
                    for k in range(0, len(yrmonth)):
                        if int(yrmonth[k][0]) == int(year):
                            # print(yrmonth[k][1])
                            if yrmonth[k][1]: monthcount +=1;

                    if monthcount == 12: complete+=1;
                    else: incomplete+=1;

                print(stnnum,"\t", format(float(incomplete/len(years)), '.3f'), "\t", complete)

                if complete > 0:
                    os.rename(path, directory + "whole_" + filename)

    print('Total processed: ' + str(count))
if __name__ == "__main__":
    main()
