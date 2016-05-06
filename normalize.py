def get_geodata(address):
    import requests
    URL = "https://maps.googleapis.com/maps/api/geocode/json"
    payload = {
        'address': address,
        'key': 'AIzaSyDRG3RXgL59DvWnxRgKhPDQLKzhYbD3R9E'
    }
    response = requests.get(URL, params=payload)
    return response.json()


def main():
    import csv
    ifile = open('all_bathrooms.csv', "r")
    reader = csv.reader(ifile)
    ofile = open('bathrooms.csv', "w")
    writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    counter = 1
    for row in reader:
        row = next(reader)
        try:
            geodata = get_geodata(row[0] + ',' + row[4])["results"][0]["geometry"]["location"]
            writer.writerow(row + [geodata['lat'], geodata['lng']])
        except IndexError as e:
            print(e)
            writer.writerow(row + ['null', 'null'])
        print(counter)
        counter = counter + 1
    ifile.close()
    ofile.close()

if __name__ == '__main__':
    main()
