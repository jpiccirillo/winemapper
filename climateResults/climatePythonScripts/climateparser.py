import csv
import sys
import datetime
import numpy
import os
import gzip
import shutil

def main():
    directory = "../../../Downloads/E7C2017D-5F45-4D38-92BB-58919AC74CA9/unpackeddata/"
    # directory = "testing/"
    count = 0;
    for filename in os.listdir(directory):
        if filename.endswith(".op.gz"):
            path = directory + filename

            if filename.endswith("2017.op.gz"):
                # os.remove(path)?
                continue;

            outputFile = "climateResults/"
            filenum = filename[:6]
            # filenum = filename[8:14]

            with gzip.open(path, 'rb') as src, open(path.rstrip('.gz'), 'wb') as dest:
                shutil.copyfileobj(src, dest)

            with open(path.rstrip('.gz'), newline='', encoding='latin') as stationyear:
                reader = list(csv.reader(stationyear))
                # temps = [];

                for k in range(1, 13):
                    # print("-----------------" + str(k) + "------------------")
                    monthlist = [];
                    preciplist = [];
                    write = False;
                    for row in reader:
                        # print(row)
                        if "STN" in row[0][:4]: continue;
                        station = row[0][:6]
                        peices = row[0].split(" ")
                        j = 0; #counter for actual fields, ignoring blanks
                        for i in range (0, len(peices)):

                            if peices[i] == "": continue
                            # print(str(j), "\t", peices[i])
                            if j==2:
                                month = peices[i][4:6]
                                if int(month) != k: break;

                                year = peices[i][:4]
                                day = peices[i][6:8]
                                write = True;
                                # print(year + "\t" + month + "\t" + day, end="\t")

                            elif j==3: monthlist.append(float(peices[i]))
                            elif j==19:
                                precip = float(peices[i][:4])
                                preciplist.append(0) if (precip == 99.9) else preciplist.append(precip)

                            j+=1;
                            if j==20: break;

                    if write:
                        with open(outputFile + "STN" + str(filenum) + ".csv", 'a', encoding='utf-8', newline='') as outFile:
                            writer = csv.writer(outFile)
                            writer.writerow([station, int(year), k, numpy.mean(monthlist), numpy.mean(preciplist), numpy.sum(preciplist)])

                os.remove(path.rstrip(".gz"))
                count += 1;
                if count % 500 == 0: print(str(count) + " files processed.")
                # os.rename(path, directory + "scraped_" + filename)

    print('Total processed: ' + str(count))
if __name__ == "__main__":
    main()
