# Author: Yeung King Yiu
# This this the spider used to crawl housing data

import scrapy, winsound
from capstone_crawl2.items import estate_item
from scrapy_splash import SplashRequest
from random import randint, shuffle


class WebpageSpider(scrapy.Spider):
    name = "estate_spider2"
    start_urls = ["https://shanghai.anjuke.com/sale/"]
    main_page = "https://shanghai.anjuke.com/"

    # Visit the catalog of a single district
    def parse(self, response):
        url_list = response.xpath("//div[(@class = \"items\") and (position() = 1)]/span[@class = \"elems-l\"]/a/@href").extract()
        # randomize district order
        shuffle(url_list)
        for link in range(len(url_list)):
            yield scrapy.Request(url=url_list[link], callback=self.parse_sub_district)

    # Visit the catalog of a sub_district
    def parse_sub_district(self, response):
        url_list = response.xpath("//div[@class = \"sub-items\"]//a/@href").extract()
        # randomize sub_district order
        shuffle(url_list)
        for link in range(len(url_list)):
            request = scrapy.Request(url=url_list[link]+"p50/", callback=self.parse_last_page)
            request.meta['link'] = url_list[link]
            yield request

    def parse_last_page(self, response):
        base_url = response.meta['link']
        page_url = []

        # find maximum page number in a sub_district
        max_number = response.xpath("//div[contains(@class, \"page\")]//i[last()-1]/text()").extract_first()
        if max_number != "50":
            max_number = response.xpath("//div[contains(@class, \"page\")]//a[last()]/text()").extract_first()
        max_number = int(max_number)

        for number in range(1, max_number+1):
            page_url.append(base_url + "p" + str(number) + "/")

        shuffle(page_url)
        for element in range(len(page_url)):
            yield scrapy.Request(url=page_url[element], callback=self.parse_page)

    # real function to crawl from housing catalog
    def parse_page(self, response):
        # get all listing housing on a single page
        # crawl pages are split into batches of size 20 to encounter dynamic links
        # crawling for batch1
        link_list1 = response.xpath("//li[(contains(@class, \"list-item\")) and (position() <= 20)]//div[(@class = \"house-title\")]/a/@href").extract()
        shuffle(link_list1)
        for element in range(len(link_list1)):
            yield SplashRequest(url=link_list1[element], callback=self.parse_details,
                                args={'wait': 1, 'timeout': 180}, endpoint='render.html')

        # crawling for batch2
        link_list2 = response.xpath("//li[(contains(@class, \"list-item\")) and (position() > 20) and (position() <= 40)]//div[(@class = \"house-title\")]/a/@href").extract()
        shuffle(link_list2)
        for element in range(len(link_list2)):
            yield SplashRequest(url=link_list2[element], callback=self.parse_details,
                                args={'wait': 1, 'timeout': 180}, endpoint='render.html')

        # crawling for batch3
        link_list3 = response.xpath("//li[(contains(@class, \"list-item\")) and (position() > 40)]//div[(@class = \"house-title\")]/a/@href").extract()
        shuffle(link_list3)
        for element in range(len(link_list3)):
            yield SplashRequest(url=link_list3[element], callback=self.parse_details,
                                args={'wait': 1, 'timeout': 180}, endpoint='render.html')

        winsound.Beep(2000, 1000)

    # sub function to crawl details of every listed housing
    def parse_details(self, response):
        # forming a dictionary of xpath
        field_name = ["estate", "location_part1", "location_part2", "yearbuild", "housingtype",
                      "roompartition", "pricepersqmeter", "area", "orientation", "floor",
                      "upgradelevel", "refdownpay", "sellingpoint", "ownerview", "supportingfacilities",
                      "expertview", "estatepriceavg", "price", "parkingspace", "greening",
                      "mgmtfee", "sub_districtavg"]

        xpath_dict = {}
        xpath_list = ["//div[@class = \"first-col detail-col\"]/dl[1]//a/text()",
                      "//div[@class = \"first-col detail-col\"]/dl[position()=2]//p/a/text()",
                      "//div[@class = \"first-col detail-col\"]/dl[position()=2]//p/text()",
                      "//div[@class = \"first-col detail-col\"]/dl[3]/dd/text()",
                      "//div[@class = \"first-col detail-col\"]/dl[4]/dd/text()",
                      "//div[@class = \"second-col detail-col\"]/dl[1]/dd/text()",
                      "//div[@class = \"third-col detail-col\"]/dl[2]/dd/text()",
                      "//div[@class = \"second-col detail-col\"]/dl[2]/dd/text()",
                      "//div[@class = \"second-col detail-col\"]/dl[3]/dd/text()",
                      "//div[@class = \"second-col detail-col\"]/dl[4]/dd/text()",
                      "//div[@class = \"third-col detail-col\"]/dl[1]/dd/text()",
                      "//div[@class = \"third-col detail-col\"]/dl[3]/dd/text()",
                      "//div[@class = \"houseInfo-item\"]//div[contains(@class, \"js-house-explain\")]/span/text()",
                      "//div[(@class = \"houseInfo-item\") and (position()=2)]//div/text()",
                      "//div[(@class = \"houseInfo-item\") and (position()=3)]//div/text()",
                      "//dl[contains(@class, \"-character\")]//dd//text()",
                      "//div[@id = \"price_trend\"]//div[@id = \"commhousedesc\"]/span[1]/text()",
                      "//div[@class = \"basic-info clearfix\"]//span[@class = \"light info-tag\"]/em/text()",
                      "//div[@class = \"cmmmap-info\"]//div[position() =4]/p[2]/text()",
                      "//div[@class = \"cmmmap-info\"]//div[position() =5]/p[2]/text()",
                      "//div[@class = \"cmmmap-info\"]//div[position() =6]/p[2]/text()",
                      "//div[@id = \"price_trend\"]//div[@id = \"areahousedesc\"]/span[1]/text()"
                      ]
        for i in range(len(field_name)):
            xpath_dict[field_name[i]] = xpath_list[i]

        # Instantiate an item for storing a listed estate's data
        # plz check pipelines.py for data cleaning and outputing
        item = estate_item()

        item["estate"] = (xpath_dict["estate"]response.xpath).extract_first()
        #print(estate)
        #print(type(estate))

        item["district"] = response.xpath(xpath_dict["location_part1"]).extract()[0]
        item["sub_district"] = response.xpath(xpath_dict["location_part1"]).extract()[1]
        item["address"] = response.xpath(xpath_dict["location_part2"]).extract()
        #print(item["district"])
        #print(type(item["district"]))
        #print(item["sub_district"])
        #print(type(item["sub_district"]))
        #print(item["address"])
        #print(type(item["address"]))

        item["yearbuild"] = response.xpath(xpath_dict["yearbuild"]).extract_first()
        #print(item["yearbuild"])
        #print(type(item["yearbuild"]))

        item["housingtype"] = response.xpath(xpath_dict["housingtype"]) .extract_first()
        #print(item["housingtype"])
        #print(type(item["housingtype"]))

        item["roompartition"] = response.xpath(xpath_dict["roompartition"]).extract_first()
        #print(item["roompartition"])
        #print(type(item["roompartition"]))

        item["pricepersqmeter"] = response.xpath(xpath_dict["pricepersqmeter"]).extract_first()
        #print(item["pricepersqmeter"])
        #print(type(item["pricepersqmeter"]))

        item["area"] = response.xpath(xpath_dict["area"]).extract_first()
        #print(item["area"])
        #print(type(item["area"]))

        item["orientation"] = response.xpath(xpath_dict["orientation"]).extract_first()
        #print(item["orientation"])
        #print(type(item["orientation"]))

        item["floor"] = response.xpath(xpath_dict["floor"]).extract_first()
        #print(item["floor"])
        #print(type(item["floor"]))

        item["upgradelevel"] = response.xpath(xpath_dict["upgradelevel"]).extract_first()
        #print(item["upgradelevel"])
        #print(type(item["upgradelevel"]))

        item["refdownpay"] = response.xpath(xpath_dict["refdownpay"]).extract_first()
        #print(item["refdownpay"])
        #print(type(item["refdownpay"]))

        item["sellingpoint"] = response.xpath(xpath_dict["sellingpoint"]).extract()
        #print(item["sellingpoint"])
        #print(type(item["sellingpoint"]))

        item["ownerview"] = response.xpath(xpath_dict["ownerview"]).extract()
        #print(item["ownerview"])
        #print(type(item["ownerview"]))

        item["supportingfacilities"] = response.xpath(xpath_dict["supportingfacilities"]).extract()
        #print(item["supportingfacilities"])
        #print(type(item["supportingfacilities"]))

        item["expertview"] = response.xpath(xpath_dict["expertview"]).extract()
        #print(item["expertview"])
        #print(type(item["expertview"]))

        item["estatepriceavg"] = response.xpath(xpath_dict["estatepriceavg"]).extract_first()
        #print(item["estatepriceavg"])
        #print(type(item["estatepriceavg"]))

        item["price"] = response.xpath(xpath_dict["price"]).extract_first()
        #print(item["price"])
        #print(type(item["price"]))

        item["parkingspace"] = response.xpath(xpath_dict["parkingspace"]).extract()
        #print(item["parkingspace"])
        #print(type(item["parkingspace"]))

        item["greening"] = response.xpath(xpath_dict["greening"]).extract()
        #print(item["greening"])
        #print(type(item["greening"]))

        item["mgmtfee"] = response.xpath(xpath_dict["mgmtfee"]).extract_first()
        #print(item["mgmtfee"])
        #print(type(item["mgmtfee"]))

        item["sub_districtavg"] = response.xpath(xpath_dict["sub_districtavg"]).extract_first()
        #print(item["sub_districtavg"])
        #print(type(item["sub_districtavg"]))

        # After crawling a housing page,
        # there are 1/3 chance that the spider would go back to the main page of the platform
        # to prevent robotic accessing pattern
        if (randint(-67, 33) > 0):
            SplashRequest(url=self.main_page, args={'wait': 1}, endpoint='render.html')
        return item