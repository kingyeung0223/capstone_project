# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# Author: Yeung King Yiu

import re
import json, csv

class CapstoneCrawlPipeline(object):
    # remove empty space character character in data
    def remove_empty(self, field):
        sample = []
        if isinstance(field, str):
            field = field.replace("\n", "")
            field = field.replace("\t", "")
            field = field.replace("\v", "")
            field = field.replace("\r", "")
            field = field.replace(" ", "")
        elif isinstance(field, type(sample)):
            for element in range(len(field)):
                field[element] = field[element].replace("\n", "")
                field[element] = field[element].replace("\t", "")
                field[element] = field[element].replace("\v", "")
                field[element] = field[element].replace("\r", "")
                field[element] = field[element].replace(" ", "")
        return field

    # function to check if a numerical data exist or not
    # if it exists, chinese unit would be removed
    def clean_numeric(self, data):
        if isinstance(data, str):
            if re.search(r'[0-9]+(\.[0-9]*)?', data):
                data = re.sub(r'[^0-9\.]', "", data)
        return data

    # function for joining results obtained by extract() from a list into a string
    def list_to_string(self, data_list, separator):
        sample = []
        if isinstance(data_list, type(sample)):
            data_list = separator.join(data_list)
        return data_list

    # a json file would be created and opened when the spider start crawling
    def open_spider(self, spider):
        self.file = open("data.js", "a", encoding="utf-8")

    # the json file would be closed when the spider finishes crawling
    def close_spider(self, spider):
        self.file.close()

    # final function to output result
    def process_item(self, item, spider):
        item['estate'] = self.remove_empty(item['estate'])

        item['district'] = self.remove_empty(item['district'])

        item['sub_district'] = self.remove_empty(item['sub_district'])

        item['address'] = self.list_to_string(item['address'], "")
        item['address'] = self.remove_empty(item['address'])
        item['address'] = item['address'].replace("－", "")

        item['yearbuild'] = self.clean_numeric(item['yearbuild'])

        item['housingtype'] = self.remove_empty(item['housingtype'])

        item['roompartition'] = self.remove_empty(item['roompartition'])

        # in unit 元/平方米
        item['pricepersqmeter'] = self.remove_empty(item['pricepersqmeter'])
        item['pricepersqmeter'] = self.clean_numeric(item['pricepersqmeter'])

        item['area'] = self.remove_empty(item['area'])
        item['area'] = self.clean_numeric(item['area'])

        item['orientation'] = self.remove_empty(item['orientation'])

        item['floor'] = self.remove_empty(item['floor'])

        item['upgradelevel'] = self.remove_empty(item['upgradelevel'])

        # in unit 萬
        item['refdownpay'] = self.remove_empty(item['refdownpay'])
        item['refdownpay'] = self.clean_numeric(item['refdownpay'])

        item['sellingpoint'] = self.remove_empty(item['sellingpoint'])
        item['sellingpoint'] = self.list_to_string(item['sellingpoint'], " ")

        item['ownerview'] = self.remove_empty(item['ownerview'])
        item['ownerview'] = self.list_to_string(item['ownerview'], " ")

        item['supportingfacilities'] = self.remove_empty(item['supportingfacilities'])
        item['supportingfacilities'] = self.list_to_string(item['supportingfacilities'], " ")

        item['expertview'] = self.remove_empty(item['expertview'])
        item['expertview'] = self.list_to_string(item['expertview'], " ")

        # 屋苑平均價 in unit 元/平方米
        item['estatepriceavg'] = self.remove_empty(item['estatepriceavg'])
        item['estatepriceavg'] = self.clean_numeric(item['estatepriceavg'])

        # 分區小區平均價 in unit 元/平方米
        item['sub_districtavg'] = self.remove_empty(item['sub_districtavg'])
        item['sub_districtavg'] = self.clean_numeric(item['sub_districtavg'])

        # 樓盤價格 in unit 萬
        item['price'] = self.remove_empty(item['price'])
        item['price'] = self.clean_numeric(item['price'])

        # in unit 個
        item['parkingspace'] = self.list_to_string(item['parkingspace'], "")
        item['parkingspace'] = self.remove_empty(item['parkingspace'])
        item['parkingspace'] = self.clean_numeric(item['parkingspace'])

        # greening = 0.1 means 10%
        item['greening'] = self.list_to_string(item['greening'], "")
        item['greening'] = self.remove_empty(item['greening'])
        if (item['greening'].find("%") + 1):
            item['greening'] = float(item['greening'][:item['greening'].find("%")]) / 100
            item['greening'] = str(item['greening'])

        # in unit 元/平方米
        item['mgmtfee'] = self.remove_empty(item['mgmtfee'])
        item['mgmtfee'] = self.clean_numeric(item['mgmtfee'])

        # store information into the json file after crawling a housing item
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
