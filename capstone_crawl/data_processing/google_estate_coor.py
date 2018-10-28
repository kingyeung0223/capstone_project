# Author: Yeung King Yiu
"""
This purpose of this python program is to obtain coordinate of all distinct addresses/estates found in
the hosing data which are stored as a .csv file through google geocode API
"""

import googlemaps, csv, json, time

# set path for import and export csv
path_csv = "C:/Users/KingYiu/PycharmProjects/capstone_crawl2/capstone_crawl2/distinct_estate.tsv"
coor_csv = "distinct_estate_coor.csv"

# write the header of out put csv first:
with open(coor_csv, "w", encoding="utf-8") as write_head:
    writer = csv.writer(write_head, delimiter=",")
    writer.writerow(["estate", "district", "sub_district", "address", "lat", "lng"])
write_head.close()

# connect to google map server
gmap = googlemaps.Client(key="AIzaSyCMk2nGKkuocVRefiOobdzJRG1Tjvr-gps")

# read address from csv
with open(path_csv, "r", encoding="utf-8") as reading:
    reader = csv.reader(reading, delimiter="\t")
    full_json_list = []
    for link in reader:
        # ignore header line
        if link[1] == "estate":
            continue
        else:
            # transform address for better search
            address_info = link
            search_key_base = address_info[0]
            # use address + sub_district to find coor
            search_key = search_key_base + "," + address_info[2]

            # check and get coordinate of different addresses
            geocode_result = gmap.geocode(address=search_key, language="zh-CN", region="cn")

            # use alternative search methods if the previous one is unidentified
            tried_alternative = 0
            while(geocode_result is None or len(geocode_result) == 0):
                # search with address + district
                if tried_alternative == 0:
                    search_key = search_key_base + "," + address_info[3]
                    geocode_result = gmap.geocode(address=search_key, language="zh-CN", region="cn")
                    tried_alternative += 1

                # search with estate + sub_district
                elif tried_alternative == 1:
                    search_key = search_key_base + "," + address_info[1]
                    geocode_result = gmap.geocode(address=search_key, language="zh-CN", region="cn")
                    tried_alternative += 1

                # search with estate + district
                elif tried_alternative == 2:
                    search_key = search_key_base
                    geocode_result = gmap.geocode(address=search_key, language="zh-CN", region="cn")
                    tried_alternative += 1
                else:
                    tried_alternative += 1
                    break

            # assign "" to lat and lng if the location is still unidentified
            if tried_alternative == 4:
                lat = lng = ""
            else:
                lat = geocode_result[0]['geometry']['location']['lat']
                lng = geocode_result[0]['geometry']['location']['lng']

            print(lat)
            print(lng)

            # write into csv file
            address_info.append(lat)
            address_info.append(lng)
            print(address_info)
            with open(coor_csv, "a", encoding="utf-8") as write_coor:
                writer = csv.writer(write_coor, delimiter=",")
                writer.writerow(address_info)
