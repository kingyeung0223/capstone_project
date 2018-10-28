import csv

def export_distinct():
    read_file = "C:/Users/KingYiu/PycharmProjects/capstone_crawl2/raw_data_full.csv"
    with open(read_file, "r", encoding="utf-8") as reading:
        csv_reader = csv.DictReader(reading)
        export_csv = "location_info.csv"
        with open(export_csv, "w", encoding="utf-8", newline="") as writing:
            all_field_names = ['address', 'area', 'district', 'estate', 'estatepriceavg',
                               'expertview', 'floor', 'greening', 'housingtype', 'mgmtfee',
                               'orientation', 'ownerview', 'parkingspace', 'price', 'pricepersqmeter',
                               'refdownpay', 'roompartition', 'sellingpoint', 'sub_district', 'sub_districtavg',
                               'supportingfacilities', 'upgradelevel', 'yearbuild']
            target_field = ['address', 'district', 'estate', 'sub_district']
            csv_writer = csv.DictWriter(writing, fieldnames=target_field)
            csv_writer.writeheader()
            for line in csv_reader:
                delete_field = ['area', 'estatepriceavg', 'expertview', 'floor', 'greening', 'housingtype', 'mgmtfee', 'orientation', 'ownerview', 'parkingspace', 'price', 'pricepersqmeter', 'refdownpay', 'roompartition', 'sellingpoint', 'sub_districtavg', 'supportingfacilities', 'upgradelevel', 'yearbuild']
                line['address'] = line['address'].split(",")
                line['address'] = line['address'][0]
                for i in delete_field:
                    del line[i]
                csv_writer.writerow(line)

def clean_address_fullset ():
    read_file = "C:/Users/KingYiu/PycharmProjects/capstone_crawl2/raw_data_full.csv"
    with open(read_file, "r", encoding="utf-8") as reading:
        csv_reader = csv.DictReader(reading)
        export_csv = "data_cleaned_add.csv"
        with open(export_csv, "w", encoding="utf-8", newline="") as writing:
            all_field_names = ['house_id', 'address', 'area', 'district', 'estate', 'estatepriceavg',
                               'expertview', 'floor', 'greening', 'housingtype', 'mgmtfee',
                               'orientation', 'ownerview', 'parkingspace', 'price', 'pricepersqmeter',
                               'refdownpay', 'roompartition', 'sellingpoint', 'sub_district', 'sub_districtavg',
                               'supportingfacilities', 'upgradelevel', 'yearbuild']
            target_field = ['address', 'district', 'estate', 'sub_district']
            csv_writer = csv.DictWriter(writing, fieldnames=all_field_names)
            csv_writer.writeheader()
            i = 1
            for line in csv_reader:
                line['house_id'] = i
                line['address'] = line['address'].split(",")
                line['address'] = line['address'][0]
                i += 1
                csv_writer.writerow(line)

def main():
    export_distinct()
    return 0

main()