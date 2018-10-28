# Author: Yeung King Yiu
"""
The purpose of this python program is to search specific types of facilities near a housing estate through google places API
based on latitudes and longitudes of every housing estate which have been stored in a .csv file
"""

import googlemaps, csv, time, copy


# return the type of a facility by categorizing received sub_type
def find_type(sub_type):
    if sub_type == "bus_station" or sub_type == "train_station" or sub_type == "subway_station":
        type_field = 'transportation'
    elif sub_type == "doctor" or sub_type == "hospital" or sub_type == "dentist":
        type_field = 'health_care'
    elif sub_type == "school":
        type_field = 'school'
    elif sub_type == "restaurant" or sub_type == "meal_delivery" or sub_type == "meal_takeaway":
        type_field = 'food'
    else:
        type_field = 'shopping'
    return type_field


# return a dictionary which stores info of a facility
def store_facility_to_a_dict(facility_dict, facility):
    facility_dict['faci_lat'] = facility['geometry']['location']['lat']
    facility_dict['faci_lng'] = facility['geometry']['location']['lng']
    facility_dict['faci_id'] = facility['id']
    facility_dict['faci_name'] = facility['name']
    return facility_dict


# return a list of coordinates of all facilities surrounding an address
def get_all_facilities_location(list):
    location_list = []
    list_size = len(facility_list)
    for entry in range(list_size):
        lat = list[entry]['faci_lat']
        lng = list[entry]['faci_lng']
        location_list.append((lat, lng))
    return location_list


def combine_with_distance(list, distance_matrix):
    for facility in range(len(list)):
        list[facility]['distance'] = distance_matrix['rows'][0]['elements'][facility]['distance']['value']
    return list

# set path of input and output .csv file
coor_csv = "C:/Users/KingYiu/PycharmProjects/capstone_crawl2/capstone_crawl2/distinct_estate_coor_cleaned.tsv"
output_file = "C:/Users/KingYiu/PycharmProjects/capstone_crawl2/capstone_crawl2/facilities_without_dis.csv"

# Parameter for filtering facilities
sub_type_list = ["bus_station", "train_station", "subway_station",
                 "doctor", "hospital", "dentist",
                 "restaurant", "meal_delivery", "meal_takeaway",
                 "bank", "shopping_mall", "supermarket",
                 "school"]

# connect to google map server
gmap = googlemaps.Client(key="AIzaSyAFtobYgVFNIute1IqZx4IhyQBmYxbgI1c")

with open(coor_csv, "r", encoding="utf-8") as get_coor:
    reader = csv.reader(get_coor, delimiter="\t")
    for line in reader:
        if line[1] == "district":
            continue
        else:
            # get info of estate from a .csv file
            address_info = line
            # a dictionary to store info of a facility
            facility_info = {}
            facility_info['estate'] = address_info[0]
            facility_list = []

            for sub_type in range(len(sub_type_list)):
                facility_info['type'] = find_type(sub_type_list[sub_type])
                # search different kinds of facilities nearby an address
                params = {
                    "location": (address_info[4], address_info[5]),
                    "radius": 1000,
                    "language": "zh-CN",
                    "type": sub_type_list[sub_type],
                }
                facilities = gmap.places_nearby(**params)

                next_page = ""
                # continue when more than 1 page of facilities are found
                while next_page is not None:
                    facilities_num = len(facilities['results'])
                    for i in range(facilities_num):
                        # get info of facility from google query
                        facility_info['sub_type'] = sub_type_list[sub_type]
                        facility_info = store_facility_to_a_dict(facility_dict=facility_info, facility=(facilities['results'][i]))
                        facility_list.append(copy.deepcopy(facility_info))
                        print("facility_list: \n", facility_list)
                        print("facility_info \n", facility_info)
                    try:
                        params['page_token'] = facilities['next_page_token']
                        time.sleep(4)
                        facilities = gmap.places_nearby(**params)
                    except Exception as e:
                        next_page = None

            # calculating distance from the facilities to the address
            # get coordinates of all facilities surrounding a single address
            """
            destination_list = get_all_facilities_location(facility_list)

            params = {
                "origins": (address_info[4], address_info[5]),
                "destinations": destination_list,
                "mode": "walking",
                "language": "zh-CN"
            }
            distance_matrix = gmap.distance_matrix(**params)
            # add the obtained distance back to dictionaries that correspond to different facilities
            facility_list = combine_with_distance(facility_list, distance_matrix)
            """

            # store all facilities near different estates into a .csv file
            with open(output_file, "a", encoding="utf-8", newline="") as write_facilities:
                fieldnames = ['estate', 'type', 'sub_type', 'faci_lat', 'faci_lng', 'faci_id', 'faci_name']
                writer = csv.DictWriter(write_facilities, fieldnames=fieldnames)
                for rows in range(len(facility_list)):
                    writer.writerow(facility_list[rows])
