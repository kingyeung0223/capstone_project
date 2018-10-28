# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

# Author: Yeung King Yiu

import scrapy


class estate_item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 屋苑
    estate = scrapy.Field()

    # 分區小區
    sub_district = scrapy.Field()

    # 分區
    district = scrapy.Field()

    # 地址
    address = scrapy.Field()

    yearbuild = scrapy.Field()

    housingtype = scrapy.Field()

    # 單位間隔
    roompartition = scrapy.Field()

    pricepersqmeter = scrapy.Field()

    area = scrapy.Field()

    # 座向
    orientation = scrapy.Field()

    floor = scrapy.Field()

    upgradelevel = scrapy.Field()

    # 參考首期
    refdownpay = scrapy.Field()

    sellingpoint = scrapy.Field()

    ownerview = scrapy.Field()

    supportingfacilities = scrapy.Field()

    expertview = scrapy.Field()

    estatepriceavg = scrapy.Field()

    sub_districtavg = scrapy.Field()

    price = scrapy.Field()

    parkingspace = scrapy.Field()

    greening = scrapy.Field()

    mgmtfee = scrapy.Field()
