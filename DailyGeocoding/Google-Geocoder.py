#----------------------------------------------------------------------
# Name:    Google-Geocoder.py
# Purpose: A simple script to run through winery data and spit out a
#          CSV with lat/lon
# Author:  Jon Koser
#----------------------------------------------------------------------

import geocoder
import csv
import sys
import datetime

GOOGLE_KEY = 'AIzaSyBoBscaL-pwNzwrEgvK1vTJSBAGkdQT3ds'
GOOGLE_LIMIT = 2500 # per day

'''
Should:
    1) Query the max from each service each day
    2) Alternate APIs every 100 queries
    3) Save off results to a CSV file as [Winery, Country, Latitute, Longitude]'''

def main():
    if len(sys.argv) != 2:
        print("Needs to have arguments [inputCSV]")
        exit(1)

    addresses = {}

    inputFile = sys.argv[1]
    countryColumn = 0
    wineryNameColumn = 1
    outputFile = inputFile + "_google-geocoded-{}.csv".format(datetime.date.today())

    with open(inputFile, newline='', encoding='latin') as wineryList:
        import geocoder
        print("opened csv")
        reader = csv.reader(wineryList)

        # url = 'https://maps.googleapis.com/maps/api/geocode/json'
        # params = {'sensor': 'false', 'address': 'Mountain View, CA'}
        # r = requests.get(url, params=params)
        # results = r.json()['results']
        # location = results[0]['geometry']['location']
        # location['lat'], location['lng']

        for index, row in enumerate(reader):
            wineryName = row[wineryNameColumn]
            if not wineryName[-6:].upper() == "WINERY" and not wineryName[-5:].upper() == 'WINES' \
                    and not wineryName[-9:].upper() == 'VINEYARDS' and not wineryName[-8:].upper() == 'VINEYARD':
                wineryName = "{} Winery".format(wineryName)

            searchString = "{}, {}".format(wineryName, row[countryColumn])

            result = geocoder.google(searchString, key=GOOGLE_KEY)

            if result.latlng is not None and result.address is not None:
                print(searchString + " |" + result.address + " | " + str(result.latlng))

            address = result.address
            latlng = result.latlng
            if address in addresses:
                with open(outputFile + "_duplicates.csv", 'a', encoding='utf-8', newline='') as outFile:
                    writer = csv.writer(outFile)
                    writer.writerow([searchString, address, latlng])
            else:
                with open(outputFile, 'a', encoding='utf-8', newline='') as outFile:
                    writer = csv.writer(outFile)
                    writer.writerow([searchString, address, latlng])
                addresses[result.address] = ''


if __name__ == "__main__":
    main()
